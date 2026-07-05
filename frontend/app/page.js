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
  // App Role View: 'student' (DNA Sandbox) vs 'teacher' vs 'admin' vs 'parent'
  const [role, setRole] = useState("student");

  // Auth States
  const [token, setToken] = useState(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("swift_science_token") || null;
    }
    return null;
  });
  const [currentUser, setCurrentUser] = useState(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("swift_science_user");
      return stored ? JSON.parse(stored) : null;
    }
    return null;
  });

  const [authMode, setAuthMode] = useState("login"); // 'login' or 'register'
  const [usernameInput, setUsernameInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");
  const [firstNameInput, setFirstNameInput] = useState("");
  const [lastNameInput, setLastNameInput] = useState("");
  const [roleInput, setRoleInput] = useState("student");
  const [classCodeInput, setClassCodeInput] = useState("");
  const [authError, setAuthError] = useState("");

  // Classroom Management States
  const [newClassName, setNewClassName] = useState("");
  const [createdClassroom, setCreatedClassroom] = useState(null);
  const [classCodeJoin, setClassCodeJoin] = useState("");
  const [classroomInfo, setClassroomInfo] = useState(null);
  const [joinMessage, setJoinMessage] = useState("");
  const [joinError, setJoinError] = useState("");

  // District Admin KPIs State
  const [adminKpisData, setAdminKpisData] = useState(null);
  const [isLoadingAdminKpis, setIsLoadingAdminKpis] = useState(false);

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

  // Parent dashboard report states
  const [parentReportData, setParentReportData] = useState(null);
  const [isLoadingParentReport, setIsLoadingParentReport] = useState(false);
  const [parentReportError, setParentReportError] = useState(null);

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

  // Set default student if user is student
  useEffect(() => {
    if (currentUser && currentUser.role === "student" && currentUser.student_id) {
      setSelectedStudent({
        id: currentUser.student_id,
        name: `${currentUser.first_name} ${currentUser.last_name}`.trim() || currentUser.username
      });
    }
  }, [currentUser]);

  // Fetch report data when role switches to teacher or token changes
  useEffect(() => {
    if (role === "teacher" && token) {
      fetchTeacherReport();
    }
  }, [role, token]);

  // Fetch admin KPIs when role switches to admin or token changes
  useEffect(() => {
    if (role === "admin" && token) {
      fetchAdminKpis();
    }
  }, [role, token]);

  // Fetch parent report when role switches to parent or token changes
  useEffect(() => {
    if (role === "parent" && token) {
      fetchParentReport();
    }
  }, [role, token]);

  const fetchTeacherReport = async () => {
    setIsLoadingReport(true);
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      const response = await fetch("http://localhost:8000/api/reports/teacher/", { headers });
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

  const fetchAdminKpis = async () => {
    setIsLoadingAdminKpis(true);
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      const response = await fetch("http://localhost:8000/api/reports/admin/kpis/", { headers });
      if (response.ok) {
        const data = await response.json();
        setAdminKpisData(data);
      }
    } catch (err) {
      console.warn("Failed to fetch admin KPIs:", err.message);
    } finally {
      setIsLoadingAdminKpis(false);
    }
  };

  const fetchParentReport = async () => {
    setIsLoadingParentReport(true);
    setParentReportError(null);
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      const response = await fetch("http://localhost:8000/api/reports/parent/", { headers });
      if (response.ok) {
        const data = await response.json();
        setParentReportData(data);
      } else {
        setParentReportError("Failed to fetch parent report data.");
      }
    } catch (err) {
      setParentReportError("Network error fetching parent report.");
    } finally {
      setIsLoadingParentReport(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setAuthError("");
    try {
      const response = await fetch("http://localhost:8000/api/auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: usernameInput,
          password: passwordInput,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        setToken(data.token);
        setCurrentUser(data);
        localStorage.setItem("swift_science_token", data.token);
        localStorage.setItem("swift_science_user", JSON.stringify(data));
        setRole(data.role);
        
        if (data.role === "student" && data.student_id) {
          setSelectedStudent({
            id: data.student_id,
            name: `${data.first_name} ${data.last_name}`.trim() || data.username
          });
        }
        
        setUsernameInput("");
        setPasswordInput("");
      } else {
        const err = await response.json();
        setAuthError(err.error || "Invalid username or password.");
      }
    } catch (err) {
      setAuthError("Failed to connect to backend server.");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setAuthError("");
    try {
      const response = await fetch("http://localhost:8000/api/auth/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: usernameInput,
          password: passwordInput,
          role: roleInput,
          first_name: firstNameInput,
          last_name: lastNameInput,
          class_code: classCodeInput,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        setToken(data.token);
        setCurrentUser(data);
        localStorage.setItem("swift_science_token", data.token);
        localStorage.setItem("swift_science_user", JSON.stringify(data));
        setRole(data.role);
        
        if (data.role === "student" && data.student_id) {
          setSelectedStudent({
            id: data.student_id,
            name: `${data.first_name} ${data.last_name}`.trim() || data.username
          });
        }
        
        setUsernameInput("");
        setPasswordInput("");
        setFirstNameInput("");
        setLastNameInput("");
        setClassCodeInput("");
      } else {
        const err = await response.json();
        setAuthError(err.error || "Registration failed.");
      }
    } catch (err) {
      setAuthError("Failed to connect to backend server.");
    }
  };

  const handleLogout = () => {
    setToken(null);
    setCurrentUser(null);
    localStorage.removeItem("swift_science_token");
    localStorage.removeItem("swift_science_user");
    setRole("student");
    resetSimulation();
  };

  const handleCreateClassroom = async (e) => {
    e.preventDefault();
    if (!newClassName) return;
    try {
      const response = await fetch("http://localhost:8000/api/classroom/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({ name: newClassName }),
      });
      if (response.ok) {
        const data = await response.json();
        setCreatedClassroom(data);
        setNewClassName("");
        fetchTeacherReport();
      }
    } catch (err) {
      console.error("Error creating classroom:", err);
    }
  };

  const handleJoinClassroom = async (e) => {
    e.preventDefault();
    setJoinMessage("");
    setJoinError("");
    if (!classCodeJoin) return;
    try {
      const response = await fetch("http://localhost:8000/api/classroom/join/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({ class_code: classCodeJoin }),
      });
      if (response.ok) {
        const data = await response.json();
        setJoinMessage(data.message);
        setClassroomInfo(data);
        setClassCodeJoin("");
      } else {
        const err = await response.json();
        setJoinError(err.error || "Failed to join classroom.");
      }
    } catch (err) {
      setJoinError("Failed to connect to backend.");
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
      const headers = {
        "Content-Type": "application/json",
      };
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      const response = await fetch("http://localhost:8000/api/telemetry/", {
        method: "POST",
        headers,
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

  const simulateCsvUpload = async () => {
    if (isCalibrating) return;
    setCsvFile("ccra_export_sample.csv");
    setUploadProgress(0);
    setIsCalibrating(true);
    setIsCalibrated(false);
    setCalibrationLogs(["[INFO] Initiating EOY assessment data import..."]);

    const csvContent = [
      "user_id,raw_score",
      "alex_rivera,385",
      "blake_henderson,318",
      "charlie_smith,285",
      "daniela_garcia,240",
      "erik_johnson,200"
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const formData = new FormData();
    formData.append("file", blob, "ccra_export_sample.csv");

    try {
      setUploadProgress(40);
      setCalibrationLogs((prev) => [...prev, "[INFO] Stripping PII and converting usernames to de-identified hashes..."]);
      
      const response = await fetch("http://localhost:8000/api/admin/import-eoy/", {
        method: "POST",
        headers: {
          "Authorization": token ? `Token ${token}` : "",
        },
        body: formData,
      });

      setUploadProgress(80);
      
      if (response.ok) {
        const data = await response.json();
        setUploadProgress(100);
        setCalibrationLogs(data.logs);
        setIsCalibrated(true);
        fetchTeacherReport();
      } else {
        const err = await response.json();
        setCalibrationLogs((prev) => [
          ...prev,
          `[ERROR] Calibration failed: ${err.error || "Server error"}`
        ]);
      }
    } catch (err) {
      setCalibrationLogs((prev) => [
        ...prev,
        "[ERROR] Network error connecting to calibration endpoint."
      ]);
    } finally {
      setIsCalibrating(false);
    }
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

        {/* Role-Based Route Guards / Tab Toggles */}
        {token && currentUser && (
          <div className="flex bg-zinc-800 p-1 rounded-lg border border-zinc-700/50">
            {(currentUser.role === "student" || currentUser.role === "teacher" || currentUser.role === "admin") && (
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
            )}
            {(currentUser.role === "teacher" || currentUser.role === "admin") && (
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
            )}
            {currentUser.role === "admin" && (
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
            )}
            {currentUser.role === "parent" && (
              <button
                onClick={() => setRole("parent")}
                className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                  role === "parent"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                Parent Portal
              </button>
            )}
          </div>
        )}

        {/* User Account Info / Logout */}
        {token && currentUser ? (
          <div className="flex items-center gap-4">
            <div className="text-right hidden sm:block">
              <div className="text-sm font-semibold text-white">
                {currentUser.first_name} {currentUser.last_name}
              </div>
              <div className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider">
                {currentUser.role}
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="px-3 py-1.5 text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded border border-zinc-700 font-bold transition"
            >
              Logout
            </button>
          </div>
        ) : null}
      </header>


      {/* Main Content Area / Route Guard */}
      {!token ? (
        <main className="flex-1 flex items-center justify-center p-6">
          <div className="bg-zinc-900/80 border border-zinc-800 backdrop-blur rounded-2xl p-8 max-w-md w-full shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 h-40 w-40 bg-indigo-500/10 rounded-full blur-3xl" />
            
            <div className="text-center mb-8">
              <div className="h-12 w-12 mx-auto rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center font-bold text-2xl text-white shadow-lg shadow-indigo-500/30 mb-3">
                S
              </div>
              <h2 className="text-2xl font-bold text-white">Welcome to Swift Science</h2>
              <p className="text-xs text-zinc-500 mt-1">Authenticate to access the Grade 11 OAS Biology platform</p>
            </div>

            {authError && (
              <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-3 rounded-lg text-xs font-semibold mb-5 text-center animate-pulse">
                {authError}
              </div>
            )}

            <form onSubmit={authMode === "login" ? handleLogin : handleRegister} className="space-y-4">
              {authMode === "register" && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">First Name</label>
                    <input
                      type="text"
                      value={firstNameInput}
                      onChange={(e) => setFirstNameInput(e.target.value)}
                      required
                      className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Last Name</label>
                    <input
                      type="text"
                      value={lastNameInput}
                      onChange={(e) => setLastNameInput(e.target.value)}
                      required
                      className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                    />
                  </div>
                </div>
              )}

              <div>
                <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Username</label>
                <input
                  type="text"
                  value={usernameInput}
                  onChange={(e) => setUsernameInput(e.target.value)}
                  required
                  placeholder="e.g. teacher_albright"
                  className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>

              <div>
                <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Password</label>
                <input
                  type="password"
                  value={passwordInput}
                  onChange={(e) => setPasswordInput(e.target.value)}
                  required
                  placeholder="••••••••"
                  className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>

              {authMode === "register" && (
                <>
                  <div>
                    <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Account Role</label>
                    <select
                      value={roleInput}
                      onChange={(e) => setRoleInput(e.target.value)}
                      className="w-full bg-zinc-950 border border-zinc-850.rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors bg-zinc-900"
                    >
                      <option value="student">Student</option>
                      <option value="teacher">Teacher</option>
                      <option value="admin">District Administrator</option>
                      <option value="parent">Parent</option>
                    </select>
                  </div>

                  {roleInput === "student" && (
                    <div>
                      <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Class Code (Optional)</label>
                      <input
                        type="text"
                        value={classCodeInput}
                        onChange={(e) => setClassCodeInput(e.target.value)}
                        placeholder="e.g. BIO101"
                        className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                      />
                    </div>
                  )}
                </>
              )}

              <button
                type="submit"
                className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs uppercase tracking-wider shadow-lg shadow-indigo-600/20 transform hover:scale-[1.02] active:scale-[0.98] transition-all"
              >
                {authMode === "login" ? "Sign In" : "Create Account"}
              </button>
            </form>

            <div className="text-center mt-6 pt-6 border-t border-zinc-800/60 text-xs">
              <span className="text-zinc-500">
                {authMode === "login" ? "New to the platform?" : "Already have an account?"}
              </span>
              <button
                onClick={() => {
                  setAuthMode(authMode === "login" ? "register" : "login");
                  setAuthError("");
                }}
                className="text-indigo-400 hover:text-indigo-300 font-bold ml-1.5 focus:outline-none"
              >
                {authMode === "login" ? "Register here" : "Sign in instead"}
              </button>
            </div>
          </div>
        </main>
      ) : (
        <>
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
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-white">Teacher Analytics Dashboard</h2>
              <p className="text-sm text-zinc-400">Monitor student standard mastery, session metrics, and predicted OPI Performance Bands.</p>
            </div>
            
            <div className="flex flex-wrap gap-3">
              {/* Create Classroom Form */}
              <form onSubmit={handleCreateClassroom} className="flex gap-2">
                <input
                  type="text"
                  placeholder="Create class (e.g. Period 4)"
                  value={newClassName}
                  onChange={(e) => setNewClassName(e.target.value)}
                  className="bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                />
                <button type="submit" className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-bold transition">
                  Create Class
                </button>
              </form>

              <button
                onClick={fetchTeacherReport}
                disabled={isLoadingReport}
                className="px-3 py-1.5 text-xs font-semibold bg-zinc-850 hover:bg-zinc-750 text-zinc-200 rounded-lg border border-zinc-700 transition flex items-center gap-2"
              >
                {isLoadingReport ? "Refreshing..." : "Refresh Roster"}
              </button>
            </div>
          </div>

          {/* Active Classroom & Code Display */}
          <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 relative overflow-hidden">
            <div className="absolute top-0 right-0 h-32 w-32 bg-indigo-500/5 rounded-full blur-2xl" />
            <div>
              <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-wider">Active Classroom</span>
              <h3 className="text-xl font-bold text-white mt-0.5">
                {createdClassroom ? createdClassroom.name : "Period 3 Biology"}
              </h3>
              <p className="text-xs text-zinc-500 mt-1">
                Classroom ID: {createdClassroom ? createdClassroom.id.slice(0, 8) + "..." : "c1111111"}
              </p>
            </div>
            <div className="bg-zinc-950 border border-zinc-850 px-5 py-3 rounded-xl flex items-center gap-3">
              <div>
                <span className="text-[9px] uppercase font-bold text-zinc-500 tracking-wider block">Class Code for Students</span>
                <span className="text-2xl font-black text-indigo-400 tracking-widest font-mono select-all cursor-pointer" title="Copy to Clipboard">
                  {createdClassroom ? createdClassroom.class_code : "BIO101"}
                </span>
              </div>
            </div>
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
                  ? `${Math.round(teacherReportData.reduce((acc, curr) => acc + (curr.accuracy || 0), 0) / teacherReportData.length)}%`
                  : "0%"}
              </div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Class Avg Speed</span>
              <div className="text-2xl font-bold text-white mt-1">
                {teacherReportData.length > 0
                  ? `${(teacherReportData.reduce((acc, curr) => acc + (curr.avg_time_per_base || 0), 0) / teacherReportData.length).toFixed(2)}s / base`
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
                    <th className="py-3">Intervention Recommendation / Next Steps</th>
                    <th className="py-3 text-right">Accountability Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-850 font-medium">
                  {teacherReportData.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="py-8 text-center text-zinc-500 italic">
                        No students found in this classroom. Share your Class Code to add students.
                      </td>
                    </tr>
                  ) : (
                    teacherReportData.map((student) => {
                      let recommendation = "No active intervention required.";
                      if (student.performance_band === "Advanced") {
                        recommendation = "On track. Recommend advanced challenges (e.g. translation/protein synthesis).";
                      } else if (student.performance_band === "Proficient") {
                        recommendation = "On track. Encourage speed improvements.";
                      } else if (student.performance_band === "Basic") {
                        recommendation = "Struggles with GC/AU base-pairing. Suggest additional guided practice.";
                      } else if (student.performance_band === "Below Basic") {
                        recommendation = "High error rate. Recommend direct teacher-led intervention on mRNA matching.";
                      } else if (student.performance_band === "N/A" || student.total_actions === 0) {
                        recommendation = "Waiting for first gameplay telemetry data.";
                      }

                      return (
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
                              <span className="text-zinc-650 font-mono">—</span>
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
                          <td className="py-3.5 text-xs text-zinc-400 italic">
                            <div className="flex items-center gap-2">
                              {student.status_flag === "Needs Support" && (
                                <span className="text-rose-400 text-sm" title="Intervention Alert">⚠️</span>
                              )}
                              <span>{recommendation}</span>
                            </div>
                          </td>
                          <td className="py-3.5 text-right font-sans">
                            {student.status_flag === "On Track" ? (
                              <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-semibold text-emerald-400 bg-emerald-500/5 rounded-md border border-emerald-500/10">
                                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                                On Track
                              </span>
                            ) : student.status_flag === "Needs Support" ? (
                              <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-semibold text-rose-400 bg-rose-500/5 rounded-md border border-rose-500/10 animate-pulse" title="Student flagged for learning support">
                                <span className="h-1.5 w-1.5 rounded-full bg-rose-500"></span>
                                Needs Support
                              </span>
                            ) : (
                              <span className="text-zinc-655">—</span>
                            )}
                          </td>
                        </tr>
                      );
                    })
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
              <div className="text-2xl font-bold text-white mt-1">
                {adminKpisData ? adminKpisData.campuses.length : 4} Schools
              </div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Seat Licenses</span>
              <div className="text-2xl font-bold text-white mt-1">
                {adminKpisData ? `${adminKpisData.total_seats_active} / ${adminKpisData.total_seats_allocated}` : "1,420 / 2,000"}
              </div>
              <div className="text-xs text-zinc-500 mt-0.5">
                {adminKpisData && adminKpisData.total_seats_allocated > 0
                  ? `${Math.round((adminKpisData.total_seats_active / adminKpisData.total_seats_allocated) * 100)}% Seat Utilization`
                  : "71% Seat Utilization"}
              </div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Est. Proficiency Rate</span>
              <div className="text-2xl font-bold text-indigo-400 mt-1">
                {adminKpisData ? `${adminKpisData.overall_proficiency_rate}%` : "68.4%"}
              </div>
              <div className="text-xs text-zinc-500 mt-0.5">Target: 70% for positive card</div>
            </div>
            <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">District Avg Accuracy</span>
              <div className="text-2xl font-bold text-white mt-1">
                {adminKpisData ? `${adminKpisData.overall_avg_accuracy}%` : "82.5%"}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Campus List Table */}
            <div className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-bold text-white">Campus Performance Summary</h3>
                <button
                  onClick={fetchAdminKpis}
                  disabled={isLoadingAdminKpis}
                  className="px-2.5 py-1 text-[11px] font-semibold bg-zinc-850 hover:bg-zinc-750 text-zinc-350 rounded border border-zinc-700 transition"
                >
                  {isLoadingAdminKpis ? "Loading..." : "Refresh KPIs"}
                </button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-zinc-400">
                  <thead className="text-xs text-zinc-500 uppercase border-b border-zinc-850">
                    <tr>
                      <th className="py-3">School Name</th>
                      <th className="py-3">Students Active / Seats</th>
                      <th className="py-3">Seat Utilization</th>
                      <th className="py-3 text-right">District Calibration Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-zinc-850 font-medium">
                    {!adminKpisData || adminKpisData.campuses.length === 0 ? (
                      <>
                        <tr>
                          <td className="py-3.5 text-white">Central High School</td>
                          <td className="py-3.5">680 / 800 seats</td>
                          <td className="py-3.5">85%</td>
                          <td className="py-3.5 text-right text-emerald-400">Active</td>
                        </tr>
                        <tr>
                          <td className="py-3.5 text-white">Westside Academy</td>
                          <td className="py-3.5">420 / 600 seats</td>
                          <td className="py-3.5">70%</td>
                          <td className="py-3.5 text-right text-emerald-400">Active</td>
                        </tr>
                        <tr>
                          <td className="py-3.5 text-white">Oak Creek High</td>
                          <td className="py-3.5">210 / 400 seats</td>
                          <td className="py-3.5">52.5%</td>
                          <td className="py-3.5 text-right text-emerald-400">Active</td>
                        </tr>
                        <tr>
                          <td className="py-3.5 text-white">Innovation Charter</td>
                          <td className="py-3.5">110 / 200 seats</td>
                          <td className="py-3.5">55%</td>
                          <td className="py-3.5 text-right text-emerald-400">Active</td>
                        </tr>
                      </>
                    ) : (
                      adminKpisData.campuses.map((campus) => (
                        <tr key={campus.id} className="hover:bg-zinc-900/30 transition-colors">
                          <td className="py-3.5 text-white">{campus.name}</td>
                          <td className="py-3.5 font-mono">{campus.students_active} / {campus.seat_limit}</td>
                          <td className="py-3.5">
                            <div className="flex items-center gap-2">
                              <span className="font-mono">{campus.utilization_pct}%</span>
                              <div className="w-16 bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-indigo-500" 
                                  style={{ width: `${campus.utilization_pct}%` }}
                                ></div>
                              </div>
                            </div>
                          </td>
                          <td className="py-3.5 text-right font-sans">
                            <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-semibold text-emerald-400 bg-emerald-500/5 rounded-md border border-emerald-500/10">
                              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                              Active
                            </span>
                          </td>
                        </tr>
                      ))
                    )}
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

      {role === "parent" && (
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-white">Parent Progress Portal</h2>
              <p className="text-sm text-zinc-400">Track your child's OAS biology simulator learning progress, mastery state, and hands-on home labs.</p>
            </div>
            <button
              onClick={fetchParentReport}
              disabled={isLoadingParentReport}
              className="px-3 py-1.5 text-xs font-semibold bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded-lg border border-zinc-700 transition"
            >
              {isLoadingParentReport ? "Refreshing..." : "Refresh Report"}
            </button>
          </div>

          {parentReportError && (
            <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-3 rounded-lg text-xs font-semibold text-center">
              {parentReportError}
            </div>
          )}

          {parentReportData && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column: Student Overview & Mastery */}
              <div className="lg:col-span-2 space-y-6">
                {/* Child Aggregate Profile Card */}
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden shadow-xl">
                  <div className="absolute top-0 right-0 h-40 w-40 bg-indigo-500/5 rounded-full blur-3xl" />
                  <div className="flex items-center gap-4 border-b border-zinc-800/60 pb-5 mb-5">
                    <div className="h-12 w-12 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center font-bold text-lg text-white shadow-lg shadow-indigo-500/20">
                      {parentReportData.child_name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div>
                      <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-wider">Student Profile</span>
                      <h3 className="text-xl font-bold text-white mt-0.5">{parentReportData.child_name}</h3>
                      <p className="text-xs text-zinc-400 mt-0.5">OAS Science standard: B.LS1.1 (DNA & Proteins)</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div className="bg-zinc-950/60 border border-zinc-850 p-4 rounded-xl">
                      <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-wider">OPI Band</span>
                      <div className="mt-1.5">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-bold border ${parentReportData.color_class}`}>
                          {parentReportData.performance_band}
                        </span>
                      </div>
                    </div>
                    <div className="bg-zinc-950/60 border border-zinc-850 p-4 rounded-xl">
                      <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-wider">Predicted Score</span>
                      <div className="text-xl font-black text-white mt-1 font-mono">
                        {parentReportData.opi_score > 0 ? parentReportData.opi_score : "—"}
                      </div>
                    </div>
                    <div className="bg-zinc-950/60 border border-zinc-850 p-4 rounded-xl">
                      <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-wider">Accuracy</span>
                      <div className="text-xl font-black text-white mt-1 font-mono">
                        {parentReportData.accuracy}%
                      </div>
                    </div>
                    <div className="bg-zinc-950/60 border border-zinc-850 p-4 rounded-xl">
                      <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-wider">Avg Speed</span>
                      <div className="text-xl font-black text-white mt-1 font-mono">
                        {parentReportData.avg_time_per_base}s
                      </div>
                    </div>
                  </div>

                  <div className="mt-5 p-4 bg-zinc-950/40 border border-zinc-850 rounded-xl flex items-center justify-between">
                    <div>
                      <span className="text-xs font-bold text-white block">State Test Target Status</span>
                      <span className="text-[11px] text-zinc-500">Target score is 300+ for Proficient.</span>
                    </div>
                    <div>
                      {parentReportData.status_flag === "On Track" ? (
                        <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-emerald-400 bg-emerald-500/5 rounded-lg border border-emerald-500/10">
                          <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping"></span>
                          On Track for Proficiency
                        </span>
                      ) : parentReportData.status_flag === "Needs Support" ? (
                        <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-rose-400 bg-rose-500/5 rounded-lg border border-rose-500/10">
                          <span className="h-1.5 w-1.5 rounded-full bg-rose-500 animate-pulse"></span>
                          Needs Additional Support
                        </span>
                      ) : (
                        <span className="text-zinc-650">—</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Daily Gameplay Time Chart */}
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-zinc-400 mb-6">Daily Gameplay Activity</h3>
                  <div className="flex justify-between items-end h-40 pt-4 border-b border-zinc-800 font-mono">
                    {parentReportData.daily_gameplay.map((day, idx) => (
                      <div key={idx} className="flex flex-col items-center flex-1 group">
                        <span className="text-[10px] text-zinc-500 opacity-0 group-hover:opacity-100 transition-opacity mb-2 font-bold">
                          {day.minutes}m
                        </span>
                        <div 
                          className="w-10 sm:w-12 bg-gradient-to-t from-indigo-600 to-purple-500 rounded-t-lg transition-all duration-500 hover:brightness-125"
                          style={{ height: `${(day.minutes / 20) * 100}px` }}
                        ></div>
                        <span className="text-xs text-zinc-400 mt-2 font-sans font-bold">
                          {day.day}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between text-[10px] text-zinc-500 mt-2 font-mono">
                    <span>Total sessions completed: {parentReportData.total_sessions}</span>
                    <span>Daily recommendation: 10 mins</span>
                  </div>
                </div>
              </div>

              {/* Right Column: Home Labs & Experiment Recommendations */}
              <div className="space-y-6">
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl relative overflow-hidden flex flex-col h-full justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-1">🏡 At-Home Science Connection</h3>
                    <p className="text-xs text-zinc-500 mb-4">
                      Simple hands-on labs you can run together to reinforce the active OAS standard in the kitchen!
                    </p>

                    <div className="space-y-4">
                      {parentReportData.home_activity_cards.map((card, idx) => (
                        <div key={idx} className="bg-zinc-950 border border-zinc-850 p-4 rounded-xl hover:border-zinc-700 transition">
                          <span className="text-[9px] uppercase font-bold text-indigo-400 tracking-wider block">
                            {card.difficulty}
                          </span>
                          <h4 className="text-sm font-bold text-white mt-1">
                            {card.title}
                          </h4>
                          <p className="text-xs text-zinc-400 mt-1.5 leading-relaxed">
                            {card.description}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      )}
      </>
      )}
    </div>
  );
}
