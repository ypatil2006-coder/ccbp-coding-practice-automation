#!/usr/bin/env python3
"""
CCBP Portal MCQ Practice Automation Helper
Connects to persistent CDP bridge at http://127.0.0.1:9999
"""

import time
import json
import urllib.request

def eval_js(expr):
    req = urllib.request.Request(
        'http://127.0.0.1:9999/eval',
        data=json.dumps({'expression': expr}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8')).get('result', {}).get('value')

def get_current_question():
    script = """
    (() => {
        const qEl = document.querySelector(".markdown-body, [class*=\\"MarkdownTextContainer\\"]");
        const options = Array.from(document.querySelectorAll("label.radioButtonLabel")).map((l, i) => ({
            index: i,
            text: l.innerText.trim()
        }));
        return {
            question: qEl ? qEl.innerText.trim() : null,
            options
        };
    })()
    """
    return eval_js(script)

def answer_and_advance(target_index):
    # Select option
    eval_js(f'document.querySelectorAll("label.radioButtonLabel")[{target_index}].click()')
    time.sleep(0.1)
    
    # Click SUBMIT
    eval_js('(() => { const b = Array.from(document.querySelectorAll("button")).find(el => el.innerText.trim() === "SUBMIT"); if (b) b.click(); })()')
    time.sleep(0.4)
    
    # Click NEXT
    eval_js('(() => { const b = Array.from(document.querySelectorAll("button")).find(el => el.innerText.trim() === "NEXT"); if (b) b.click(); })()')

if __name__ == '__main__':
    q = get_current_question()
    print("Current Question:", json.dumps(q, indent=2))
