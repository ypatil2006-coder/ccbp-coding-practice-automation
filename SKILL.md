---
name: ccbp-browser-automation
description: Instructions and operational protocols for AI agents to autonomously solve CCBP coding and MCQ practices using browser automation, Chrome DevTools Protocol (CDP), and persistent bridge architecture without remote debugging permission popups.
---

# CCBP Portal Browser Automation: AI Agent Skill Guide

This skill guides AI agents on how to automate and solve **Coding Practices** and **MCQ Practices** on the **CCBP Learning Portal** (`https://learning.ccbp.in`) using browser automation and the Chrome DevTools Protocol (CDP).

---

## 1. Core Architecture & Remote Debugging Constraint (Rule 1)

### The Chrome Security Constraint
In modern Chromium / Google Chrome (v128+ on Linux / Wayland), connecting an ad-hoc debugging client triggers an OS-level confirmation modal:
> *"Allow remote debugging? A third-party application is requesting access to inspect and automate Chrome."*

If an agent spawns disposable browser instances, creates ephemeral Puppeteer/Playwright connections, or repeatedly opens and closes WebSockets to port `9222`, Chrome bombards the user with permission popups, halting automation.

### The Single Persistent Bridge Solution
To ensure zero repeated notifications:
1. **Endpoint Discovery**: Read Chrome's active debugging port and path from:
   ```
   /home/yash/.config/google-chrome/DevToolsActivePort
   ```
   - Line 1: Port (usually `9222`)
   - Line 2: Browser target path (e.g. `/devtools/browser/<guid>`)
2. **Single Handshake**: Establish **one** long-lived WebSocket connection to `ws://127.0.0.1:<port><path>` **without** an `Origin` header (avoiding 403 Forbidden origin checks).
3. **Session Multiplexing**: Attach to the active CCBP tab via `Target.attachToTarget` (`flatten: true`) and retain the `sessionId`.
4. **Local Daemon Bridge (`bridge.py`)**: Expose local HTTP endpoints on `http://127.0.0.1:9999`:
   - `POST /eval`: Dispatches `Runtime.evaluate` over the persistent WebSocket (<= 2 ms).
   - `POST /cdp`: Sends raw CDP commands (`method`, `params`).
   - `GET /status`: Returns connection health and active target info.
   - `GET /reattach`: Re-queries `Target.getTargets` and attaches to the newest CCBP tab if URL navigation occurred.

---

## 2. CCBP DOM & Component Selector Catalog

### Coding Practice Interface
| Action / Element | Selector / JavaScript API | Execution Notes |
| :--- | :--- | :--- |
| **Problem Cards** | `[data-testid="card-container"]` | Zero-indexed cards in practice syllabus view |
| **Code Tab** | `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Code")` | Mounts Ace Editor if currently viewing Description/Editorial |
| **Description Tab** | `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Description")` | Contains problem statement, examples, and constraints |
| **Ace Editor Buffer** | `ace.edit("codingQuestionEditor")` | Global Ace editor instance attached to `window.ace` |
| **Code Injection** | `ace.edit("codingQuestionEditor").setValue(code, -1)` | Instant full-buffer replacement (sets cursor to top, no dropped keys) |
| **Read Editor Code** | `ace.edit("codingQuestionEditor").getValue()` | Extracts current starter template or student code |
| **Run Button** | `document.getElementById("runCode")` | Compiles and executes code against public sample cases |
| **Submit Button** | `document.getElementById("submitCode")` | Evaluates code against hidden test suite |
| **Back Button** | `document.querySelector('[data-testid="practice-header-back-button"]')` | Official React router back button |
| **Unsaved Changes Modal** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "YES")` | Dismisses exit confirmation modal |

### MCQ Practice Interface
| Action / Element | Selector / JavaScript API | Execution Notes |
| :--- | :--- | :--- |
| **Start Practice** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "START PRACTICE")` | Launches active MCQ session from topic overview |
| **Question Statement** | `.markdown-body` or `[class*="MarkdownTextContainer"]` | Contains question text, formatted code blocks, and math |
| **Option Radio Labels** | `document.querySelectorAll("label.radioButtonLabel")` | Array of clickable option labels (0-indexed) |
| **Submit Choice** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "SUBMIT")` | Evaluates selected radio option |
| **Advance Question** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "NEXT")` | Dynamically replaces SUBMIT button after evaluation |
| **Proceed Button** | `document.querySelector("button.StartButton-gjsfIy")` | Exits the completion summary modal (text: `"PROCEED"`) |

---

## 3. Operational Workflow: Coding Practices

When automating a coding problem:

### Step 1: Inspect Problem Statement & Starter Code
Run:
```bash
python3 bridge/coding_solver.py details
```
- Read the description to determine time and space complexity constraints.
- Inspect `starterCode`:
  - Check if driver code with `int main()` is provided or if a `class solution` / function signature is expected.
  - Check if data structures (e.g., `struct Node` for Linked Lists or Trees) are pre-defined in the harness. **Do not re-declare pre-defined classes/structs**, or compilation will fail with duplicate symbol errors.

