import sys
import json
import urllib.request

def eval_js(code):
    req = urllib.request.Request(
        'http://127.0.0.1:9999/eval',
        data=json.dumps({'expression': code}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

if __name__ == '__main__':
    code = sys.stdin.read() if not sys.argv[1:] else sys.argv[1]
    res = eval_js(code)
    print(json.dumps(res, indent=2))
