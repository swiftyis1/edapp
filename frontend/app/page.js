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

const MOCK_STUDENTS = [
  { id: "da59114f-c0df-4d51-a957-cc3b23c92b23", name: "Alex Rivera" },
  { id: "e2d1d0c5-5a7c-47bc-8367-4f6c122bb33f", name: "Blake Henderson" },
  { id: "f04eb32d-2098-4b72-88ec-8f0a1c6a23b1", name: "Charlie Smith" },
  { id: "0e46be9f-b7a4-4df8-9226-eb52cbfb27d4", name: "Daniela Garcia" },
  { id: "1b131012-38d5-4ad9-bf9f-864a66a1cc92", name: "Erik Johnson" },
];

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
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [feedbackLog, setFeedbackLog] = useState([]);

  // Active student & session IDs
  const [selectedStudent, setSelectedStudent] = useState(MOCK_STUDENTS[1]); // Default to Blake Henderson
  const [sessionId, setSessionId] = useState("");

  // Telemetry dispatch logs (stored locally for preview in Task 3)
  const [dispatchedTelemetry, setDispatchedTelemetry] = useState([]);

  // Teacher dashboard live report states
  const [teacherReportData, setTeacherReportData] = useState([]);
  const [isLoadingReport, setIsLoadingReport] = useState(false);

  // District admin mock upload states
  const [csvFile, setCsvFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [calibrationLogs, setCalibrationLogs] = useState([]);
  const [isCalibrated, setIsCalibrated] = useState(false);


  // Initialize Session ID on mount or on student change
  useEffect(() => {
    if (typeof window !== "undefined") {
      setSessionId(crypto.randomUUID());
    }
  }, [selectedStudent]);

  // Fetch report data when role switches to teacher
  useEffect(() => {
    if (role === "teacher") {
      fetchTeacherReport();
    }
  }, [role]);

  const fetchTeacherReport = async () => {
    setIsLoadingReport(true);
    try {
      const response = await fetch("http://localhost:8000/api/reports/teacher/");
      if (response.ok) {
        const data = await response.json();
        setTeacherReportData(data);
      } else {
        console.warn("Failed to fetch teacher report:", response.statusText);
      }
    } catch (err) {
      console.warn("Error fetching teacher report:", err.message);
    } finally {
      setIsLoadingReport(false);
    }
  };


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
        setFeedbackLog((prev) => [newLogEntry, ...prev]);
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

  // Log events locally for developer visualization and dispatch to Django backend
  const logTelemetryEvent = async (eventType, payload) => {
    const newEvent = {
      event_id: typeof window !== "undefined" ? crypto.randomUUID() : `evt_${Math.random().toString(36).substr(2, 9)}`,
      student_id: selectedStudent.id,   // Dynamic UUID
      session_id: sessionId,           // Dynamic Session UUID
      timestamp: new Date().toISOString(),
      event_type: eventType,
      level_id: "dna_transcription_1",
      construct_tag: "OAS.B.LS1.1",
      payload: payload,
    };

    // Add to local preview state
    setDispatchedTelemetry((prev) => [newEvent, ...prev]);

    // Dispatch to the backend API stub
    try {
      const response = await fetch("http://localhost:8000/api/telemetry/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newEvent),
      });
      if (!response.ok) {
        console.warn("Failed to dispatch telemetry to backend:", response.statusText);
      }
    } catch (err) {
      console.warn("Network error dispatching telemetry:", err.message);
    }
  };

  const handleSubmitSimulation = async () => {
    const duration = startTime ? (Date.now() - startTime) / 1000 : 0.0;
    const accuracy = mrnaChain.length + errors > 0
      ? Math.round((mrnaChain.length / (mrnaChain.length + errors)) * 100)
      : 100;

    await logTelemetryEvent("session_complete", {
      total_errors: errors,
      accuracy: accuracy,
      duration_seconds: parseFloat(duration.toFixed(2)),
    });

    setIsSubmitted(true);
  };

  const resetSimulation = () => {
    setMrnaChain([]);
    setCurrentIndex(0);
    setErrors(0);
    setStartTime(null);
    setIsCompleted(false);
    setIsSubmitted(false);
    setFeedbackLog([]);
    setDispatchedTelemetry([]);
    if (typeof window !== "undefined") {
      setSessionId(crypto.randomUUID());
    }
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
              
              <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-6 border-b border-zinc-800/60 pb-6">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">
                    Active Challenge
                  </span>
                  <h2 className="text-2xl font-bold mt-1 text-white">
                    DNA Transcription (B.LS1.1)
                  </h2>
                </div>
                
                <div className="flex flex-wrap items-center gap-3">
                  {/* Student Select Dropdown */}
                  <div className="flex items-center gap-2 bg-zinc-950 px-3 py-1.5 rounded-lg border border-zinc-800">
                    <span className="text-[10px] uppercase font-bold text-zinc-500">Student:</span>
                    <select
                      value={selectedStudent.id}
                      onChange={(e) => {
                        const s = MOCK_STUDENTS.find(x => x.id === e.target.value);
                        if (s) {
                          setSelectedStudent(s);
                          resetSimulation();
                        }
                      }}
                      className="bg-transparent text-xs font-bold text-white focus:outline-none border-none cursor-pointer"
                    >
                      {MOCK_STUDENTS.map(s => (
                        <option key={s.id} value={s.id} className="bg-zinc-900 text-white">
                          {s.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <button
                    onClick={resetSimulation}
                    className="px-3 py-1.5 text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-md border border-zinc-700 transition"
                  >
                    Reset Canvas
                  </button>
                </div>
              </div>

              {isSubmitted ? (
                <div className="text-center py-12 px-4 space-y-6">
                  <div className="h-16 w-16 mx-auto bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center text-3xl font-black shadow-lg shadow-emerald-500/10">
                    ✓
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-white">Simulation Completed!</h3>
                    <p className="text-sm text-zinc-400 mt-2 max-w-md mx-auto">
                      DNA transcription telemetry data has been successfully transmitted and logged in PostgreSQL.
                    </p>
                  </div>
                  <div className="bg-zinc-950/60 border border-zinc-800/80 p-5 rounded-xl max-w-sm mx-auto grid grid-cols-2 gap-4 text-left font-sans">
                    <div>
                      <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Student Profile</span>
                      <div className="text-sm font-semibold text-white mt-0.5">{selectedStudent.name}</div>
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Session ID</span>
                      <div className="text-sm font-mono text-zinc-400 mt-0.5">{sessionId.slice(0, 8)}...</div>
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Errors Logged</span>
                      <div className="text-sm font-bold mt-0.5 text-rose-400">{errors}</div>
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Accuracy</span>
                      <div className="text-sm font-bold mt-0.5 text-emerald-400">
                        {mrnaChain.length + errors > 0
                          ? `${Math.round((mrnaChain.length / (mrnaChain.length + errors)) * 100)}%`
                          : "100%"}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={resetSimulation}
                    className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg shadow-md shadow-indigo-600/20 transition-all transform hover:scale-105 active:scale-95"
                  >
                    Reset & Play Again
                  </button>
                </div>
              ) : (
                <>
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
                    {isCompleted ? (
                      <div className="space-y-4 py-2">
                        <p className="text-sm text-emerald-400 font-semibold animate-pulse">
                          ✓ Helix fully transcribed! Ready to submit telemetry data to backend.
                        </p>
                        <button
                          onClick={handleSubmitSimulation}
                          className="px-8 py-3.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-bold rounded-xl shadow-lg shadow-emerald-500/20 transform hover:scale-105 transition-all duration-300 active:scale-95 text-xs uppercase tracking-wider"
                        >
                          Submit Simulation Results
                        </button>
                      </div>
                    ) : (
                      <>
                        <p className="text-sm text-zinc-400 mb-4 font-medium">
                          Select the matching mRNA base for DNA nucleotide {templateDNA[currentIndex]} at position {currentIndex + 1}:
                        </p>

                        <div className="flex justify-center gap-4">
                          {["A", "U", "C", "G"].map((base) => (
                            <button
                              key={base}
                              onClick={() => handleBaseSelection(base)}
                              className={`h-16 w-16 rounded-full font-black text-xl bg-gradient-to-b transition-all transform hover:scale-105 active:scale-95 shadow-md ${BASE_COLORS[base]}`}
                            >
                              {base}
                            </button>
                          ))}
                        </div>
                      </>
                    )}
                  </div>
                </>
              )}
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
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-white">Teacher Analytics Dashboard</h2>
              <p className="text-sm text-zinc-400">Monitor student standard mastery, session metrics, and predicted OPI Performance Bands.</p>
            </div>
            <button
              onClick={fetchTeacherReport}
              disabled={isLoadingReport}
              className="px-3 py-1.5 text-xs font-semibold bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded-lg border border-zinc-700 transition flex items-center gap-2"
            >
              {isLoadingReport ? "Refreshing..." : "Refresh Roster"}
            </button>
          </div>

          {/* Quick Metrics Summary */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Total Roster</span>
              <div className="text-2xl font-bold text-white mt-1">{teacherReportData.length} Students</div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Class Avg Accuracy</span>
              <div className="text-2xl font-bold text-indigo-400 mt-1">
                {teacherReportData.length > 0
                  ? `${Math.round(teacherReportData.reduce((acc, curr) => acc + curr.accuracy, 0) / teacherReportData.length)}%`
                  : "0%"}
              </div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Class Avg Speed</span>
              <div className="text-2xl font-bold text-white mt-1">
                {teacherReportData.length > 0
                  ? `${(teacherReportData.reduce((acc, curr) => acc + curr.avg_time_per_base, 0) / teacherReportData.length).toFixed(2)}s / base`
                  : "0.00s / base"}
              </div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Accountability Flag</span>
              <div className="text-2xl font-bold text-rose-400 mt-1">
                {teacherReportData.filter(s => s.status_flag === "Needs Support").length} Flagged
              </div>
            </div>
          </div>

          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold text-white">Student Mastery Roster (OAS B.LS1.1)</h3>
              <div className="text-xs bg-zinc-950 px-2.5 py-1.5 rounded-md border border-zinc-850 font-mono text-zinc-500">
                Active Standard: DNA & Proteins
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-zinc-400">
                <thead className="text-xs text-zinc-500 uppercase border-b border-zinc-850">
                  <tr>
                    <th className="py-3">Student Name</th>
                    <th className="py-3">OPI Performance Band</th>
                    <th className="py-3">Predicted OPI Score</th>
                    <th className="py-3">Accuracy (%)</th>
                    <th className="py-3">Avg Speed</th>
                    <th className="py-3">Actions Logged</th>
                    <th className="py-3 text-right">Accountability Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-850 font-medium">
                  {teacherReportData.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="py-8 text-center text-zinc-500 italic">
                        No students found. Run the seed telemetry script to populate.
                      </td>
                    </tr>
                  ) : (
                    teacherReportData.map((student) => (
                      <tr key={student.id} className="hover:bg-zinc-900/30 transition-colors">
                        <td className="py-3.5 text-white flex items-center gap-3">
                          <div className="h-7 w-7 rounded-full bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center text-xs font-bold font-mono">
                            {student.name.split(' ').map(n => n[0]).join('')}
                          </div>
                          <span>{student.name}</span>
                        </td>
                        <td className="py-3.5">
                          {student.performance_band !== "N/A" ? (
                            <span className={`px-2.5 py-1 rounded-full text-xs font-bold border ${student.color_class}`}>
                              {student.performance_band}
                            </span>
                          ) : (
                            <span className="text-zinc-600">—</span>
                          )}
                        </td>
                        <td className="py-3.5 font-bold font-mono text-white">
                          {student.opi_score > 0 ? student.opi_score : "—"}
                        </td>
                        <td className="py-3.5">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-zinc-200">{student.accuracy}%</span>
                            <div className="w-16 bg-zinc-800 h-1.5 rounded-full overflow-hidden hidden sm:block">
                              <div 
                                className={`h-full ${
                                  student.accuracy >= 90 
                                    ? "bg-emerald-500" 
                                    : student.accuracy >= 80 
                                    ? "bg-indigo-500" 
                                    : student.accuracy >= 70 
                                    ? "bg-amber-500" 
                                    : "bg-rose-500"
                                }`} 
                                style={{ width: `${student.accuracy}%` }}
                              ></div>
                            </div>
                          </div>
                        </td>
                        <td className="py-3.5 font-mono text-zinc-300">
                          {student.avg_time_per_base > 0 ? `${student.avg_time_per_base}s` : "—"}
                        </td>
                        <td className="py-3.5 font-mono text-zinc-400">
                          {student.total_actions}
                        </td>
                        <td className="py-3.5 text-right">
                          {student.status_flag === "On Track" ? (
                            <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-semibold text-emerald-400 bg-emerald-500/5 rounded-md border border-emerald-500/10">
                              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                              On Track
                            </span>
                          ) : student.status_flag === "Needs Support" ? (
                            <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-semibold text-rose-400 bg-rose-500/5 rounded-md border border-rose-500/10 animate-pulse">
                              <span className="h-1.5 w-1.5 rounded-full bg-rose-500"></span>
                              Needs Support
                            </span>
                          ) : (
                            <span className="text-zinc-600">—</span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
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
