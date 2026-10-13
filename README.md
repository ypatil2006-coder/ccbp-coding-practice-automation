# CCBP Portal Browser Automation Suite & Agent Skill

A production-grade browser automation suite and skill specification for AI agents to solve **Coding Practices** and **MCQ Practices** on the **CCBP Learning Portal** (`https://learning.ccbp.in`) via Chrome DevTools Protocol (CDP) and `/browser` workflows.

---

## 📌 Agent Skill Specification

This repository contains the official Antigravity skill definition:  
👉 **[`SKILL.md`](SKILL.md)** — Ingestible agent instructions with YAML frontmatter, execution state machines, DOM blueprints, and operational runbooks.

---

## 🛡️ Core Architecture: Rule 1 Compliance (Persistent CDP Bridge)

### The Chrome Security Constraint
In Chromium / Google Chrome 128+ on Linux and Wayland, any ad-hoc remote debugging connection initiates an OS-level confirmation modal:
> *"Allow remote debugging? A third-party application is requesting access to inspect and automate Chrome."*

Opening ephemeral WebSocket connections, creating short-lived Puppeteer/Playwright instances, or closing and reopening debugging sockets will repeatedly trigger permission popups, halting automated agent pipelines.

### The Persistent Daemon Solution
To guarantee zero repeated popups and sub-millisecond execution:
1. **Target Discovery**: Read Chrome's active debugging port and path directly from `/home/yash/.config/google-chrome/DevToolsActivePort`.
2. **Single Handshake**: Establish exactly **one** persistent WebSocket connection to `ws://127.0.0.1:<port><path>` with no `Origin` header (avoiding 403 Forbidden origin checks).
3. **Session Multiplexing**: Attach to the active CCBP tab using `Target.attachToTarget` (`flatten: true`) and retain the `sessionId`.
4. **Local Daemon Bridge (`bridge/bridge.py`)**: Expose local HTTP JSON-RPC endpoints on `http://127.0.0.1:9999`:
   - `POST /eval`: Evaluates JavaScript expressions in the active tab context (<= 2 ms).
   - `POST /cdp`: Sends raw CDP commands (`method`, `params`).
   - `GET /status`: Verifies connection health and active target metadata.
   - `GET /reattach`: Dynamically re-discovers and re-attaches to the CCBP tab if URL navigation occurred.

---

## 🎯 CCBP DOM & Component Selector Catalog

### Coding Practice Interface
| Action / Element | Selector / JavaScript API | Execution Notes |
| :--- | :--- | :--- |
| **Problem Cards** | `[data-testid="card-container"]` | Problem cards listed on practice syllabus view |
| **Code Tab** | `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Code")` | Mounts Ace editor when viewing problem description |
| **Description Tab** | `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Description")` | Contains problem statement, examples, and constraints |
| **Ace Editor Buffer** | `ace.edit("codingQuestionEditor")` | Global Ace editor instance attached to `window.ace` |
| **Code Injection** | `ace.edit("codingQuestionEditor").setValue(code, -1)` | Instant full-buffer replacement (sets cursor to beginning, no dropped characters) |
| **Read Editor Code** | `ace.edit("codingQuestionEditor").getValue()` | Extracts current starter template or student code |
| **Run Button** | `document.getElementById("runCode")` | Compiles and executes code against public sample cases |
| **Submit Button** | `document.getElementById("submitCode")` | Evaluates code against the full hidden test suite |
| **Back Button** | `document.querySelector('[data-testid="practice-header-back-button"]')` | Official React router back button |
| **Unsaved Changes Modal** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "YES")` | Dismisses exit confirmation modal |

### MCQ Practice Interface
| Action / Element | Selector / JavaScript API | Execution Notes |
| :--- | :--- | :--- |
| **Start Practice** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "START PRACTICE")` | Launches active MCQ session from topic overview |
| **Question Statement** | `.markdown-body` or `[class*="MarkdownTextContainer"]` | Contains question text, formatted code blocks, and math |
| **Option Radio Labels** | `document.querySelectorAll("label.radioButtonLabel")` | Clickable option `<label>` elements (0-indexed) |
| **Submit Choice** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "SUBMIT")` | Evaluates selected radio option |
| **Advance Question** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "NEXT")` | Dynamically replaces SUBMIT button after evaluation |
| **Proceed Button** | `document.querySelector("button.StartButton-gjsfIy")` | Exits the completion summary modal (text: `"PROCEED"`) |

---

## 🔄 Autonomous Execution Protocols

### 1. Coding Practice SOP
1. **Extract Problem State**:
   Execute `python3 bridge/coding_solver.py details` to extract title, problem description, constraints, and starter code.
2. **Inspect Driver Harness**:
   Verify whether data structures (e.g., `struct Node` for Linked Lists or Trees) are pre-defined in the harness. Avoid duplicate symbol declarations that trigger compilation errors.
