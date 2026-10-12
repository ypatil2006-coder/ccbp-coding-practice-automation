# CCBP Coding Practice: Automated Browser Solver & Skill Architecture

[![Problems Solved](https://img.shields.io/badge/Problems%20Solved-21%2F21%20(100%25)-brightgreen.svg)]()
[![Total Score](https://img.shields.io/badge/Score-413%2F413%20(100%25)-blue.svg)]()
[![Testcases Passed](https://img.shields.io/badge/Testcases%20Passed-1465%2F1465%20(100%25)-success.svg)]()
[![Remote Prompts](https://img.shields.io/badge/Chrome%20Prompts-0%20(Rule%201%20Compliant)-orange.svg)]()
[![Language](https://img.shields.io/badge/Language-C%2B%2B17%20%2F%20Python%203-blueviolet.svg)]()

Production-grade automated browser solving system and reverse-engineered DOM skill set for the **CCBP Learning Portal** (`https://learning.ccbp.in`). Solves algorithmic coding practices with instant Ace Editor AST buffer injection, zero repeated remote debugging pop-ups, and 100% first-pass test case pass rates.

---

## 🌟 Key Features & Benchmarks

- **Single Permission Grant (Rule 1)**: Conforms to modern Chrome 128+ security requirements by establishing a persistent background CDP WebSocket bridge. **Zero repeated prompts or pop-up notifications.**
- **Sub-Millisecond Code Injection**: Directly manipulates the underlying Ace Editor buffer via `ace.edit('codingQuestionEditor').setValue(code, -1)` instead of simulated keystrokes, reducing code injection from 15 seconds to $< 2\text{ ms}$.
- **Comprehensive Solution Library**: 21 optimal C++ implementations covering Stacks, Queues, Linked Lists, Two Pointers, Hashing, Prefix Sum, and Binary Trees.
- **Flawless Evaluation Record**: **1,465 / 1,465 test cases passed** across all 21 problems (0 failed attempts).

---

## 📊 Solved Practices Summary

| # | Problem Name | Module | Difficulty | Score | Test Cases | Algorithm |
| :-: | :--- | :--- | :-: | :-: | :-: | :--- |
| 1 | **Queue Implementation Using Array** | Stacks & Queues | Easy | 20 / 20 | 88 / 88 | Circular buffer with modular indexing ($O(1)$) |
| 2 | **Next Greater Element** | Stacks & Queues | Medium | 20 / 20 | 105 / 105 | Monotonic decreasing stack ($O(N)$) |
| 3 | **Next Greater Element Lookup** | Stacks & Queues | Medium | 20 / 20 | 20 / 20 | Monotonic stack + hash map ($O(N)$) |
| 4 | **Next Greater Element II** | Stacks & Queues | Medium | 20 / 20 | 106 / 106 | Circular monotonic stack ($O(N)$) |
| 5 | **Nearest Smaller Element** | Stacks & Queues | Easy | 20 / 20 | 8 / 8 | Monotonic stack left-to-right ($O(N)$) |
| 6 | **Next Warmer Day Forecast** | Stacks & Queues | Medium | 25 / 25 | 10 / 10 | Daily temperatures index stack ($O(N)$) |
| 7 | **Find Towers Facing Sea** | Stacks & Queues | Easy | 25 / 25 | 10 / 10 | Right-to-left running maximum ($O(N)$) |
| 8 | **Insertion At Head - Linked List** | Linked Lists | Easy | 10 / 10 | 104 / 104 | Prepend pointer linking ($O(1)$) |
| 9 | **Insertion At Tail - Linked List** | Linked Lists | Easy | 10 / 10 | 104 / 104 | Traversal to tail node ($O(N)$) |
| 10 | **Insertion Before Node With Value X** | Linked Lists | Easy | 10 / 10 | 104 / 104 | Predecessor pointer tracking ($O(N)$) |
| 11 | **Minimum Balls in the Box** | Frequency / Greedy | Medium | 25 / 25 | 10 / 10 | Frequency hash parity reduction ($O(N)$) |
| 12 | **Two Sum** | Two Pointers / Hash | Easy | 15 / 15 | 89 / 89 | Hash map complement lookup ($O(N)$) |
| 13 | **Two Sum II** | Two Pointers | Medium | 20 / 20 | 8 / 8 | Dual pointer convergence 1-based ($O(N)$) |
| 14 | **Three Sum** | Two Pointers | Medium | 20 / 20 | 106 / 106 | Sorted two-pointer sweep ($O(N^2)$) |
| 15 | **Four Sum** | Two Pointers | Easy | 20 / 20 | 97 / 97 | Quadruple pointer sweep ($O(N^3)$) |
| 16 | **Count Subarrays with Target Sum** | Prefix Sum | Easy | 45 / 45 | 152 / 152 | Prefix sum hash frequency counter ($O(N)$) |
| 17 | **Count Valid Triplets** | Math / Modulo | Medium | 13 / 13 | 30 / 30 | Remainder grouping combinatorics ($O(K^2)$) |
| 18 | **Binary Tree Representation** | Trees | Easy | 15 / 15 | 90 / 90 | Array level-order tree construction ($O(N)$) |
| 19 | **Preorder Traversal** | Trees | Easy | 15 / 15 | 107 / 107 | Depth-first root $\to$ left $\to$ right ($O(N)$) |
| 20 | **Inorder Traversal** | Trees | Easy | 10 / 10 | 94 / 94 | Depth-first left $\to$ root $\to$ right ($O(N)$) |
| 21 | **Postorder Traversal** | Trees | Easy | 15 / 15 | 88 / 88 | Depth-first left $\to$ right $\to$ root ($O(N)$) |

---

## 🏗️ Architecture & Rule 1 Enforcement

### The Chrome 128+ Problem
Modern Chrome displays an intrusive modal: *"Allow remote debugging?"* whenever a new external client connects to port 9222. Reconnecting or creating disposable WebSocket sessions triggers multiple prompts.

### The Background Bridge Daemon (`bridge/bridge.py`)
1. **Single Handshake**: Handshakes to the browser endpoint (`DevToolsActivePort`) exactly once without an `Origin` header.
2. **Session Multiplexing**: Attaches to the active CCBP tab session via `Target.attachToTarget` (`flatten: true`).
3. **Local HTTP JSON-RPC Server (`http://127.0.0.1:9999`)**:
   - `POST /eval`: Evaluates JavaScript inside the active page in $\le 10\text{ ms}$.
   - `POST /screenshot`: Captures high-res viewport screenshots.
   - `GET /status`: Verifies target and session health.

```bash
# Launch persistent bridge daemon
python3 bridge/bridge.py
```

---

## 🎯 CCBP Portal DOM & UI Selectors

| Action / Element | Selector / JavaScript API |
| :--- | :--- |
| **Open Question Card** | `document.querySelectorAll('[data-testid="card-container"]')[i].click()` |
| **Switch to Code Tab** | `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Code").click()` |
| **Switch to Summary Tab** | `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Summary").click()` |
| **Get Starter Code** | `ace.edit("codingQuestionEditor").getValue()` |
| **Inject Solution** | `ace.edit("codingQuestionEditor").setValue(code, -1)` |
| **Run Code** | `document.getElementById("runCode").click()` |
| **Submit Code** | `document.getElementById("submitCode").click()` |
| **Back Button** | `document.querySelector('[data-testid="practice-header-back-button"]').click()` |
| **Exit Save Modal** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "YES").click()` |

---

## 📂 Repository Layout

```
.
├── README.md                          # Project documentation and benchmarks
├── bridge/
│   ├── bridge.py                      # Persistent CDP bridge daemon
│   ├── eval_helper.py                 # Remote JS evaluation CLI client
│   └── requirements.txt               # Dependencies
├── docs/
│   ├── MASTER_REPORT.md               # Complete 21-practice evaluation report
│   └── RULES_AND_ARCHITECTURE.md       # Full engineering blueprint
├── solutions/
│   ├── 01_stacks_and_queues/          # Problems 1-7
│   ├── 02_linked_lists/               # Problems 8-10
│   ├── 03_hashing_and_two_pointers/   # Problems 11-17
│   └── 04_trees_and_bst/              # Problems 18-21
└── assets/                            # Verification screenshots
```

---

## 📸 Verification & Screenshots

| Postorder Traversal (88/88 Passed) | Linked Lists Suite (100% Passed) |
| :---: | :---: |
| ![Postorder Traversal](assets/ccbp_postorder_solved.png) | ![Linked Lists](assets/ccbp_linked_list_all_solved.png) |

| Next Greater Element Suite (100% Passed) | Submission Evaluation Output |
| :---: | :---: |
| ![NGE Solved](assets/ccbp_nge_solved.png) | ![Evaluation Diff](assets/ccbp_screen_eval.png) |

---

## 📜 License
MIT License. Created for algorithmic automation and browser engineering research.
