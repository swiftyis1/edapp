# Sprint 2: Editor Integration & Control Flow (Weeks 3 & 4)

**Theme:** Monaco Editor setup, auto-grading runner, and Module 2: Selection & Iteration (AP CSA Unit 2 equivalent).

---

## 📋 Iteration Checklist

### Week 3: Monaco Coding Editor & Auto-Grading Framework
*   [x] **1. Next.js Monaco Editor Workspace**
    *   Integrate Monaco Editor component with Python language bindings, highlighting, autocomplete, and auto-indentation rules.
*   [x] **2. Client-Side Test Runner**
    *   Build standard testing wrapper that loads hidden assertions, intercepts student function prints, and evaluates variable states in Pyodide.
*   [x] **3. Infinite Loop Timeout Interceptor**
    *   Calibrate the Web Worker execution watchdog timer. Stop code runs and raise `TimeoutError` if thread doesn't respond in 5 seconds.

### Week 4: Module 2: Selection & Iteration (AP CSA Unit 2)
*   [x] **4. Module 2 Lessons & Autograding Tests**
    *   Build 5 core learning exercises (with detailed curriculum helper explanations in prompts) and 1 summative unit assessment:
        *   `if_statement`: Basic comparison testing.
        *   `logical_operators`: Combining conditions using `and`, `or`, `not`.
        *   `while_loop`: Counter loops and condition validation.
        *   `for_loop`: Iterating range sequences.
        *   `nested_loop`: Generating 2D coordinate patterns.
        *   `unit2_assessment: Summative Assessment combining selection statements, while/for loops, and nested loop patterns.`
    *   Configure test suites in the database verifying correct conditional structures are utilized.
