# Sprint 1: Sandbox Architecture & Variables (Weeks 1 & 2)

**Theme:** Initialize the Python learning sandbox, database schema, and Module 1: Variables & Expressions (AP CSA Unit 1 equivalent).

---

## 📋 Iteration Checklist

### Week 1: Wasm Pyodide Sandbox & Telemetry Schemas
*   [x] **1. Python Assignment & Submission Models**
    *   Create models `PythonAssignment` (storing prompt, starter code, test suites) and `PythonSubmission` (storing code submitted by student, output, duration, and test results).
*   [x] **2. WebAssembly Pyodide Integration**
    *   Setup Pyodide compiler script inside a Web Worker. Establish postMessage API to send user code and retrieve print console buffers.
*   [x] **3. Terminal Output Panel**
    *   Integrate Xterm.js library into Next.js workspace to stream stdout and stderr outputs.

### Week 2: Module 1: Variables & Expression Evaluation (AP CSA Unit 1)
*   [x] **4. Module 1 Lessons & Autograding Tests**
    *   Build 5 core learning exercises (with detailed curriculum helper explanations in prompts) and 1 summative unit assessment:
        *   `var_assignment`: Storing user input strings and integer calculations.
        *   `arithmetic_ops`: Calculating sums, products, and modulo checks.
        *   `type_casting`: Converting strings to integers/floats using `int()` and `float()`.
        *   `string_concat`: Formatted printing using f-strings.
        *   `input_math`: Capturing console inputs and performing float math operations.
        *   `unit1_assessment: Summative Assessment combining variables, casting, formatting, and arithmetic calculations.`
    *   Implement client-side unit test runners executing assertions in Wasm.
*   [x] **5. Progress Telemetry Logging**
    *   Wire API client to dispatch results (`python_run_code`, `python_submit_solution`).
