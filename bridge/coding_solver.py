#!/usr/bin/env python3
"""
CCBP Coding Practice Automation Helper for AI Agents.
Provides high-level programmatic commands over http://127.0.0.1:9999
"""

import sys
import time
import json
import urllib.request
import urllib.error

BRIDGE_URL = "http://127.0.0.1:9999"

def eval_js(expr):
    """Executes a JavaScript expression on the active CCBP tab."""
    payload = json.dumps({'expression': expr}).encode('utf-8')
    req = urllib.request.Request(
        f"{BRIDGE_URL}/eval",
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('result', {}).get('value')
    except Exception as e:
        return {'error': str(e)}

def reattach():
    """Re-attaches bridge to the active CCBP tab."""
    req = urllib.request.Request(f"{BRIDGE_URL}/reattach")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get_problem_details():
    """Extracts problem title, description, and editor starter code."""
    script = """
    (() => {
        const titleEl = document.querySelector('h1, [class*="ProblemTitle"], [class*="title"]');
        const descEl = document.querySelector('.markdown-body, [class*="MarkdownTextContainer"], [class*="Description"]');
        let starterCode = '';
        if (window.ace && ace.edit) {
            try {
                const ed = ace.edit('codingQuestionEditor');
                if (ed) starterCode = ed.getValue();
            } catch (e) {}
        }
        return {
            title: titleEl ? titleEl.innerText.trim() : null,
            description: descEl ? descEl.innerText.trim() : null,
            starterCode: starterCode
        };
    })()
    """
    return eval_js(script)

def inject_code(code_str):
    """Injects solution code directly into Ace Editor buffer instantly (<2ms)."""
    encoded = json.dumps(code_str)
    script = f"""
    (() => {{
        if (!window.ace || !ace.edit) return {{ success: false, reason: 'Ace editor not loaded' }};
        const ed = ace.edit('codingQuestionEditor');
        if (!ed) return {{ success: false, reason: 'codingQuestionEditor element not found' }};
        ed.setValue({encoded}, -1);
        return {{ success: true, length: {len(code_str)} }};
    }})()
    """
    return eval_js(script)

def click_run():
    """Triggers the Run Code button."""
    script = """
    (() => {
        const btn = document.getElementById('runCode') || document.querySelector('[data-testid="runCode"]');
        if (btn) {
            btn.click();
            return { clicked: true };
        }
        return { clicked: false, error: 'Run button not found' };
    })()
    """
    return eval_js(script)

def click_submit():
    """Triggers the Submit Code button."""
    script = """
    (() => {
        const btn = document.getElementById('submitCode') || document.querySelector('[data-testid="submitCode"]');
        if (btn) {
            btn.click();
            return { clicked: true };
        }
        return { clicked: false, error: 'Submit button not found' };
    })()
    """
    return eval_js(script)

def poll_status(timeout_sec=25):
    """Polls CCBP evaluation status until execution finishes or times out."""
    start = time.time()
    while time.time() - start < timeout_sec:
        time.sleep(0.5)
        text = eval_js("document.body.innerText") or ""
        if "Hurray!" in text or "Testcases Passed" in text:
            lines = [l.strip() for l in text.split('\n') if 'Testcases Passed' in l or 'Passed' in l]
            return {'status': 'completed', 'summary': lines[:5]}
        if "Compilation Error" in text or "Runtime Error" in text or "Wrong Answer" in text:
            return {'status': 'failed', 'details': text[:500]}
    return {'status': 'timeout'}

def go_back():
    """Navigates back to the course/syllabus view and handles confirmation modals."""
    script = """
    (() => {
        const backBtn = document.querySelector('[data-testid="practice-header-back-button"]');
        if (backBtn) {
            backBtn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
            return { backClicked: true };
        }
        return { backClicked: false };
    })()
    """
    res = eval_js(script)
    time.sleep(0.4)
    confirm_script = """
    (() => {
        const yesBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'YES');
        if (yesBtn) {
            yesBtn.click();
            return { modalDismissed: true };
        }
        return { modalDismissed: false };
    })()
    """
    modal_res = eval_js(confirm_script)
    return {'back': res, 'modal': modal_res}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 coding_solver.py [details|inject <file>|run|submit|poll|back|reattach]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == 'details':
        print(json.dumps(get_problem_details(), indent=2))
    elif cmd == 'inject':
        if len(sys.argv) < 3:
            code = sys.stdin.read()
        else:
            with open(sys.argv[2], 'r') as f:
                code = f.read()
        print(json.dumps(inject_code(code), indent=2))
    elif cmd == 'run':
        print(json.dumps(click_run(), indent=2))
    elif cmd == 'submit':
        print(json.dumps(click_submit(), indent=2))
    elif cmd == 'poll':
        print(json.dumps(poll_status(), indent=2))
    elif cmd == 'back':
        print(json.dumps(go_back(), indent=2))
    elif cmd == 'reattach':
        print(json.dumps(reattach(), indent=2))
    else:
        print(f"Unknown command: {cmd}")