### Step 2: Synthesize C++ Solution
- Write optimal C++17 implementation into a temporary file (e.g. `/tmp/solution.cpp`).
- Handle all boundary conditions: null pointers, single-node lists, empty inputs, cycle detection bounds.

### Step 3: Inject Code via Direct Buffer Replacement
**Never** type characters one-by-one via keystroke emulation (`Input.dispatchKeyEvent`). Keystroke typing drops characters and triggers auto-closing braces.
Inject via:
```bash
python3 bridge/coding_solver.py inject /tmp/solution.cpp
```
Under the hood, this executes:
```javascript
ace.edit('codingQuestionEditor').setValue(code, -1);
```

### Step 4: Run Sample Cases
```bash
python3 bridge/coding_solver.py run
```
Poll the page text for `Compiled Successfully` and verify sample outputs match expected outputs.

### Step 5: Submit Hidden Cases
```bash
python3 bridge/coding_solver.py submit
```
Poll until `Testcases Passed` or `Hurray!` is detected. Verify all test cases pass.

### Step 6: Clean Back Navigation
```bash
python3 bridge/coding_solver.py back
```
This triggers the back navigation button and automatically clicks `"YES"` if the portal prompts with an unsaved changes confirmation modal.

---

## 4. Operational Workflow: MCQ Practices

When automating MCQ sessions:

### Step 1: Fetch Active Question
```bash
python3 bridge/mcq_solver.py question
```
Returns structured JSON:
```json
{
  "question": "Question text...",
  "options": [
    {"index": 0, "text": "Option A"},
    {"index": 1, "text": "Option B"},
    {"index": 2, "text": "Option C"},
    {"index": 3, "text": "Option D"}
  ],
  "progress": "QUESTIONS ATTEMPTED: X/10",
  "isCompleted": false
}
```

### Step 2: Deduce and Select Option
Analyze the algorithmic properties, deduce the correct 0-based option index, and execute:
```bash
python3 bridge/mcq_solver.py answer <index>
```
This performs a three-phase action:
1. Dispatches click on `label.radioButtonLabel[index]`.
2. Dispatches click on the `"SUBMIT"` button.
3. Dispatches click on the dynamic `"NEXT"` button once the answer is evaluated.

### Step 3: Handle Session Completion
Repeat until `isCompleted` is `true` (Question 10/10). Then exit to syllabus:
```bash
python3 bridge/mcq_solver.py proceed
```

---

## 5. Edge Cases & Autonomous Self-Healing

| Symptom | Root Cause | Autonomous Recovery Procedure |
| :--- | :--- | :--- |
| **Port 9999 connection refused** | Bridge daemon was terminated or system restarted. | Launch `python3 bridge/bridge.py` in background (`IsDaemon: true`). Confirm via `curl -s http://127.0.0.1:9999/status`. |
| **`ace is not defined` or editor not found** | The question page is showing the Description or Editorial tab. | Switch to Code tab: `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Code").click()`. |
| **Duplicate symbol compilation error** | Student code re-defines classes/structs (like `Node` or `class solution`) already declared in CCBP test harness. | Inspect `starterCode` using `python3 bridge/coding_solver.py details` and retain only the requested class or method body. |
| **Back button does not return to syllabus** | Unsaved changes modal is blocking navigation. | Click the confirmation button: `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "YES").click()`. |
| **Browser URL changed / tab reloaded** | Portal navigated to a new question UUID. | Invoke `http://127.0.0.1:9999/reattach` or `python3 bridge/coding_solver.py reattach` to re-sync target session. |
| **Submit button missing or disabled** | Previous run/submit is still compiling (`Processing...`). | Wait 1-2 seconds for execution to complete before clicking Submit. |

---

## 6. Bridge CLI Quick Reference

```bash
# Bridge Lifecycle
python3 bridge/bridge.py                     # Start persistent CDP daemon (:9999)
curl -s http://127.0.0.1:9999/status         # Check health & active target
curl -s http://127.0.0.1:9999/reattach       # Re-attach to active CCBP tab

# Coding Practices
python3 bridge/coding_solver.py details      # Extract title, description, starter code
python3 bridge/coding_solver.py inject <file># Set Ace buffer
python3 bridge/coding_solver.py run          # Run sample cases
python3 bridge/coding_solver.py submit       # Submit against test suite
python3 bridge/coding_solver.py poll         # Poll judge status
python3 bridge/coding_solver.py back         # Navigate back (auto-dismisses modal)

# MCQ Practices
python3 bridge/mcq_solver.py question        # Get current question & options
python3 bridge/mcq_solver.py answer <index>  # Select option, submit, advance
python3 bridge/mcq_solver.py proceed         # Exit 10/10 modal back to syllabus
python3 bridge/mcq_solver.py start           # Launch next practice from syllabus
```
