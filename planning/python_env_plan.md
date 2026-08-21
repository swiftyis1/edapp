# Product Master Plan: Python Learning Environment & Google Classroom Sync

This document establishes the product vision, architecture, curriculum alignment, AI constraints, and key design decisions for building the **Python Learning Environment** with integrated **Google Classroom Gradebook synchronization**.

---

## 1. Product Scope & Core Vision

The **Python Learning Environment** is an expansion of the Swift Science platform, designed to teach computer science concepts using Python while integrating with school learning management systems. 

### Key Features
1. **Interactive In-Browser Editor & Terminal**: A full coding environment powered by **Pyodide** (Python compiled to WebAssembly) running natively in the client browser, completely eliminating the need for server-side code execution.
2. **Automated Unit Testing & Grading**: A client-side testing framework that evaluates student code submissions using custom test assertions and publishes telemetry results.
3. **SSO and Roster Ingestion**: Teachers can import their course roster directly from Google Classroom using OAuth2.
4. **Coursework Mapping**: Allows teachers to link specific in-app Python challenges to corresponding coursework items on their Google Classroom stream.
5. **Direct Grade Syncing**: Allows teachers to push grades (points, progress percentages) directly from the platform gradebook into the student's submission record on Google Classroom as a `draftGrade` or `assignedGrade`.

---

## 2. Component Architecture & Data Flow

The system runs Python code client-side, records submission telemetry to the Django database, and synchronizes grade records with Google Classroom using Google APIs.

```
+-----------------------------------------------------------------------------------------+
|                                    Next.js Frontend                                     |
|                                                                                         |
|  +------------------------+      Run Code       +------------------------------------+  |
|  |     Monaco Editor      |-------------------->|            Pyodide Wasm            |  |
|  |  (Student Python Code) |                     |  (In-Browser Code Execution Unit)  |  |
|  +------------------------+                     +-----------------+------------------+  |
|              ^                                                    |                     |
|              | Save Code & Telemetry                              | Capture Output      |
|              |                                                    v                     |
|              |                                  +------------------------------------+  |
|              |                                  |        Xterm.js Terminal UI        |  |
|              |                                  |   (stdout/stderr/stdin display)    |  |
|              |                                  +------------------------------------+  |
|              |                                                    |                     |
|              |                                                    | Runs Unit Tests     |
|              v                                                    v                     |
|  +------------------------+   POST Telemetry    +------------------------------------+  |
|  |   API Client Service   |-------------------->|      Telemetry & Score Logger      |  |
|  +------------------------+                     +------------------------------------+  |
+--------------+----------------------------------------------------+---------------------+
               |                                                    |
               | OAuth2 & Sync Requests                             | Fetch rosters & grades
               v                                                    v
+--------------v----------------------------------------------------+---------------------+
|                                     Django Backend                                      |
|                                                                                         |
|   +-----------------------+   Read/Write   +---------------------------------------+    |
|   |   Google OAuth View   |<-------------->|       Google Classroom API Sync       |    |
|   |  (Token Ingestion)    |                |      (Rosters, Coursework, Grades)    |    |
|   +-----------------------+                +-------------------+-------------------+    |
+----------------------------------------------------------------|------------------------+
                                                                 |
                                                                 | Push Grades
                                                                 v
                                                      +----------+-----------+
                                                      | Google Classroom API |
                                                      +----------------------+
```

### Data Flow Execution Steps
1. **Writing & Running Code**: The student types Python code in the in-app Monaco Editor. Clicking "Run Code" executes the program inside the WebAssembly Pyodide sandbox. Output is piped to a mock console terminal (Xterm.js).
2. **Automated Testing**: Clicking "Submit" triggers a local test runner. Pyodide executes a custom testing script containing standard assertions against the student's functions and variable states.
3. **Telemetry Ingestion**: The execution details (code, correctness status, error counts, execution duration) are POSTed to the Django backend database models (`StudentSubmission` and `TelemetryEvent`).
4. **Google Classroom Sync**:
   * The teacher authenticates via Google OAuth2. The backend stores the credentials (`OAuth2Credential`).
   * The teacher fetches their Google Classroom course list and imports a selected course.
   * Student emails are mapped between our database and Google Classroom user IDs.
   * The teacher maps Python assignments to Google Coursework IDs.
   * Clicking "Sync Grades" calls Google's `courses.courseWork.submissions.patch` API to save student grades as `draftGrade` or `assignedGrade` values inside Google Classroom.

---

## 3. AP Computer Science A Curriculum Alignment Mapping

The Python Learning Environment covers concepts equivalent to the **AP Computer Science A** curriculum and the **Oklahoma Academic Standards for Computer Science (OAS-CS)**, adapted for Python:

| AP CSA Unit (Java) | Python Learning Environment Course Module | Target Skills & Concept Coverage |
| :--- | :--- | :--- |
| **Unit 1: Primitive Types** | **Module 1: Variables & Expression Evaluation** | Python basic data types (`int`, `float`, `str`, `bool`), arithmetic operators, input capture, and type conversions. |
| **Unit 2: Selection & Iteration** | **Module 2: Control Flow & Loops** | Boolean logic, conditional statements (`if`, `elif`, `else`), logical operators, and loop structures (`while`, `for`, `break`, `continue`). |
| **Unit 1 & 2: Methods** | **Module 3: Functions, Modules & Scoping** | Declaring functions (`def`), parameters, default arguments, return values, variable scope (local vs global), and importing libraries. |
| **Unit 3: Class Creation** | **Module 4: Object-Oriented Programming (OOP)** | Designing classes, properties, constructors (`__init__`), instance methods, self-reference (`self`), and encapsulation. |
| **Unit 3: Class Creation** | **Module 5: Inheritance & Polymorphism** | Parent/Child class hierarchies, overriding parent methods, and using polymorphism in program design. |
| **Unit 4: Data Collections** | **Module 6: 1D Lists & Sequence Operations** | Python lists, sequence slicing, built-in list methods (append, pop, insert, sort), list traversals, and list comprehensions. |
| **Unit 4: Data Collections** | **Module 7: 2D Lists & Grids** | Nested lists, representing grid coordinates, and nested loop traversals. |
| **Unit 4: Data Collections** | **Module 8: Searching & Sorting Algorithms** | Implementing linear search, binary search, bubble sort, selection sort, and insertion sort algorithms. |
| **Unit 4: Recursion** | **Module 9: Recursion & Advanced Sorts** | Writing recursive methods, base cases, tracking the call stack, and implementing merge sort. |
| **Unit 3: Social/Ethical Impact**| **Module 10: Social, Ethical, & Security Auditing** | Data privacy rules (FERPA), software testing rigor, and computing's societal impacts. |

---

## 4. AI & WebAssembly Limitations

Developing an educational IDE in WebAssembly poses technical constraints that we must account for during planning:

1. **Single-Thread UI Blocking**:
   * *Problem*: Pyodide runs on the main browser thread by default. Long-running code or infinite loops (e.g., `while True: pass`) will freeze the tab interface.
   * *Mitigation*: We will execute Pyodide code inside a **Web Worker**. The main Next.js thread communicates with the Web Worker via message passing (`postMessage`), allowing us to enforce a **5-second execution timeout** and terminate the worker if it hangs.
2. **Network Payload & Performance on School Devices**:
   * *Problem*: Loading the Pyodide WebAssembly package, standard libraries, and editor assets requires ~10-15MB of transfer. Low-powered school Chromebooks with poor internet connections can experience slow initialization times.
   * *Mitigation*: Leverage **Service Workers** to cache Pyodide, Monaco Editor, and curriculum JSON payloads locally. Once loaded, the coding environment can compile and run code offline.
3. **Google Classroom API Quota Limits**:
   * *Problem*: Google Classroom API enforces strict rate limits. Iterating through large classroom rosters (e.g., syncing grades for multiple classes of 30+ students) using individual requests can hit API quotas.
   * *Mitigation*: Implement batch request updates using the Google API batch system or queue sync requests inside a backend Celery pipeline to throttled rates.
4. **OAuth2 Security & App Verification**:
   * *Problem*: Writing grades via API requires sensitive OAuth scopes (`.../auth/classroom.coursework.students`). Google requires strict security audits and app verification for production apps requesting these scopes.
   * *Mitigation*: While in development/pilot stages, the app remains in "Testing" mode on the Google Cloud Console, limiting access to pre-registered test accounts. Our sprints include preparing developer logs for Google's verification checklist.

---

## 5. Architectural Decision Log

This log tracks architectural trade-offs resolved during the design phase:

### Decision 1: Pyodide (WebAssembly) vs. Server-Side Execution (Docker/Celery)
* **Status**: `Approved`
* **Choice**: Pyodide (Wasm) execution.
* **Rationale**: Server-side execution of untrusted user code requires sandboxed Docker containers, heavy server scaling to support concurrent student runs, and deep security monitoring. Running Python inside the client's WebAssembly sandbox is free, scales infinitely, and cannot compromise backend servers.

### Decision 2: Google Classroom API vs. LTI 1.3 Integration
* **Status**: `Approved`
* **Choice**: Direct Google Classroom API.
* **Rationale**: While LTI 1.3 is a standardized protocol supporting multiple platforms (Canvas, Blackboard), Google Classroom's LTI implementation is complex and requires Google Workspace Domain Administrator intervention. Direct Google API integration allows individual teachers to authorize and sync rosters with a simple Google login. LTI 1.3 is deferred to the future roadmap.

### Decision 3: Monaco Editor vs. Simple Textarea Editor
* **Status**: `Approved`
* **Choice**: Monaco Editor (with fallback).
* **Rationale**: Learning Python requires proper indentation, syntax coloring, and immediate bracket completion. Monaco Editor provides a VS Code-like coding experience. On ultra-low-powered mobile devices or old browsers where Monaco crashes, the app will fall back to a styled textarea with basic auto-tabbing.
