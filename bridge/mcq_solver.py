#!/usr/bin/env python3
"""
CCBP Portal MCQ Practice Automation Helper for AI Agents.
Connects to persistent CDP bridge at http://127.0.0.1:9999
"""

import sys
import time
import json
import urllib.request
import urllib.error

BRIDGE_URL = "http://127.0.0.1:9999"

def eval_js(expr):
    """Executes JavaScript in the active CCBP tab via persistent bridge."""
    req = urllib.request.Request(
        f"{BRIDGE_URL}/eval",
        data=json.dumps({'expression': expr}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8')).get('result', {}).get('value')
    except Exception as e:
        return {'error': str(e)}

def get_current_question():
    """Extracts the active question text, options list, and question status."""
    script = """
    (() => {
        const qEl = document.querySelector(".markdown-body, [class*=\\"MarkdownTextContainer\\"]");
        const options = Array.from(document.querySelectorAll("label.radioButtonLabel")).map((l, i) => ({
            index: i,
            text: l.innerText.trim()
        }));
        const progressEl = Array.from(document.querySelectorAll("*")).find(el => el.innerText && el.innerText.includes("QUESTIONS ATTEMPTED"));
        const proceedBtn = document.querySelector("button.StartButton-gjsfIy") || Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "PROCEED");
        return {
            question: qEl ? qEl.innerText.trim() : null,
            options: options,
            progress: progressEl ? progressEl.innerText.trim() : null,
            isCompleted: !!proceedBtn
        };
    })()
    """
    return eval_js(script)

def select_and_submit(target_index):
    """Selects the designated option, clicks SUBMIT, then advances with NEXT."""
    # Step 1: Select Option
    eval_js(f'document.querySelectorAll("label.radioButtonLabel")[{target_index}].click()')
    time.sleep(0.15)
    
    # Step 2: Click SUBMIT
    eval_js('(() => { const b = Array.from(document.querySelectorAll("button")).find(el => el.innerText.trim() === "SUBMIT"); if (b) b.click(); })()')
    time.sleep(0.4)
    
    # Step 3: Click NEXT (or check if completed)
    advance_res = eval_js('(() => { const b = Array.from(document.querySelectorAll("button")).find(el => el.innerText.trim() === "NEXT"); if (b) { b.click(); return { advanced: true }; } return { advanced: false }; })()')
    return {'selected': target_index, 'advance': advance_res}

def click_proceed():
    """Exits the completion modal and returns to syllabus view."""
    script = """
    (() => {
        const b = document.querySelector("button.StartButton-gjsfIy") || Array.from(document.querySelectorAll("button")).find(el => el.innerText.trim() === "PROCEED");
        if (b) {
            b.click();
            return { proceeded: true };
        }
        return { proceeded: false, error: 'Proceed button not found' };
    })()
    """
    return eval_js(script)

def click_start_practice():
    """Clicks START PRACTICE button on the topic syllabus view."""
    script = """
    (() => {
        const b = Array.from(document.querySelectorAll("button")).find(el => el.innerText.trim() === "START PRACTICE");
        if (b) {
            b.click();
            return { started: true };
        }
        return { started: false, error: 'Start practice button not found' };
    })()
    """
    return eval_js(script)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('question', 'get'):
        q = get_current_question()
        print(json.dumps(q, indent=2))
    elif sys.argv[1] == 'answer':
        if len(sys.argv) < 3:
            print("Error: Missing option index (0-based)")
            sys.exit(1)
        idx = int(sys.argv[2])
        res = select_and_submit(idx)
        print(json.dumps(res, indent=2))
    elif sys.argv[1] == 'proceed':
        print(json.dumps(click_proceed(), indent=2))
    elif sys.argv[1] == 'start':
        print(json.dumps(click_start_practice(), indent=2))
    else:
        print("Usage: python3 mcq_solver.py [question|answer <index>|proceed|start]")
