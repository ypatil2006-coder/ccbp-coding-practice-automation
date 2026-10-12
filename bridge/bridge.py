import socket
import json
import base64
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class CDPClient:
    def __init__(self):
        self.sock = None
        self.session_id = None
        self.target_info = None
        self.msg_id = 1
        self.pending_responses = {}
        self.lock = threading.Lock()
        self.running = True

    def connect(self):
        with open('/home/yash/.config/google-chrome/DevToolsActivePort') as f:
            lines = [line.strip() for line in f if line.strip()]
        port = int(lines[0])
        path = lines[1]

        self.sock = socket.socket()
        self.sock.connect(('127.0.0.1', port))
        key = 'dGhlIHNhbXBsZSBub25jZQ=='
        req = (
            f'GET {path} HTTP/1.1\r\n'
            f'Host: 127.0.0.1:{port}\r\n'
            f'Upgrade: websocket\r\n'
            f'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Key: {key}\r\n'
            f'Sec-WebSocket-Version: 13\r\n\r\n'
        )
        self.sock.sendall(req.encode())
        resp = self.sock.recv(4096)
        if b'101 WebSocket' not in resp:
            raise RuntimeError(f"WebSocket handshake failed: {resp.decode(errors='replace')}")

        t = threading.Thread(target=self._recv_loop, daemon=True)
        t.start()

        self.attach_tab()

    def attach_tab(self):
        targets_res = self.send_cmd('Target.getTargets')
        targets = targets_res.get('result', {}).get('targetInfos', [])
        
        # Priority 1: Page with learning.ccbp.in or ccbp.in
        target = None
        for t_info in targets:
            if t_info.get('type') == 'page' and 'ccbp.in' in t_info.get('url', ''):
                target = t_info
                break

        # Priority 2: Any page
        if not target:
            for t_info in targets:
                if t_info.get('type') == 'page':
                    target = t_info
                    break

        if not target:
            raise RuntimeError("No page target found!")

        self.target_info = target
        target_id = target['targetId']

        attach_res = self.send_cmd('Target.attachToTarget', {'targetId': target_id, 'flatten': True})
        self.session_id = attach_res.get('result', {}).get('sessionId')

        self.send_cmd('Runtime.enable', session_id=self.session_id)
        self.send_cmd('Page.enable', session_id=self.session_id)
        print(f"Attached successfully to PAGE: {target.get('title')} ({target.get('url')}) sessionId={self.session_id}")

    def _recv_loop(self):
        buf = bytearray()
        while self.running:
            try:
                chunk = self.sock.recv(65536)
                if not chunk:
                    break
                buf.extend(chunk)

                while len(buf) >= 2:
                    b1 = buf[0]
                    b2 = buf[1]
                    opcode = b1 & 0x0f
                    is_masked = (b2 & 0x80) != 0
                    length = b2 & 0x7f

                    offset = 2
                    if length == 126:
                        if len(buf) < 4: break
                        length = int.from_bytes(buf[2:4], 'big')
                        offset = 4
                    elif length == 127:
                        if len(buf) < 10: break
                        length = int.from_bytes(buf[2:10], 'big')
                        offset = 10

                    mask_bytes = None
                    if is_masked:
                        if len(buf) < offset + 4: break
                        mask_bytes = buf[offset:offset+4]
                        offset += 4

                    if len(buf) < offset + length:
                        break

                    payload = buf[offset:offset+length]
                    del buf[:offset+length]

                    if is_masked:
                        payload = bytearray(b ^ mask_bytes[i % 4] for i, b in enumerate(payload))

                    if opcode == 1:
                        try:
                            msg_text = payload.decode('utf-8', errors='replace')
                            msg_json = json.loads(msg_text)
                            msg_id = msg_json.get('id')
                            if msg_id in self.pending_responses:
                                ev, res_container = self.pending_responses[msg_id]
                                res_container[0] = msg_json
                                ev.set()
                        except Exception as e:
                            print("Error parsing incoming message:", e)
                    elif opcode == 8:
                        self.running = False
                        break
            except Exception as e:
                print("Recv loop terminated:", e)
                break

    def send_cmd(self, method, params=None, session_id=None, timeout=10.0):
        with self.lock:
            self.msg_id += 1
            cur_id = self.msg_id

        msg = {'id': cur_id, 'method': method}
        if params is not None:
            msg['params'] = params
        if session_id:
            msg['sessionId'] = session_id

        ev = threading.Event()
        res_container = [None]
        self.pending_responses[cur_id] = (ev, res_container)

        self._send_frame(json.dumps(msg))

        if not ev.wait(timeout):
            del self.pending_responses[cur_id]
            raise TimeoutError(f"CDP command {method} (id={cur_id}) timed out")

        del self.pending_responses[cur_id]
        return res_container[0]

    def _send_frame(self, text):
        payload = text.encode('utf-8')
        length = len(payload)
        frame = bytearray([0x81])
        mask = b'\x12\x34\x56\x78'
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(length.to_bytes(2, 'big'))
        else:
            frame.append(0x80 | 127)
            frame.extend(length.to_bytes(8, 'big'))
        frame.extend(mask)
        masked_payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        frame.extend(masked_payload)
        self.sock.sendall(frame)

    def evaluate(self, expr, await_promise=True):
        try:
            res = self.send_cmd('Runtime.evaluate', {
                'expression': expr,
                'returnByValue': True,
                'awaitPromise': await_promise
            }, session_id=self.session_id, timeout=10.0)
            return res.get('result', {}).get('result', {})
        except TimeoutError:
            self.attach_tab()
            res = self.send_cmd('Runtime.evaluate', {
                'expression': expr,
                'returnByValue': True,
                'awaitPromise': await_promise
            }, session_id=self.session_id, timeout=10.0)
            return res.get('result', {}).get('result', {})

    def screenshot(self, file_path):
        res = self.send_cmd('Page.captureScreenshot', {
            'format': 'png'
        }, session_id=self.session_id, timeout=10.0)
        b64_data = res.get('result', {}).get('data')
        if b64_data:
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(b64_data))
            return True
        return False

client = CDPClient()

class BridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        try:
            if self.path == '/status':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = {
                    'status': 'connected',
                    'target': client.target_info,
                    'session_id': client.session_id
                }
                self.wfile.write(json.dumps(data).encode())
            elif self.path == '/reattach':
                client.attach_tab()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok', 'target': client.target_info}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body, strict=False) if body else {}
            except Exception:
                data = {}

            if self.path == '/eval':
                expr = data.get('expression') or data.get('code')
                result = client.evaluate(expr)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok', 'result': result}).encode())

            elif self.path == '/cdp':
                method = data.get('method')
                params = data.get('params')
                sid = data.get('sessionId', client.session_id)
                res = client.send_cmd(method, params, session_id=sid)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok', 'result': res}).encode())

            elif self.path == '/screenshot':
                path = data.get('path', '/tmp/ccbp_screenshot.png')
                ok = client.screenshot(path)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok' if ok else 'error', 'path': path}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())

def main():
    print("Connecting to Chrome CDP...")
    client.connect()
    server = ThreadingHTTPServer(('127.0.0.1', 9999), BridgeHandler)
    print("Bridge server listening on http://127.0.0.1:9999")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        client.running = False
        client.sock.close()

if __name__ == '__main__':
    main()