3. **Direct Buffer Injection**:
   Write the synthesized C++17 solution to `/tmp/solution.cpp` and inject via `python3 bridge/coding_solver.py inject /tmp/solution.cpp`. Do not simulate keystrokes.
4. **Compile & Sample Verification**:
   Execute `python3 bridge/coding_solver.py run` and verify output matches expected results.
5. **Full Suite Submission**:
   Execute `python3 bridge/coding_solver.py submit` and poll until `Testcases Passed` or `Hurray!` appears.
6. **Clean Navigation**:
   Execute `python3 bridge/coding_solver.py back` to return to syllabus (automatically clicks `"YES"` if prompted with an unsaved changes confirmation modal).

### 2. MCQ Practice SOP
1. **Fetch Question**:
   Execute `python3 bridge/mcq_solver.py question` to receive structured JSON containing the question text, 0-indexed options, and attempt progress.
2. **Select & Submit**:
   Deduce the correct 0-based option index and execute `python3 bridge/mcq_solver.py answer <index>` to select the radio label, click `"SUBMIT"`, and click `"NEXT"`.
3. **Exit Session**:
   When question 10 is reached and `isCompleted` is `true`, execute `python3 bridge/mcq_solver.py proceed` to return to syllabus.

---

## 🛠️ Tooling & Bridge CLI Reference

All automation scripts are located in `bridge/` and communicate with the persistent daemon on port `9999`:

```bash
# Daemon Management
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
python3 bridge/mcq_solver.py proceed         # Exit completion modal back to syllabus
python3 bridge/mcq_solver.py start           # Launch next practice from syllabus
```

---

## 🛡️ Edge Cases & Self-Healing Guide

| Failure Mode | Underlying Cause | Autonomous Self-Healing Action |
| :--- | :--- | :--- |
| **Port 9999 connection refused** | Bridge daemon process is not running. | Run `python3 bridge/bridge.py` in the background (`IsDaemon: true`). Verify via `curl -s http://127.0.0.1:9999/status`. |
| **Ace editor not detected** | Question page currently shows Description or Editorial tab. | Click Code tab: `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Code").click()`. |
| **Duplicate symbol compilation error** | Re-defining classes/structs already present in CCBP harness. | Check `starterCode` using `python3 bridge/coding_solver.py details` and supply only the requested method or class. |
| **Back button blocked** | Unsaved changes dialog modal is open. | Dispatch click on button with text `"YES"`: `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "YES").click()`. |
| **Target desync / page navigation** | Page navigated to a new question UUID. | Call `curl -s http://127.0.0.1:9999/reattach` to re-sync the session. |
| **Submit button missing** | Previous evaluation still running (`Processing...`). | Wait 1-2 seconds for execution to settle before triggering submission. |

---

## 📂 Repository Layout

```text
├── SKILL.md                    # Official AI Agent Skill Specification (Pure information)
├── bridge/                     # Persistent CDP WebSocket Daemon & CLI automation tools
│   ├── bridge.py               # Rule 1 compliant persistent CDP daemon (:9999)
│   ├── coding_solver.py        # Autonomous coding problem extraction & injection CLI
│   ├── eval_helper.py          # HTTP IPC client for sub-millisecond JS eval
│   ├── mcq_solver.py           # Automated MCQ extraction & submission helper
│   └── requirements.txt
├── docs/                       # Technical documentation & blueprints
│   ├── AGENT_PLAYBOOK.md       # Autonomous AI Agent Playbook, state machines & SOP
│   ├── MASTER_REPORT.md        # Technical analysis of coding practice problems
│   ├── MCQ_PRACTICE_REPORT.md  # Technical analysis of MCQ practice questions
│   └── RULES_AND_ARCHITECTURE.md # Rule 1 enforcement & CDP multiplexing mechanics
└── solutions/                  # Reference C++17 implementations
    ├── 01_stacks_and_queues/
    ├── 02_linked_lists/
    ├── 03_hashing_and_two_pointers/
    └── 04_trees_and_bst/
```

---

## 📖 Related Documentation

- ⚡ **[AI Agent Skill Guide (SKILL.md)](SKILL.md)**: Agent-executable skill document with YAML frontmatter.
- 🤖 **[Autonomous Agent Playbook (docs/AGENT_PLAYBOOK.md)](docs/AGENT_PLAYBOOK.md)**: Detailed state machine diagrams and prompt templates for AI subagents.
- 🛡️ **[Rule 1 Architecture (docs/RULES_AND_ARCHITECTURE.md)](docs/RULES_AND_ARCHITECTURE.md)**: Chrome 128+ remote debugging security analysis and persistent daemon design.

---

## 📜 License
MIT License. Created for algorithmic automation and browser engineering research.
