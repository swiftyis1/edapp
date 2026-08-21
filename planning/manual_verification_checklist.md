# Manual Verification Checklist: Module Navigation & Wasm Python IDE

This document contains step-by-step instructions for testing the dynamic landing page and python compiler integration in the local environment.

## Phase 1: Authentication & Portal Landing Page

1. **Clean state verification**:
   * Open Developer Tools in your browser (F12) -> Application -> Local Storage.
   * Clear local storage.
   * Refresh `http://localhost:3000`. Verify you see the login portal with the title "Welcome to Swift Science".
2. **Registration test**:
   * Click "Register here".
   * Fill out the form with a test username (`test_user_student`), password (`Password123`), and role `Student`.
   * Click "Create Account".
3. **Module Landing Page**:
   * Verify you land on the portal selector page showing two cards: **Swift Science** and **Swift CS**.
   * Verify the dynamic header title shows **Swift Portal** with the description "OAS Science & Computer Science Adaptive Assessment".

---

## Phase 2: Swift CS Environment (Student View)

1. **Enter Suite**:
   * Click "Enter Coding Suite" on the Swift CS card.
   * Verify the header updates: Title becomes **Swift CS** and subtitle becomes "Python Programming & Google Classroom Sync".
   * Verify the "🏠 Switch Module" button is visible in the header.
2. **Interpreter Initialization**:
   * Watch the bottom **Output Terminal** panel.
   * Verify it displays initialization statements ending in `✓ Python 3.11 Interpreter Ready!`.
3. **Dynamic Assignment Navigation**:
   * Expand the **1. Variables & Expressions** module.
   * Verify a nested list of assignments is rendered underneath (e.g. *Python Division*, *Variable Swapping*, *Modulo Math*, etc.).
   * Click on **Python Division**. Verify the workspace prompt updates to the custom instructions: "Define variable x = 45 and y = 15. Perform division (x / y) and print the output using print()."
   * Verify the editor loads the starter code:
     ```python
     x = 45
     y = 15
     # Write your code to divide x by y and print the result
     ```
4. **Interpreter Execution & Safety Filters**:
   * Click the "Run Code" button. Verify the output terminal displays the computed value (e.g., `3.0`).
   * Test code compilation safety limits:
     * Write an infinite loop: `while True: pass`. Click "Run Code". Verify the execution block warning prints.
     * Write a heavy loop: `for i in range(2000000): pass`. Click "Run Code". Verify iteration safety block warning prints.
5. **Database-backed Grading**:
   * With the correct code in the editor, click **Submit & Grade**.
   * Observe the button text transitions to `Grading...` and a server-side request checks assertions.
   * Verify a success message pops up: `✓ Solution submitted successfully! Score: 100`.
   * Verify a green badge labeled `✓ Passed & Submitted` appears on the right side of the workspace header.
   * Verify the assignment row in the sidebar shows a checkmark symbol (`✅` instead of `📝`).
   * Choose another assignment (e.g., **Variable Swapping**). Verify the workspace loads its respective starter template.

---

## Phase 3: Swift CS Google Classroom Sync (Teacher View)

1. **Role Toggle**:
   * Switch the simulator view to **Teacher** in the header.
   * Verify the Swift CS teacher dashboard is displayed.
2. **Google Classroom Link**:
   * Click "🔗 Link Google Classroom".
   * A simulated sync window should pop up. Click on one of the mock courses (e.g. `AP Computer Science A - Section 1`).
   * Verify the sync progress logs run and display imported student details:
     `✓ Success: Imported course AP Computer Science A - Section 1 with 12 active students.`
   * Verify the table lists mock student rows (Alex Rivera, Blake Henderson, Daniela Garcia).
3. **Grade Pushing Sync**:
   * Click "Sync Grades to Google Classroom".
   * Verify sync logs process and complete with:
     `✓ Updated 8 student draft grades in Google Classroom!`

---

## Phase 4: Module Swapping

1. **Portal Switch**:
   * Click the "🏠 Switch Module" button in the header.
   * Verify it returns you to the home selection portal.
2. **Enter Swift Science**:
   * Click "Enter Science Suite" on the Swift Science card.
   * Verify the header title updates to **Swift Science** and the physical science/biology simulators load.
   * Click "🏠 Switch Module" again to verify you can toggle back and forth smoothly.

---

## Phase 5: Rate Limiting & Execution Safety Limits

1. **Infinite Loop Protection**:
   * Write an infinite loop in the editor:
     ```python
     while True:
         print("Looping")
     ```
   * Click "Run Code".
   * Verify execution is blocked and the terminal prints:
     `⚠️ Execution Blocked: Detected potential infinite 'while' loop. Please include a 'break' or exit condition to avoid freezing your browser.`

2. **Iteration Safety Limits**:
   * Write a bounded loop with a massive range:
     ```python
     for i in range(10000000):
         pass
     ```
   * Click "Run Code".
   * Verify execution is blocked and the terminal prints:
     `⚠️ Execution Blocked: Range iteration limit exceeded (max 1,000,000). Please scale down iteration bounds.`

3. **Backend Rate Limiter (45 reqs/min)**:
   * Rapidly trigger page reloads, logins, or database requests.
   * Verify the Django backend throttles the request rate if it exceeds 45 requests in a 60-second window, responding with HTTP 429 (Too Many Requests).

