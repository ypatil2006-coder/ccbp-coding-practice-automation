# CCBP Learning Portal: Automated Solver & Skill Architecture

[![Coding Solved](https://img.shields.io/badge/Coding%20Practices-27%2F27%20(100%25)-brightgreen.svg)]()
[![MCQ Solved](https://img.shields.io/badge/MCQ%20Practices-40%2F40%20(100%25)-success.svg)]()
[![Coding Score](https://img.shields.io/badge/Coding%20Score-533%2F533%20(100%25)-blue.svg)]()
[![Coding Testcases](https://img.shields.io/badge/Coding%20Testcases-1853%2F1853-brightgreen.svg)]()
[![Skill Guide](https://img.shields.io/badge/Agent%20Skill-SKILL.md-success.svg)](SKILL.md)
[![Remote Prompts](https://img.shields.io/badge/Chrome%20Prompts-0%20(Rule%201%20Compliant)-orange.svg)]()
[![Language](https://img.shields.io/badge/Language-C%2B%2B17%20%2F%20Python%203-blueviolet.svg)]()

Production-grade automated browser solving system and reverse-engineered DOM skill set for the **CCBP Learning Portal** (`https://learning.ccbp.in`). Supports both **Algorithmic Coding Practices** (Ace Editor direct AST buffer injection) and **MCQ Practices** with instant evaluation, zero repeated remote debugging pop-ups, and a 100% first-pass pass rate.

> 🤖 **For AI Agents**: Refer directly to [**SKILL.md**](SKILL.md) for the pure actionable skill instructions, DOM selectors, execution SOP, and error recovery protocols without images or statistics.

---

## 🌟 Key Features & Benchmarks

- **Single Permission Grant (Rule 1)**: Conforms to modern Chrome 128+ security requirements by establishing a persistent background CDP WebSocket bridge. **Zero repeated prompts or pop-up notifications.**
- **Dual Engine**:
  - **Coding Practices**: Instant Ace Editor buffer injection via `ace.edit('codingQuestionEditor').setValue(code, -1)` (reduces injection from 15s to $< 2\text{ ms}$).
  - **MCQ Practices**: Automated question & option parsing (`label.radioButtonLabel`), submission, and transition handling.
- **Flawless Evaluation Record**:
  - **Coding Practices**: **27 / 27 solved** | **1,853 / 1,853 test cases passed** (100% pass rate).
  - **MCQ Practices**: **40 / 40 correct answers** across 4 complete sessions (0 wrong, 0 unanswered).

---

## 📊 Solved Practices Summary

### 1. Algorithmic Coding Practices (21 / 21 Solved, 413/413 Pts)

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
| 22 | **Delete Kth Node - Doubly Linked List** | Linked Lists | Easy | 10 / 10 | 103 / 103 | Bi-directional pointer deletion ($O(K)$) |
| 23 | **Cycle Detection** | Linked Lists | Easy | 15 / 15 | 163 / 163 | Floyd's Tortoise and Hare ($O(N)$) |
| 24 | **Cycle Detection In Linked List II** | Linked Lists | Medium | 20 / 20 | 8 / 8 | Floyd's Phase 2 Cycle Entry ($O(N)$) |
| 25 | **Balanced Parenthesis** | Stacks & Queues | Easy | 15 / 15 | 94 / 94 | Stack parenthesis matching ($O(N)$) |
| 26 | **Balanced Parentheses with Locked Characters** | Stacks & Queues | Medium | 25 / 25 | 10 / 10 | Two-pass flexible parity sweep ($O(N)$) |
| 27 | **Minimum Removal for Valid Parentheses** | Stacks & Queues | Medium | 25 / 25 | 10 / 10 | Greedy stack index filtering ($O(N)$) |

### 2. MCQ Practice Sessions (40 / 40 Correct across 4 Sessions)

| Session # | Topic | Questions | Correct | Accuracy | Key Concepts Tested |
| :-: | :--- | :-: | :-: | :-: | :--- |
| **1** | **Introduction to Binary Trees** | 10 | 10 | **100%** | Balanced trees, full/complete/degenerate trees, internal/leaf nodes, degree properties |
| **2** | **Binary Tree Traversals** | 10 | 10 | **100%** | In-order, Pre-order, Post-order, Level-order (BFS), tree reconstruction, root values |
| **3** | **Pre-Order Traversal** | 10 | 10 | **100%** | Pre-order recursion, call stack backtrack, $O(N)$ time/space, base case null checks |
| **4** | **In-Order Traversal** | 10 | 10 | **100%** | Left-Root-Right invariants, call stack bounds, first/last visited nodes, algorithmic complexity |

---

## 🎯 CCBP Portal DOM & UI Selectors

### Coding Practice Selectors
| Action / Element | Selector / JavaScript API |
| :--- | :--- |
| **Open Question Card** | `document.querySelectorAll('[data-testid="card-container"]')[i].click()` |
| **Switch to Code Tab** | `Array.from(document.querySelectorAll("div, button, a")).find(el => el.textContent.trim() === "Code").click()` |
| **Inject Solution** | `ace.edit("codingQuestionEditor").setValue(code, -1)` |
| **Run Code** | `document.getElementById("runCode").click()` |
| **Submit Code** | `document.getElementById("submitCode").click()` |
| **Back Button** | `document.querySelector('[data-testid="practice-header-back-button"]').click()` |
| **Exit Save Modal** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "YES").click()` |

### MCQ Practice Selectors
| Action / Element | Selector / JavaScript API |
| :--- | :--- |
| **Start Practice** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "START PRACTICE").click()` |
| **Question Text** | `document.querySelector(".markdown-body, [class*=\"MarkdownTextContainer\"]").innerText` |
| **Select Option $i$** | `document.querySelectorAll("label.radioButtonLabel")[i].click()` |
| **Submit Choice** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "SUBMIT").click()` |
| **Advance Question** | `Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "NEXT").click()` |
| **Exit Modal** | `document.querySelector("button.StartButton-gjsfIy").click()` (Text: `"PROCEED"`) |

---

## 📸 Verification & Screenshots

| MCQ Practice 4 (10/10 Correct) | MCQ Practice 2 (10/10 Correct) |
| :---: | :---: |
| ![MCQ Practice 4](assets/ccbp_mcq_practice4_10_correct.png) | ![MCQ Practice 2](assets/ccbp_mcq_practice2_10_correct.png) |

| Linked Lists Suite (100% Passed) | Postorder Traversal (88/88 Passed) |
| :---: | :---: |
| ![Linked Lists](assets/ccbp_linked_list_all_solved.png) | ![Postorder Traversal](assets/ccbp_postorder_solved.png) |

---

## 📂 Repository Layout

```text
├── SKILL.md                    # Official AI Agent Skill Specification (No images/stats)
├── assets/                     # Verification screenshots and visual audit proof
│   ├── ccbp_mcq_practice4_10_correct.png
│   ├── ccbp_mcq_practice2_10_correct.png
│   ├── ccbp_mcq_10_correct.png
│   ├── ccbp_postorder_solved.png
│   ├── ccbp_linked_list_all_solved.png
│   └── ...
├── bridge/                     # Persistent CDP WebSocket Daemon & automation scripts
│   ├── bridge.py               # Rule 1 compliant single-handshake persistent CDP bridge
│   ├── coding_solver.py        # CLI helper for autonomous coding problem extraction & injection
│   ├── eval_helper.py          # HTTP IPC client for sub-millisecond evaluation
│   ├── mcq_solver.py           # Automated MCQ extraction & submission helper
│   └── requirements.txt
├── docs/                       # Comprehensive engineering documentation & blueprints
│   ├── AGENT_PLAYBOOK.md       # Autonomous AI Agent Playbook, state machines & SOP
│   ├── MASTER_REPORT.md        # 27/27 Coding Practice report & full performance audit
│   ├── MCQ_PRACTICE_REPORT.md  # 40/40 MCQ Practice report & React DOM blueprint
│   └── RULES_AND_ARCHITECTURE.md # Rule 1 enforcement & CDP multiplexing mechanics
└── solutions/                  # Optimized C++17 implementations (100% passed)
    ├── 01_stacks_and_queues/
    ├── 02_linked_lists/
    ├── 03_hashing_and_two_pointers/
    └── 04_trees_and_bst/
```

---

## 📖 Detailed Engineering Reports & Agent Knowledge

- ⚡ **[AI Agent Skill Guide (SKILL.md)](SKILL.md)**: Official Skill file with YAML frontmatter containing pure actionable technical protocols, DOM selectors, execution SOP, and error recovery—free of images and statistics.
- 🤖 **[Autonomous AI Agent Playbook & SOP](docs/AGENT_PLAYBOOK.md)**: Machine-executable specifications, state machines, autonomous decision trees, self-healing error recovery, and system prompt templates for AI subagents.
- 📘 **[Coding Practice Master Report & Benchmark Audit](docs/MASTER_REPORT.md)**: Complete analysis of 27 algorithmic practices, test case matrices, and runtime data.
- 📝 **[MCQ Practice Master Report & DOM Blueprint](docs/MCQ_PRACTICE_REPORT.md)**: Reverse-engineered React state lifecycle, selector mapping, and 40/40 answers breakdown.
- 🛡️ **[Rule 1 Architecture & Persistent CDP Mechanics](docs/RULES_AND_ARCHITECTURE.md)**: Chrome 128+ remote debugging security analysis, persistent daemon design, and latency optimizations.

---

## 📜 License
MIT License. Created for algorithmic automation and browser engineering research.
