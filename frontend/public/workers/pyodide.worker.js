let pyodide = null;

// Initialize Pyodide Wasm environment inside Web Worker
async function initPyodide() {
  try {
    self.importScripts("https://fastly.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");
    pyodide = await self.loadPyodide({
      indexURL: "https://fastly.jsdelivr.net/pyodide/v0.25.0/full/"
    });
    self.postMessage({ type: "status", status: "ready" });
  } catch (err) {
    self.postMessage({ type: "status", status: "error", error: err.message });
  }
}

initPyodide();

self.onmessage = async (e) => {
  const { type, code, testSuite } = e.data;
  if (!pyodide) {
    self.postMessage({ type: "error", error: "Python interpreter is not ready yet." });
    return;
  }

  if (type === "run") {
    try {
      pyodide.globals.set("__student_code__", code);
      pyodide.runPython(`
import sys
import io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
      `);
      await pyodide.runPythonAsync(code);
      const stdout = pyodide.runPython("sys.stdout.getvalue()");
      const stderr = pyodide.runPython("sys.stderr.getvalue()");
      self.postMessage({
        type: "run_success",
        stdout: stdout,
        stderr: stderr
      });
    } catch (err) {
      self.postMessage({
        type: "run_error",
        error: err.message
      });
    }
  } else if (type === "grade") {
    try {
      // 1. Clear globals first to avoid cross-test pollution
      pyodide.runPython("globals().clear()");

      // 2. Set up standard output capturing
      pyodide.runPython(`
import sys
import io
import builtins
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
def default_input(*args):
    return "0"
builtins.input = default_input
      `);

      // 3. Run the student's code
      pyodide.globals.set("__student_code__", code);
      await pyodide.runPythonAsync(code);
      const mainStdout = pyodide.runPython("sys.stdout.getvalue()");
      const mainStderr = pyodide.runPython("sys.stderr.getvalue()");

      // 4. Run assertion tests
      let assertionsPassed = true;
      const assertionResults = [];
      const assertions = testSuite.assertions || [];
      for (const assertion of assertions) {
        let pass = false;
        let errMsg = "";
        try {
          const result = pyodide.runPython(assertion.code);
          if (result === false) {
            throw new Error("Assertion evaluated to False");
          }
          pass = true;
        } catch (e) {
          pass = false;
          errMsg = e.message;
        }
        if (!pass) assertionsPassed = false;
        assertionResults.push({
          code: assertion.code,
          msg: assertion.msg,
          passed: pass,
          error: errMsg
        });
      }

      // 5. Run IO tests
      let ioPassed = true;
      const ioResults = [];
      const ioTests = testSuite.io_tests || [];
      for (const test of ioTests) {
        const inputsList = JSON.stringify(test.inputs);
        pyodide.runPython(`
import builtins
inputs = ${inputsList}
input_index = 0
def mock_input(*args):
    global input_index
    if input_index < len(inputs):
        val = inputs[input_index]
        input_index += 1
        return val
    raise EOFError("No more inputs")
builtins.input = mock_input
        `);
        pyodide.runPython(`
import sys
import io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
        `);
        await pyodide.runPythonAsync(code);
        const testStdout = pyodide.runPython("sys.stdout.getvalue()").trim();
        const expected = test.expected_output.trim();
        const testPass = testStdout.includes(expected);
        if (!testPass) ioPassed = false;
        ioResults.push({
          inputs: test.inputs,
          expected: expected,
          actual: testStdout,
          passed: testPass
        });
      }

      const allPassed = assertionsPassed && ioPassed;
      self.postMessage({
        type: "grade_success",
        passed: allPassed,
        score: allPassed ? 100 : 0,
        mainStdout: mainStdout,
        mainStderr: mainStderr,
        assertionResults: assertionResults,
        ioResults: ioResults
      });
    } catch (err) {
      self.postMessage({
        type: "grade_error",
        error: err.message
      });
    }
  }
};
