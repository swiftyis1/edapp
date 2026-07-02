"use client";

import React, { useState, useEffect } from "react";

// Standard Complementary Pairing Map (DNA -> mRNA)
const COMPLEMENTARY_MAP = {
  T: "A",
  A: "U",
  C: "G",
  G: "C",
};

// Standard Nucleotide Color Scheme (Vibrant HSL Gradients)
const BASE_COLORS = {
  A: "from-rose-500 to-pink-600 shadow-rose-500/20 text-white",
  U: "from-amber-500 to-orange-600 shadow-amber-500/20 text-white",
  C: "from-teal-400 to-emerald-600 shadow-teal-500/20 text-white",
  G: "from-indigo-500 to-purple-600 shadow-indigo-500/20 text-white",
  default: "bg-zinc-800 border-zinc-700 text-zinc-400",
};

export default function Home() {
  // App Role View: 'student' (DNA Sandbox) vs 'teacher' (Dashboard Stub)
  const [role, setRole] = useState("student");

  // DNA Template Sequence (B.LS1.1 Target)
  const templateDNA = ["T", "A", "C", "G", "G", "C", "T", "T", "A"];
  
  // Game states
  const [mrnaChain, setMrnaChain] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [errors, setErrors] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [isCompleted, setIsCompleted] = useState(false);
  const [feedbackLog, setFeedbackLog] = useState([]);

  // Telemetry dispatch logs (stored locally for preview in Task 3)
  const [dispatchedTelemetry, setDispatchedTelemetry] = useState([]);

  // District admin mock upload states
  const [csvFile, setCsvFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [calibrationLogs, setCalibrationLogs] = useState([]);
  const [isCalibrated, setIsCalibrated] = useState(false);


  // Start timer on first user action
  const handleFirstAction = () => {
    if (!startTime) {
      setStartTime(Date.now());
    }
  };

  const handleBaseSelection = (base) => {
    if (isCompleted) return;
    handleFirstAction();

    const expectedBase = COMPLEMENTARY_MAP[templateDNA[currentIndex]];
    const newLogEntry = {
      timestamp: new Date().toLocaleTimeString(),
      template: templateDNA[currentIndex],
      attempt: base,
    };

    if (base === expectedBase) {
      // Correct Match
      const updatedChain = [...mrnaChain, base];
      setMrnaChain(updatedChain);
      newLogEntry.status = "SUCCESS";
      newLogEntry.message = `Correctly paired ${base} with template ${templateDNA[currentIndex]}`;
      setFeedbackLog((prev) => [newLogEntry, ...prev]);

      // Move to next base index
      if (currentIndex + 1 < templateDNA.length) {
        setCurrentIndex(currentIndex + 1);
      } else {
        setIsCompleted(true);
        newLogEntry.message = "Transcription Complete! Click 'Submit' to process telemetry.";
      }
    } else {
      // Incorrect Match
      setErrors((prev) => prev + 1);
      newLogEntry.status = "ERROR";
      newLogEntry.message = `Incorrect: ${base} does not pair with ${templateDNA[currentIndex]}`;
      setFeedbackLog((prev) => [newLogEntry, ...prev]);
    }

    // Capture telemetry locally for Task 3 validation
    logTelemetryEvent("pair_base", {
      index: currentIndex,
      template_base: templateDNA[currentIndex],
      attempted_base: base,
      is_correct: base === expectedBase,
      cumulative_errors: base === expectedBase ? errors : errors + 1,
    });
  };

  // Log events locally for developer visualization
  const logTelemetryEvent = (eventType, payload) => {
    const newEvent = {
      event_id: `evt_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      event_type: eventType,
      payload: payload,
    };
    setDispatchedTelemetry((prev) => [newEvent, ...prev]);
  };

  const resetSimulation = () => {
    setMrnaChain([]);
    setCurrentIndex(0);
    setErrors(0);
    setStartTime(null);
    setIsCompleted(false);
    setFeedbackLog([]);
    setDispatchedTelemetry([]);
    logTelemetryEvent("reset", { message: "User cleared and reset transcription canvas" });
  };

  const simulateCsvUpload = () => {
    if (isCalibrating) return;
    setCsvFile("ccra_export_sample.csv");
    setUploadProgress(0);
    setIsCalibrating(true);
    setIsCalibrated(false);
    setCalibrationLogs(["[INFO] Initiating EOY assessment data import..."]);

    const steps = [
      { progress: 20, log: "[INFO] Parsing CSV headers..." },
      { progress: 45, log: "[INFO] Stripping student names, emails, and PII... OK" },
      { progress: 65, log: "[INFO] Generating secure cryptographic UUIDv4 hashes... OK" },
      { progress: 85, log: "[INFO] Merging EOY test scores with student telemetry vectors... OK" },
      { progress: 95, log: "[INFO] Purging raw identifiers and file from memory buffer... OK" },
      { progress: 100, log: "[SUCCESS] Model retrained successfully! 1,420 matched student records. Active Model: v1.3." }
    ];

    steps.forEach((step, index) => {
      setTimeout(() => {
        setUploadProgress(step.progress);
        setCalibrationLogs((prev) => [...prev, step.log]);
        if (step.progress === 100) {
          setIsCalibrating(false);
          setIsCalibrated(true);
        }
      }, (index + 1) * 600);
    });
  };


  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Header Bar */}
      <header className="border-b border-zinc-800 bg-zinc-900/50 backdrop-blur px-6 py-4 flex justify-between items-center sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center font-bold text-lg text-white shadow-lg shadow-indigo-500/30">
            S
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-zinc-400 bg-clip-text text-transparent">
              Swift Science
            </h1>
            <p className="text-xs text-zinc-500">Grade 11 OAS Biology Simulator</p>
          </div>
        </div>

        {/* Dev Mode Role Toggle */}
        <div className="flex bg-zinc-800 p-1 rounded-lg border border-zinc-700/50">
          <button
            onClick={() => setRole("student")}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              role === "student"
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            Student Simulator
          </button>
          <button
            onClick={() => setRole("teacher")}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              role === "teacher"
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            Teacher Roster
          </button>
          <button
            onClick={() => setRole("admin")}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              role === "admin"
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            District Admin
          </button>
        </div>
      </header>


      {/* Main Content Area */}
      {role === "student" && (
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Simulator Panel */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 h-40 w-40 bg-indigo-500/5 rounded-full blur-3xl" />
              
              <div className="flex justify-between items-center mb-6">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">
                    Active Challenge
                  </span>
                  <h2 className="text-2xl font-bold mt-1 text-white">
                    DNA Transcription (B.LS1.1)
                  </h2>
                </div>
                <button
                  onClick={resetSimulation}
                  className="px-3 py-1 text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-md border border-zinc-700 transition"
                >
                  Reset Canvas
                </button>
              </div>

              {/* Progress Summary Cards */}
              <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                  <span className="text-xs text-zinc-500">Progress</span>
                  <div className="text-lg font-bold text-white mt-0.5">
                    {mrnaChain.length} / {templateDNA.length}
                  </div>
                </div>
                <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                  <span className="text-xs text-zinc-500">Errors Logged</span>
                  <div className={`text-lg font-bold mt-0.5 ${errors > 0 ? "text-rose-400" : "text-emerald-400"}`}>
                    {errors}
                  </div>
                </div>
                <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                  <span className="text-xs text-zinc-500">Accuracy</span>
                  <div className="text-lg font-bold text-white mt-0.5">
                    {mrnaChain.length + errors > 0
                      ? `${Math.round((mrnaChain.length / (mrnaChain.length + errors)) * 100)}%`
                      : "100%"}
                  </div>
                </div>
              </div>

              {/* DNA Double Helix Representation */}
              <div className="space-y-8 bg-zinc-950/80 border border-zinc-850 p-6 rounded-2xl mb-8">
                {/* DNA Template Strand */}
                <div>
                  <div className="text-xs font-semibold text-zinc-500 mb-2 uppercase tracking-wide">
                    {"DNA Template Strand (3' -> 5')"}
                  </div>
                  <div className="flex flex-wrap gap-2.5">
                    {templateDNA.map((base, idx) => {
                      const isActive = idx === currentIndex && !isCompleted;
                      return (
                        <div
                          key={idx}
                          className={`h-14 w-12 rounded-xl flex flex-col justify-center items-center font-bold text-lg border transition-all ${
                            isActive
                              ? "bg-zinc-800 border-indigo-500 scale-105 shadow-lg shadow-indigo-500/10 ring-2 ring-indigo-500/20"
                              : "bg-zinc-900 border-zinc-800 text-zinc-400"
                          }`}
                        >
                          <span className="text-xs text-zinc-600 font-semibold mb-0.5">{idx + 1}</span>
                          {base}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Connecting Bonds Representation */}
                <div className="flex gap-2.5 px-3 py-1 text-zinc-700 justify-start select-none">
                  {templateDNA.map((_, idx) => (
                    <div key={idx} className="w-12 flex justify-center text-zinc-700/40 text-xs font-black">
                      ║
                    </div>
                  ))}
                </div>

                {/* Transcribed mRNA Strand */}
                <div>
                  <div className="text-xs font-semibold text-zinc-500 mb-2 uppercase tracking-wide">
                    {"mRNA Transcript Strand (5' -> 3')"}
                  </div>

                  <div className="flex flex-wrap gap-2.5">
                    {templateDNA.map((_, idx) => {
                      const base = mrnaChain[idx];
                      const isNext = idx === currentIndex && !isCompleted;
                      return (
                        <div
                          key={idx}
                          className={`h-14 w-12 rounded-xl flex flex-col justify-center items-center font-bold text-lg border transition-all ${
                            base
                              ? `bg-gradient-to-b ${BASE_COLORS[base]}`
                              : isNext
                              ? "border-dashed border-zinc-700 bg-zinc-900/30 text-indigo-400 animate-pulse"
                              : "border-dashed border-zinc-800 text-zinc-855"
                          }`}
                        >
                          <span className="text-[10px] text-zinc-500 mb-0.5">{idx + 1}</span>
                          {base || "?"}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Interaction Nucleotide Picker Controls */}
              <div className="bg-zinc-950/40 border border-zinc-800/60 p-6 rounded-2xl text-center">
                <p className="text-sm text-zinc-400 mb-4 font-medium">
                  {isCompleted
                    ? "Helix fully transcribed! Proceed to submission."
                    : `Select the matching mRNA base for DNA nucleotide ${templateDNA[currentIndex]} at position ${currentIndex + 1}:`}
                </p>

                <div className="flex justify-center gap-4">
                  {["A", "U", "C", "G"].map((base) => (
                    <button
                      key={base}
                      disabled={isCompleted}
                      onClick={() => handleBaseSelection(base)}
                      className={`h-16 w-16 rounded-full font-black text-xl bg-gradient-to-b transition-all transform hover:scale-105 active:scale-95 disabled:opacity-30 disabled:pointer-events-none shadow-md ${BASE_COLORS[base]}`}
                    >
                      {base}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Feedback & Telemetry Visualizer Sidebar */}
          <div className="space-y-6">
            {/* Live Feedback Logs */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 shadow-xl h-72 flex flex-col">
              <h3 className="text-sm font-bold text-white mb-3 uppercase tracking-wider text-zinc-400">
                Action Feedback Log
              </h3>
              <div className="flex-1 overflow-y-auto space-y-2.5 pr-2 scrollbar-thin scrollbar-thumb-zinc-800">
                {feedbackLog.length === 0 ? (
                  <p className="text-zinc-500 text-xs italic text-center mt-16">
                    No actions taken yet. Click a base to begin transcription.
                  </p>
                ) : (
                  feedbackLog.map((log, idx) => (
                    <div
                      key={idx}
                      className={`p-2.5 rounded-lg border text-xs flex gap-2.5 items-start ${
                        log.status === "SUCCESS"
                          ? "bg-emerald-500/5 border-emerald-500/20 text-emerald-300"
                          : "bg-rose-500/5 border-rose-500/20 text-rose-300"
                      }`}
                    >
                      <span className="font-mono text-[10px] text-zinc-500 pt-0.5">
                        {log.timestamp}
                      </span>
                      <div>{log.message}</div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Developer Telemetry Preview (Task 3 Validation) */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 shadow-xl flex-1 flex flex-col h-80">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-sm font-bold text-white uppercase tracking-wider text-zinc-400">
                  Telemetry Dispatch Preview
                </h3>
                <span className="text-[10px] bg-zinc-800 text-indigo-400 px-2 py-0.5 rounded-full font-mono">
                  JSON Streams
                </span>
              </div>
              <div className="flex-1 bg-zinc-950 border border-zinc-850 rounded-xl p-3 font-mono text-[10px] text-zinc-400 overflow-y-auto scrollbar-thin scrollbar-thumb-zinc-855">
                {dispatchedTelemetry.length === 0 ? (
                  <span className="text-zinc-600 italic">
                    {"// Telemetry payload streams will render here in real time..."}
                  </span>
                ) : (
                  <pre className="whitespace-pre-wrap">
                    {JSON.stringify(dispatchedTelemetry, null, 2)}
                  </pre>
                )}
              </div>
            </div>
          </div>
        </main>
      )}

      {role === "teacher" && (
        /* Teacher Dashboard Stub View */
        <main className="flex-1 max-w-7xl w-full mx-auto p-6">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
            <h2 className="text-2xl font-bold text-white mb-2">Teacher Analytics Dashboard</h2>
            <p className="text-sm text-zinc-400 mb-6">
              This dashboard view will render in Week 2 (Sprint 1 Tasks 6 & 7) once database telemetry integration is complete.
            </p>
            <div className="border border-dashed border-zinc-800 p-12 rounded-xl text-center text-zinc-650 italic">
              Rosters, completed student profiles, and predicted OPI levels (Below Basic, Basic, Proficient, Advanced) will render here.
            </div>
          </div>
        </main>
      )}

      {role === "admin" && (
        /* District Admin Dashboard View */
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-white">District Administrator Hub</h2>
              <p className="text-sm text-zinc-400">Manage licenses, view campus performance, and calibrate predictive models.</p>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-xl flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping"></span>
              <span className="text-xs font-semibold text-zinc-300">
                Model: {isCalibrated ? "Active v1.3 (Calibrated)" : "Active v1.2 (Default Heuristic)"}
              </span>
            </div>
          </div>

          {/* Stat Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Active Campuses</span>
              <div className="text-2xl font-bold text-white mt-1">4 Schools</div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Seat Licenses</span>
              <div className="text-2xl font-bold text-white mt-1">1,420 / 2,000</div>
              <div className="text-xs text-zinc-500 mt-0.5">71% Seat Utilization</div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Est. Proficiency Rate</span>
              <div className="text-2xl font-bold text-indigo-400 mt-1">68.4%</div>
              <div className="text-xs text-zinc-500 mt-0.5">Target: 70% for positive card</div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Total Telemetry Streams</span>
              <div className="text-2xl font-bold text-white mt-1">18,342 events</div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Campus List Table */}
            <div className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
              <h3 className="text-lg font-bold text-white mb-4">Campus Performance Summary</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-zinc-400">
                  <thead className="text-xs text-zinc-500 uppercase border-b border-zinc-850">
                    <tr>
                      <th className="py-3">School Name</th>
                      <th className="py-3">Students Active</th>
                      <th className="py-3">Avg Accuracy</th>
                      <th className="py-3 text-right">Est. Proficient+</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-zinc-850 font-medium">
                    <tr>
                      <td className="py-3.5 text-white">Central High School</td>
                      <td className="py-3.5">680 / 800 seats</td>
                      <td className="py-3.5">84.2%</td>
                      <td className="py-3.5 text-right text-emerald-400">74.1%</td>
                    </tr>
                    <tr>
                      <td className="py-3.5 text-white">Westside Academy</td>
                      <td className="py-3.5">420 / 600 seats</td>
                      <td className="py-3.5">71.8%</td>
                      <td className="py-3.5 text-right text-amber-400">48.2%</td>
                    </tr>
                    <tr>
                      <td className="py-3.5 text-white">Oak Creek High</td>
                      <td className="py-3.5">210 / 400 seats</td>
                      <td className="py-3.5">91.5%</td>
                      <td className="py-3.5 text-right text-emerald-400">88.5%</td>
                    </tr>
                    <tr>
                      <td className="py-3.5 text-white">Innovation Charter</td>
                      <td className="py-3.5">110 / 200 seats</td>
                      <td className="py-3.5">64.0%</td>
                      <td className="py-3.5 text-right text-rose-400">35.4%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Score Calibration Panel */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
              <div>
                <h3 className="text-lg font-bold text-white mb-1">EOY Score Calibration</h3>
                <p className="text-xs text-zinc-500 mb-4">
                  Upload de-identified score tables to map EOY actual CCRA grades to in-app telemetry for model retraining.
                </p>

                {/* Upload Action Area */}
                <div className="border border-dashed border-zinc-800 bg-zinc-950/40 rounded-xl p-6 text-center space-y-3">
                  <div className="text-3xl text-zinc-650">📊</div>
                  <div>
                    <span className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 cursor-pointer" onClick={simulateCsvUpload}>
                      {csvFile ? `Attached: ${csvFile}` : "Click to select de-identified CSV"}
                    </span>
                    <p className="text-[10px] text-zinc-600 mt-1">Accepts serial user-id & scaled score columns.</p>
                  </div>
                </div>

                {/* Progress bar */}
                {isCalibrating && (
                  <div className="mt-4 space-y-1.5">
                    <div className="flex justify-between text-[10px] font-semibold text-zinc-500">
                      <span>Calibrating model...</span>
                      <span>{uploadProgress}%</span>
                    </div>
                    <div className="w-full bg-zinc-800 h-1 rounded-full overflow-hidden">
                      <div className="bg-indigo-500 h-1 transition-all duration-300" style={{ width: `${uploadProgress}%` }}></div>
                    </div>
                  </div>
                )}

                {/* Ingestion Log Output */}
                {calibrationLogs.length > 0 && (
                  <div className="mt-4 bg-zinc-950 border border-zinc-850 p-3 rounded-lg font-mono text-[9px] text-zinc-400 h-36 overflow-y-auto space-y-1.5">
                    {calibrationLogs.map((log, idx) => (
                      <div key={idx} className={log.startsWith("[SUCCESS]") ? "text-emerald-400" : ""}>
                        {log}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-6 pt-4 border-t border-zinc-850 flex gap-3">
                <button
                  disabled={isCalibrating || !csvFile}
                  onClick={() => {
                    setCsvFile(null);
                    setCalibrationLogs([]);
                    setIsCalibrated(false);
                  }}
                  className="flex-1 py-2 text-xs font-semibold bg-zinc-800 text-zinc-300 rounded-lg hover:bg-zinc-700 transition disabled:opacity-40"
                >
                  Clear Data
                </button>
                <button
                  disabled={isCalibrating || isCalibrated}
                  onClick={simulateCsvUpload}
                  className="flex-1 py-2 text-xs font-semibold bg-indigo-600 text-white rounded-lg hover:bg-indigo-500 transition shadow-md shadow-indigo-600/20 disabled:opacity-40"
                >
                  {isCalibrated ? "Calibrated" : "Run Ingestion"}
                </button>
              </div>
            </div>
          </div>
        </main>
      )}
    </div>
  );
}
