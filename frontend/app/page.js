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

// Codon -> Anticodon Pairing Map (mRNA -> tRNA)
const CODON_ANTICODON_MAP = {
  "AUG": "UAC",
  "CCG": "GGC",
  "AAA": "UUU",
  "UUU": "AAA",
  "GGC": "CCG",
  "UAC": "AUG"
};

// Codon -> Amino Acid Mapping
const CODON_AMINO_ACID_MAP = {
  "AUG": "Methionine (Met)",
  "CCG": "Proline (Pro)",
  "AAA": "Lysine (Lys)",
  "UUU": "Phenylalanine (Phe)",
  "GGC": "Glycine (Gly)",
  "UAC": "Tyrosine (Tyr)"
};

// Reusable SVG BKT Growth Chart Component
const BktGrowthChart = ({ history }) => {
  const [activeTab, setActiveTab] = useState("ALL");

  if (!history || history.length === 0) {
    return (
      <div className="h-44 flex items-center justify-center text-xs text-zinc-500 italic bg-zinc-950/40 rounded-xl border border-dashed border-zinc-850">
        No BKT progression logs recorded yet. Play a level to log mastery growth.
      </div>
    );
  }

  const lsPoints = history.filter(p => p.construct_tag === 'OAS.B.LS1.1');
  const psPoints = history.filter(p => p.construct_tag === 'OAS.B.PS1.1');

  const getPathData = (points) => {
    if (points.length === 0) return { line: "", area: "" };
    const width = 450;
    const height = 150;
    const padding = 25;
    
    const xStep = points.length > 1 ? (width - 2 * padding) / (points.length - 1) : 0;
    
    let path = "";
    let areaPath = "";
    
    points.forEach((p, idx) => {
      const x = padding + idx * xStep;
      const y = height - padding - (p.p_know / 100) * (height - 2 * padding);
      
      if (idx === 0) {
        path += `M ${x} ${y}`;
        areaPath += `M ${x} ${height - padding} L ${x} ${y}`;
      } else {
        path += ` L ${x} ${y}`;
        areaPath += ` L ${x} ${y}`;
      }
      
      if (idx === points.length - 1) {
        areaPath += ` L ${x} ${height - padding} Z`;
      }
    });

    return { line: path, area: areaPath };
  };

  const lsPath = getPathData(lsPoints);
  const psPath = getPathData(psPoints);

  return (
    <div className="bg-zinc-950/60 border border-zinc-850 p-5 rounded-xl space-y-4 shadow-lg">
      <div className="flex justify-between items-center">
        <div>
          <span className="text-[10px] uppercase font-black text-indigo-400 tracking-wider">Mastery Over Time</span>
          <h4 className="text-sm font-bold text-white mt-0.5">BKT Learning Growth Curve</h4>
        </div>
        <div className="flex gap-1.5 bg-zinc-900 p-1 rounded-lg border border-zinc-800 text-[9px]">
          <button
            onClick={() => setActiveTab("ALL")}
            className={`px-2 py-0.5 rounded transition-all font-bold ${activeTab === "ALL" ? "bg-indigo-600 text-white" : "text-zinc-400"}`}
          >
            All
          </button>
          <button
            onClick={() => setActiveTab("LS")}
            className={`px-2 py-0.5 rounded transition-all font-bold ${activeTab === "LS" ? "bg-indigo-600 text-white" : "text-zinc-400"}`}
          >
            B.LS1.1
          </button>
          <button
            onClick={() => setActiveTab("PS")}
            className={`px-2 py-0.5 rounded transition-all font-bold ${activeTab === "PS" ? "bg-indigo-600 text-white" : "text-zinc-400"}`}
          >
            B.PS1.1
          </button>
        </div>
      </div>

      <div className="relative h-40 w-full flex items-center justify-center bg-zinc-950/20 rounded-lg p-2 border border-zinc-900">
        <svg viewBox="0 0 450 150" className="w-full h-full overflow-visible">
          <defs>
            <linearGradient id="lsGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#6366f1" stopOpacity="0.0" />
            </linearGradient>
            <linearGradient id="psGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#14b8a6" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#14b8a6" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Grid Lines */}
          <line x1="25" y1="25" x2="425" y2="25" stroke="#27272a" strokeDasharray="3 3" />
          <line x1="25" y1="75" x2="425" y2="75" stroke="#27272a" strokeDasharray="3 3" />
          <line x1="25" y1="125" x2="425" y2="125" stroke="#27272a" />

          {/* Y Axis Labels */}
          <text x="2" y="28" fill="#71717a" className="text-[8px] font-mono">100%</text>
          <text x="2" y="78" fill="#71717a" className="text-[8px] font-mono">50%</text>
          <text x="2" y="128" fill="#71717a" className="text-[8px] font-mono">0%</text>

          {/* Life Science (B.LS1.1) Line */}
          {(activeTab === "ALL" || activeTab === "LS") && lsPoints.length > 0 && (
            <>
              {lsPath.area && <path d={lsPath.area} fill="url(#lsGrad)" />}
              {lsPath.line && <path d={lsPath.line} fill="none" stroke="#6366f1" strokeWidth="2.5" strokeLinecap="round" />}
              {lsPoints.map((p, idx) => {
                const x = 25 + idx * (lsPoints.length > 1 ? 400 / (lsPoints.length - 1) : 0);
                const y = 150 - 25 - (p.p_know / 100) * 100;
                return (
                  <circle
                    key={`ls-${idx}`}
                    cx={x}
                    cy={y}
                    r="4"
                    fill="#1e1b4b"
                    stroke="#818cf8"
                    strokeWidth="2"
                    className="cursor-pointer hover:scale-125 transition"
                  >
                    <title>{`B.LS1.1: ${p.p_know}%`}</title>
                  </circle>
                );
              })}
            </>
          )}

          {/* Physical Science (B.PS1.1) Line */}
          {(activeTab === "ALL" || activeTab === "PS") && psPoints.length > 0 && (
            <>
              {psPath.area && <path d={psPath.area} fill="url(#psGrad)" />}
              {psPath.line && <path d={psPath.line} fill="none" stroke="#14b8a6" strokeWidth="2.5" strokeLinecap="round" />}
              {psPoints.map((p, idx) => {
                const x = 25 + idx * (psPoints.length > 1 ? 400 / (psPoints.length - 1) : 0);
                const y = 150 - 25 - (p.p_know / 100) * 100;
                return (
                  <circle
                    key={`ps-${idx}`}
                    cx={x}
                    cy={y}
                    r="4"
                    fill="#042f2e"
                    stroke="#2dd4bf"
                    strokeWidth="2"
                    className="cursor-pointer hover:scale-125 transition"
                  >
                    <title>{`B.PS1.1: ${p.p_know}%`}</title>
                  </circle>
                );
              })}
            </>
          )}
        </svg>
      </div>
      <div className="flex justify-between items-center text-[9px] text-zinc-500 font-mono pt-1">
        <span className="flex items-center gap-1"><span className="h-1.5 w-1.5 rounded-full bg-indigo-500"></span> B.LS1.1 (Life Sci)</span>
        <span className="flex items-center gap-1"><span className="h-1.5 w-1.5 rounded-full bg-teal-500"></span> B.PS1.1 (Phys Sci)</span>
      </div>
    </div>
  );
};

// tRNA Anticodon distractor cards palette
const ANTICODON_COLORS = {
  "UAC": "from-emerald-500 to-teal-600 border-teal-500/30 text-white shadow-emerald-500/10",
  "GGC": "from-purple-500 to-indigo-600 border-indigo-500/30 text-white shadow-indigo-500/10",
  "UUU": "from-rose-500 to-pink-600 border-pink-500/30 text-white shadow-rose-500/10",
  "AAA": "from-amber-500 to-orange-600 border-orange-500/30 text-white shadow-orange-500/10"
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
  const [showSyncModal, setShowSyncModal] = useState(false);
  const [syncLogs, setSyncLogs] = useState([]);
  const [isSyncing, setIsSyncing] = useState(false);
  const [classCodeJoin, setClassCodeJoin] = useState("");
  const [classroomInfo, setClassroomInfo] = useState(null);
  const [joinMessage, setJoinMessage] = useState("");
  const [joinError, setJoinError] = useState("");

  // District Admin KPIs State
  const [adminKpisData, setAdminKpisData] = useState(null);
  const [isLoadingAdminKpis, setIsLoadingAdminKpis] = useState(false);
  const [schoolAdminData, setSchoolAdminData] = useState(null);
  const [isLoadingSchoolAdminData, setIsLoadingSchoolAdminData] = useState(false);

  // DNA Template Sequence (B.LS1.1 Target)
  const templateDNA = ["T", "A", "C", "G", "G", "C", "T", "T", "T"];
  
  // Game states
  const [mrnaChain, setMrnaChain] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [errors, setErrors] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [activeLevel, setActiveLevel] = useState(1);
  const [translationIndex, setTranslationIndex] = useState(0);
  const [translationErrors, setTranslationErrors] = useState(0);
  const [translationChain, setTranslationChain] = useState([]);
  const [translationStartTime, setTranslationStartTime] = useState(null);
  const [isTranslationCompleted, setIsTranslationCompleted] = useState(false);
  const [translationFeedbackLog, setTranslationFeedbackLog] = useState([]);
  
  // Level 3 Chemical Bonding States
  const [bondingTarget, setBondingTarget] = useState("H2O"); // "H2O" (covalent) or "NaCl" (ionic)
  const [bondingSharedH1, setBondingSharedH1] = useState(0); // electrons shared by H1 (target: 1)
  const [bondingSharedH2, setBondingSharedH2] = useState(0); // electrons shared by H2 (target: 1)
  const [bondingNaTransfer, setBondingNaTransfer] = useState(false); // electron transferred from Na to Cl
  const [bondingErrors, setBondingErrors] = useState(0);
  const [bondingCompleted, setBondingCompleted] = useState(false);
  const [bondingStartTime, setBondingStartTime] = useState(null);
  const [bondingFeedbackLog, setBondingFeedbackLog] = useState([]);

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
  const [newChildName, setNewChildName] = useState("");
  const [addChildMessage, setAddChildMessage] = useState("");
  const [addChildError, setAddChildError] = useState("");
  const [showAddChildForm, setShowAddChildForm] = useState(false);
  const [parentReportError, setParentReportError] = useState(null);

  // District admin mock upload states
  const [csvFile, setCsvFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [calibrationLogs, setCalibrationLogs] = useState([]);
  const [isCalibrated, setIsCalibrated] = useState(false);

  // Sprint 3 Billing, SSO, Invite States
  const [showMockCheckoutModal, setShowMockCheckoutModal] = useState(false);
  const [mockCheckoutDetails, setMockCheckoutDetails] = useState(null);
  const [showSuccessNotification, setShowSuccessNotification] = useState(false);
  const [successNotificationMessage, setSuccessNotificationMessage] = useState("");
  const [showSsoConsentModal, setShowSsoConsentModal] = useState(false);
  const [ssoDetails, setSsoDetails] = useState(null);

  // Invite states
  const [inviteEmailInput, setInviteEmailInput] = useState("");
  const [inviteCampusIdInput, setInviteCampusIdInput] = useState("");
  const [generatedInviteCode, setGeneratedInviteCode] = useState("");
  const [inviteSuccessMessage, setInviteSuccessMessage] = useState("");
  const [inviteErrorMessage, setInviteErrorMessage] = useState("");

  // Quota adjust states
  const [adjustCampusIdInput, setAdjustCampusIdInput] = useState("");
  const [adjustSeatLimitInput, setAdjustSeatLimitInput] = useState("");
  const [adjustQuotaSuccessMessage, setAdjustQuotaSuccessMessage] = useState("");
  const [adjustQuotaErrorMessage, setAdjustQuotaErrorMessage] = useState("");


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

  // Fetch school admin data when role switches or token changes
  useEffect(() => {
    if (role === "school_admin" && token) {
      fetchSchoolAdminData();
    }
  }, [role, token]);

  // Sprint 3: URL Parameters Processing Hook
  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      
      // Success Notification
      if (params.get("billing_success") === "true") {
        setSuccessNotificationMessage("Success! Your subscription is active. Welcome to Premium!");
        setShowSuccessNotification(true);
        window.history.replaceState({}, document.title, window.location.pathname);
        if (role === "parent") fetchParentReport();
        if (role === "admin") fetchAdminKpis();
        if (role === "school_admin") fetchSchoolAdminData();
      }
      
      // Mock Checkout Simulation
      if (params.get("mock_checkout") === "true") {
        const type = params.get("type");
        const session_id = params.get("session_id");
        const campus_id = params.get("campus_id");
        const seats = params.get("seats");
        const slots = params.get("slots") || 1;
        
        setMockCheckoutDetails({ type, session_id, campus_id, seats, slots });
        setShowMockCheckoutModal(true);
        window.history.replaceState({}, document.title, window.location.pathname);
      }
      
      // Invite Code Prefill
      const inviteCode = params.get("invite_code");
      if (inviteCode) {
        setAuthMode("register");
        setRoleInput("teacher");
        setClassCodeInput(inviteCode);
        window.history.replaceState({}, document.title, window.location.pathname);
      }
      
      // SSO Redirect Login
      if (params.get("sso_login") === "true") {
        const provider = params.get("sso_provider");
        let mockEmail = "sso_student@school.edu";
        let mockFirst = "Sam";
        let mockLast = "Student";
        
        if (provider === "clever") {
          mockEmail = "clever_teacher@okla.edu";
          mockFirst = "Carol";
          mockLast = "Clever";
        }
        
        setSsoDetails({ provider, email: mockEmail, firstName: mockFirst, lastName: mockLast });
        setShowSsoConsentModal(true);
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    }
  }, [role]);


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

  const fetchSchoolAdminData = async () => {
    setIsLoadingSchoolAdminData(true);
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      const response = await fetch("http://localhost:8000/api/reports/school-admin/", { headers });
      if (response.ok) {
        const data = await response.json();
        setSchoolAdminData(data);
      }
    } catch (err) {
      console.warn("Failed to fetch school admin data:", err.message);
    } finally {
      setIsLoadingSchoolAdminData(false);
    }
  };

  const fetchParentReport = async (studentId = null) => {
    setIsLoadingParentReport(true);
    setParentReportError(null);
    try {
      const headers = {};
      if (token) {
        headers["Authorization"] = `Token ${token}`;
      }
      let url = "http://localhost:8000/api/reports/parent/";
      if (studentId) {
        url += `?student_id=${studentId}`;
      }
      const response = await fetch(url, { headers });
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

  const handleBuyAdditionalSlot = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/billing/checkout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": token ? `Token ${token}` : "",
        },
        body: JSON.stringify({ type: "b2c_additional", slots: 1 }),
      });
      if (response.ok) {
        const data = await response.json();
        window.location.href = data.url;
      }
    } catch (err) {
      console.error("Additional B2C Slot Error:", err);
    }
  };

  const handleAddChild = async (e) => {
    e.preventDefault();
    setAddChildError("");
    setAddChildMessage("");
    try {
      const response = await fetch("http://localhost:8000/api/parent/add-child/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": token ? `Token ${token}` : "",
        },
        body: JSON.stringify({ name: newChildName }),
      });
      if (response.ok) {
        const data = await response.json();
        setAddChildMessage(data.message);
        setNewChildName("");
        setShowAddChildForm(false);
        fetchParentReport(data.student_id);
      } else {
        const err = await response.json();
        setAddChildError(err.error || "Failed to link child.");
      }
    } catch (err) {
      setAddChildError("Network error adding child.");
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

  // ==========================================
  // Billing, SSO, Invite Handlers
  // ==========================================

  const handleGoPremium = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/billing/checkout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": token ? `Token ${token}` : "",
        },
        body: JSON.stringify({ type: "b2c" }),
      });
      if (response.ok) {
        const data = await response.json();
        window.location.href = data.url;
      }
    } catch (err) {
      console.error("B2C Billing Error:", err);
    }
  };

  const handleBuySeats = async (campusId, seatsCount) => {
    try {
      const response = await fetch("http://localhost:8000/api/billing/checkout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": token ? `Token ${token}` : "",
        },
        body: JSON.stringify({
          type: "b2b",
          campus_id: campusId,
          seats: seatsCount
        }),
      });
      if (response.ok) {
        const data = await response.json();
        window.location.href = data.url;
      }
    } catch (err) {
      console.error("B2B Billing Error:", err);
    }
  };

  const handleAdjustQuota = async (e) => {
    e.preventDefault();
    setAdjustQuotaSuccessMessage("");
    setAdjustQuotaErrorMessage("");
    if (!adjustCampusIdInput || !adjustSeatLimitInput) return;
    try {
      const response = await fetch("http://localhost:8000/api/admin/campuses/adjust-quota/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": token ? `Token ${token}` : "",
        },
        body: JSON.stringify({
          campus_id: adjustCampusIdInput,
          seat_limit: parseInt(adjustSeatLimitInput, 10)
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setAdjustQuotaSuccessMessage(data.message);
        setAdjustCampusIdInput("");
        setAdjustSeatLimitInput("");
        fetchAdminKpis();
      } else {
        setAdjustQuotaErrorMessage(data.error || "Failed to adjust quota.");
      }
    } catch (err) {
      setAdjustQuotaErrorMessage("Network error adjusting quota.");
    }
  };

  const handleCreateInvite = async (e) => {
    e.preventDefault();
    setInviteSuccessMessage("");
    setInviteErrorMessage("");
    setGeneratedInviteCode("");
    if (!inviteEmailInput || !inviteCampusIdInput) return;
    try {
      const response = await fetch("http://localhost:8000/api/admin/invites/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": token ? `Token ${token}` : "",
        },
        body: JSON.stringify({
          email: inviteEmailInput,
          campus_id: inviteCampusIdInput
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setGeneratedInviteCode(data.code);
        setInviteSuccessMessage(`Created invite for ${data.email} to ${data.campus_name}!`);
        setInviteEmailInput("");
        setInviteCampusIdInput("");
      } else {
        setInviteErrorMessage(data.error || "Failed to generate invite code.");
      }
    } catch (err) {
      setInviteErrorMessage("Network error generating invite code.");
    }
  };

  const handleRegisterInvite = async (e) => {
    e.preventDefault();
    setAuthError("");
    try {
      const response = await fetch("http://localhost:8000/api/auth/register-invite/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: usernameInput,
          password: passwordInput,
          first_name: firstNameInput,
          last_name: lastNameInput,
          invite_code: classCodeInput, // Reused classCodeInput as invite_code field
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setToken(data.token);
        setCurrentUser(data);
        localStorage.setItem("swift_science_token", data.token);
        localStorage.setItem("swift_science_user", JSON.stringify(data));
        setRole(data.role);
        
        setUsernameInput("");
        setPasswordInput("");
        setFirstNameInput("");
        setLastNameInput("");
        setClassCodeInput("");
      } else {
        setAuthError(data.error || "Registration with invite code failed.");
      }
    } catch (err) {
      setAuthError("Failed to connect to backend server.");
    }
  };

  const handleSsoLogin = async (provider) => {
    try {
      const response = await fetch(`http://localhost:8000/api/auth/sso/${provider}/login/`);
      const data = await response.json();
      if (response.ok) {
        window.location.href = data.url;
      }
    } catch (err) {
      console.error("SSO Login Error:", err);
    }
  };

  const handleSsoConsentSubmit = async (e) => {
    e.preventDefault();
    setShowSsoConsentModal(false);
    try {
      const response = await fetch(`http://localhost:8000/api/auth/sso/${ssoDetails.provider}/callback/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: ssoDetails.email,
          first_name: ssoDetails.firstName,
          last_name: ssoDetails.lastName
        })
      });
      const data = await response.json();
      if (response.ok) {
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
        
        setSuccessNotificationMessage(`Successfully logged in via ${ssoDetails.provider === 'google' ? 'Google' : 'Clever'} SSO! Role detected: ${data.role}`);
        setShowSuccessNotification(true);
      } else {
        setAuthError(data.error || "SSO Callback authentication failed.");
      }
    } catch (err) {
      setAuthError("SSO callback network error.");
    }
  };

  const handleMockCheckoutComplete = async () => {
    setShowMockCheckoutModal(false);
    try {
      const response = await fetch("http://localhost:8000/api/billing/webhook/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Mock-Signature": "bypass-sig"
        },
        body: JSON.stringify({
          type: "checkout.session.completed",
          data: {
            object: {
              customer: "cus_mock_" + Math.random().toString(36).substr(2, 9),
              subscription: mockCheckoutDetails.session_id,
              metadata: {
                type: mockCheckoutDetails.type,
                user_id: currentUser ? currentUser.id : null,
                campus_id: mockCheckoutDetails.campus_id,
                seats: mockCheckoutDetails.seats,
                slots: mockCheckoutDetails.slots
              }
            }
          }
        })
      });
      if (response.ok) {
        setSuccessNotificationMessage("Mock checkout successfully simulated! Subscription active.");
        setShowSuccessNotification(true);
        if (role === "parent") fetchParentReport();
        if (role === "admin") fetchAdminKpis();
        if (role === "school_admin") fetchSchoolAdminData();
      } else {
        console.error("Webhook processing error");
      }
    } catch (err) {
      console.error("Failed to connect to webhook", err);
    }
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

  const handleRosterSync = async (provider) => {
    setIsSyncing(true);
    setSyncLogs([]);
    
    const addLog = (msg) => {
      setSyncLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
    };

    addLog(`Initiating roster sync with ${provider === 'google' ? 'Google Classroom' : 'Clever SSO'}...`);
    
    await new Promise(r => setTimeout(r, 800));
    addLog("Authenticating API credentials and exchanging OAuth2 tokens...");
    
    await new Promise(r => setTimeout(r, 1000));
    addLog("Scanning teacher courses and active section enrollments...");

    try {
      const response = await fetch(`http://localhost:8000/api/sync/${provider === 'google' ? 'google-classroom' : 'clever'}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Token ${token}` : ''
        }
      });

      if (response.ok) {
        const data = await response.json();
        await new Promise(r => setTimeout(r, 800));
        addLog(`Successfully synced classroom: "${data.classroom_name}" (Code: ${data.class_code})`);
        
        data.synced_students.forEach(std => {
          addLog(`  -> Synced student: ${std.name} (${std.username}) [${std.created ? 'NEW' : 'EXISTS'}]`);
        });

        addLog("Sync operation completed. Invalidating cache and rebuilding student roster...");
        await fetchTeacherReport();
        addLog("✓ Roster refreshed successfully!");
      } else {
        const errData = await response.json();
        addLog(`❌ Error: ${errData.error || 'Failed to sync with provider API'}`);
      }
    } catch (err) {
      addLog(`❌ Error: Network request failed - ${err.message}`);
    } finally {
      setIsSyncing(false);
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

  const getCodons = () => {
    if (mrnaChain.length < 9) {
      return ["AUG", "CCG", "AAA"];
    }
    const list = [];
    for (let i = 0; i < mrnaChain.length; i += 3) {
      if (i + 3 <= mrnaChain.length) {
        list.push(mrnaChain.slice(i, i + 3).join(""));
      }
    }
    return list;
  };

  const handleCodonMatch = (anticodon) => {
    if (isTranslationCompleted) return;
    
    let currentStartTime = translationStartTime;
    if (translationIndex === 0 && translationChain.length === 0 && !translationStartTime) {
      currentStartTime = Date.now();
      setTranslationStartTime(currentStartTime);
    }

    const codons = getCodons();
    const currentCodon = codons[translationIndex];
    const expectedAnticodon = CODON_ANTICODON_MAP[currentCodon];
    const isCorrect = anticodon === expectedAnticodon;
    
    const newLogEntry = {
      timestamp: new Date().toLocaleTimeString(),
      codon: currentCodon,
      attempt: anticodon,
      status: isCorrect ? "SUCCESS" : "ERROR",
      message: isCorrect 
        ? `Correctly paired tRNA ${anticodon} with mRNA codon ${currentCodon} (Added ${CODON_AMINO_ACID_MAP[currentCodon]})`
        : `Incorrect: tRNA ${anticodon} does not pair with mRNA codon ${currentCodon}`
    };
    
    setTranslationFeedbackLog((prev) => [newLogEntry, ...prev]);

    // Dispatch telemetry event for attempt
    logTelemetryEvent("codon_match_attempt", {
      codon: currentCodon,
      attempted_anticodon: anticodon,
      is_correct: isCorrect,
      cumulative_errors: isCorrect ? translationErrors : translationErrors + 1
    });

    if (isCorrect) {
      const aminoAcid = CODON_AMINO_ACID_MAP[currentCodon];
      const newChain = [...translationChain, aminoAcid];
      setTranslationChain(newChain);

      // Dispatch amino acid added event
      logTelemetryEvent("amino_acid_added", {
        amino_acid: aminoAcid,
        chain: newChain
      });

      if (translationIndex + 1 < codons.length) {
        setTranslationIndex(translationIndex + 1);
      } else {
        setIsTranslationCompleted(true);
        const elapsed = currentStartTime ? Math.round((Date.now() - currentStartTime) / 1000) : 12;
        
        // Dispatch translation complete event
        logTelemetryEvent("translation_complete", {
          total_errors: translationErrors,
          duration_seconds: elapsed,
          amino_acid_chain: newChain
        });
      }
    } else {
      setTranslationErrors((prev) => prev + 1);
    }
  };

  const handleShareElectron = (hydrogenKey, isSharing) => {
    if (bondingCompleted) return;
    
    if (hydrogenKey === "H1") {
      setBondingSharedH1(isSharing ? 1 : 0);
    } else {
      setBondingSharedH2(isSharing ? 1 : 0);
    }
    
    logTelemetryEvent("electron_share_attempt", {
      atom: hydrogenKey,
      is_sharing: isSharing,
      target_atom: "O"
    }, "chemical_bonding_3", "OAS.B.PS1.1");
  };

  const handleTransferElectron = (isTransferred) => {
    if (bondingCompleted) return;
    setBondingNaTransfer(isTransferred);
    
    logTelemetryEvent("electron_share_attempt", {
      atom: "Na",
      is_transferred: isTransferred,
      target_atom: "Cl"
    }, "chemical_bonding_3", "OAS.B.PS1.1");
  };

  const handleValenceReset = () => {
    if (bondingCompleted) return;
    setBondingSharedH1(0);
    setBondingSharedH2(0);
    setBondingNaTransfer(false);
    
    logTelemetryEvent("valence_reset", {
      bonding_target: bondingTarget
    }, "chemical_bonding_3", "OAS.B.PS1.1");
    
    setBondingFeedbackLog((prev) => [{
      timestamp: new Date().toLocaleTimeString(),
      status: "RESET",
      message: "Valence electrons reset to initial shell states."
    }, ...prev]);
  };

  const handleOctetCheck = () => {
    if (bondingCompleted) return;
    
    let isCorrect = false;
    let message = "";
    
    if (bondingTarget === "H2O") {
      isCorrect = bondingSharedH1 === 1 && bondingSharedH2 === 1;
      message = isCorrect
        ? "✓ Success: Covalent bonds stable! Oxygen central octet (8) and Hydrogen duets (2) fully satisfied."
        : "Failed: Valence shell unstable. Oxygen needs 8 valence electrons, Hydrogens need 2. Adjust shared electrons.";
    } else {
      isCorrect = bondingNaTransfer === true;
      message = isCorrect
        ? "✓ Success: Ionic bond stable! Na+ cation and Cl- anion electrostatic attraction satisfied."
        : "Failed: Valence shell unstable. Sodium (Na) must transfer its 1 valence electron to Chlorine (Cl).";
    }
    
    const newLogEntry = {
      timestamp: new Date().toLocaleTimeString(),
      status: isCorrect ? "SUCCESS" : "ERROR",
      message: message
    };
    setBondingFeedbackLog((prev) => [newLogEntry, ...prev]);
    
    logTelemetryEvent("octet_rule_check", {
      bonding_target: bondingTarget,
      is_correct: isCorrect,
      shared_h1: bondingSharedH1,
      shared_h2: bondingSharedH2,
      na_transfer: bondingNaTransfer
    }, "chemical_bonding_3", "OAS.B.PS1.1");
    
    if (isCorrect) {
      setBondingCompleted(true);
      logTelemetryEvent("bond_completed", {
        compound: bondingTarget,
        bond_type: bondingTarget === "H2O" ? "covalent" : "ionic"
      }, "chemical_bonding_3", "OAS.B.PS1.1");
    } else {
      setBondingErrors((prev) => prev + 1);
    }
  };

  const handleSubmitBondingSimulation = async () => {
    const durationLevel1 = startTime ? (Date.now() - startTime) / 1000 : 0.0;
    const accuracyLevel1 = mrnaChain.length + errors > 0
      ? Math.round((mrnaChain.length / (mrnaChain.length + errors)) * 100)
      : 100;

    const durationLevel2 = translationStartTime ? (Date.now() - translationStartTime) / 1000 : 0.0;
    const accuracyLevel2 = translationChain.length + translationErrors > 0
      ? Math.round((translationIndex / (translationIndex + translationErrors)) * 100)
      : 100;

    const durationLevel3 = bondingStartTime ? (Date.now() - bondingStartTime) / 1000 : 0.0;
    const accuracyLevel3 = bondingErrors === 0 ? 100 : Math.round((1 / (1 + bondingErrors)) * 100);

    await logTelemetryEvent("session_complete", {
      transcription: {
        total_errors: errors,
        accuracy: accuracyLevel1,
        duration_seconds: parseFloat(durationLevel1.toFixed(2))
      },
      translation: {
        total_errors: translationErrors,
        accuracy: accuracyLevel2,
        duration_seconds: parseFloat(durationLevel2.toFixed(2))
      },
      bonding: {
        total_errors: bondingErrors,
        accuracy: accuracyLevel3,
        duration_seconds: parseFloat(durationLevel3.toFixed(2))
      },
      total_errors: errors + translationErrors + bondingErrors,
      duration_seconds: parseFloat((durationLevel1 + durationLevel2 + durationLevel3).toFixed(2))
    }, "chemical_bonding_3", "OAS.B.PS1.1");

    setIsSubmitted(true);
    if (classroomInfo) {
      fetchTeacherReport();
    }
    fetchParentReport();
  };

  // Log events locally for developer visualization and dispatch to Django backend
  const logTelemetryEvent = async (eventType, payload, levelId = "dna_transcription_1", constructTag = "OAS.B.LS1.1") => {
    const newEvent = {
      event_id: typeof window !== "undefined" ? crypto.randomUUID() : `evt_${Math.random().toString(36).substr(2, 9)}`,
      student_id: selectedStudent.id,   // Dynamic UUID
      session_id: sessionId,           // Dynamic Session UUID
      timestamp: new Date().toISOString(),
      event_type: eventType,
      level_id: levelId,
      construct_tag: constructTag,
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
    const durationLevel1 = startTime ? (Date.now() - startTime) / 1000 : 0.0;
    const accuracyLevel1 = mrnaChain.length + errors > 0
      ? Math.round((mrnaChain.length / (mrnaChain.length + errors)) * 100)
      : 100;

    const durationLevel2 = translationStartTime ? (Date.now() - translationStartTime) / 1000 : 0.0;
    const accuracyLevel2 = translationChain.length + translationErrors > 0
      ? Math.round((translationChain.length / (translationChain.length + translationErrors)) * 100)
      : 100;

    await logTelemetryEvent("session_complete", {
      transcription: {
        total_errors: errors,
        accuracy: accuracyLevel1,
        duration_seconds: parseFloat(durationLevel1.toFixed(2))
      },
      translation: {
        total_errors: translationErrors,
        accuracy: accuracyLevel2,
        duration_seconds: parseFloat(durationLevel2.toFixed(2))
      },
      total_errors: errors + translationErrors,
      duration_seconds: parseFloat((durationLevel1 + durationLevel2).toFixed(2))
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
    setActiveLevel(1);
    setTranslationIndex(0);
    setTranslationErrors(0);
    setTranslationChain([]);
    setTranslationStartTime(null);
    setIsTranslationCompleted(false);
    setTranslationFeedbackLog([]);
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
      {/* Notifications & Modals */}
      {showSuccessNotification && (
        <div className="bg-emerald-600 text-white px-6 py-3 flex justify-between items-center text-xs font-bold shadow-xl sticky top-0 z-[100] border-b border-emerald-500/20">
          <span className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-white animate-ping"></span>
            {successNotificationMessage}
          </span>
          <button onClick={() => setShowSuccessNotification(false)} className="hover:text-emerald-200 font-bold ml-4">✕</button>
        </div>
      )}

      {showSyncModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6 z-[110]">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
              <div className="flex items-center gap-2">
                <span className="text-xl">🔄</span>
                <h3 className="text-lg font-bold text-white">SSO Roster Sync Integrator</h3>
              </div>
              <button 
                onClick={() => { if (!isSyncing) setShowSyncModal(false); }}
                className="text-zinc-500 hover:text-zinc-300 font-bold"
                disabled={isSyncing}
              >
                ✕
              </button>
            </div>
            
            <p className="text-xs text-zinc-400 leading-relaxed">
              Connect to your external district classroom rosters to automatically import students, assign accounts, and manage license seating assignments.
            </p>

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => handleRosterSync('google')}
                disabled={isSyncing}
                className="p-4 bg-zinc-950 hover:bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col items-center justify-center gap-2 transition disabled:opacity-50"
              >
                <span className="text-xl">🏫</span>
                <span className="text-xs font-bold text-white">Google Classroom</span>
              </button>
              <button
                onClick={() => handleRosterSync('clever')}
                disabled={isSyncing}
                className="p-4 bg-zinc-950 hover:bg-zinc-900 border border-zinc-800 rounded-xl flex flex-col items-center justify-center gap-2 transition disabled:opacity-50"
              >
                <span className="text-xl">🦊</span>
                <span className="text-xs font-bold text-white">Clever Sections</span>
              </button>
            </div>

            {/* Sync Progress Console Logs */}
            {syncLogs.length > 0 && (
              <div className="bg-black/60 border border-zinc-850 p-4 rounded-lg font-mono text-[10px] text-indigo-300 h-40 overflow-y-auto space-y-1">
                {syncLogs.map((log, idx) => (
                  <div key={idx}>{log}</div>
                ))}
                {isSyncing && (
                  <div className="text-zinc-500 animate-pulse mt-1">
                    ⚡ Running background sync operation...
                  </div>
                )}
              </div>
            )}

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setShowSyncModal(false)}
                disabled={isSyncing}
                className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50 text-zinc-300 font-bold rounded-lg text-xs uppercase tracking-wider transition"
              >
                Close Dialog
              </button>
            </div>
          </div>
        </div>
      )}

      {showMockCheckoutModal && mockCheckoutDetails && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6 z-[110]">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center gap-2 border-b border-zinc-800 pb-3">
              <span className="text-xl">💳</span>
              <h3 className="text-lg font-bold text-white">Stripe Checkout Simulator</h3>
            </div>
            <p className="text-xs text-zinc-400 leading-relaxed">
              You are simulating a Stripe redirect for a <strong>
                {mockCheckoutDetails.type === 'b2c' 
                  ? 'B2C Family Premium Subscription' 
                  : mockCheckoutDetails.type === 'b2c_additional'
                    ? 'B2C Additional Household Child Slot'
                    : 'B2B School/District Seat Quota'}
              </strong>.
            </p>
            {mockCheckoutDetails.type === 'b2b' && (
              <div className="bg-zinc-950 p-3 rounded-lg border border-zinc-850 text-xs text-zinc-400 font-mono">
                <p>Campus ID: <span className="text-indigo-400">{mockCheckoutDetails.campus_id}</span></p>
                <p className="mt-1">Seats: <span className="text-white font-bold">{mockCheckoutDetails.seats}</span> ($6.00 / seat / year)</p>
              </div>
            )}
            {mockCheckoutDetails.type === 'b2c_additional' && (
              <div className="bg-zinc-950 p-3 rounded-lg border border-zinc-850 text-xs text-zinc-400 font-mono">
                <p>Additional Slots: <span className="text-white font-bold">{mockCheckoutDetails.slots}</span> ($30.00 / slot / year)</p>
              </div>
            )}
            <div className="flex gap-3 pt-2">
              <button
                onClick={handleMockCheckoutComplete}
                className="flex-1 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-xs uppercase tracking-wider transition-all"
              >
                Simulate Payment Success
              </button>
              <button
                onClick={() => setShowMockCheckoutModal(false)}
                className="flex-1 py-2 bg-zinc-850 hover:bg-zinc-800 text-zinc-400 font-bold rounded-lg text-xs uppercase tracking-wider transition-all"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {showSsoConsentModal && ssoDetails && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6 z-[110]">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center gap-3 border-b border-zinc-800 pb-3">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-sm font-bold text-white">
                {ssoDetails.provider === 'google' ? 'G' : 'C'}
              </div>
              <h3 className="text-lg font-bold text-white">Authorize {ssoDetails.provider === 'google' ? 'Google' : 'Clever'} SSO</h3>
            </div>
            <p className="text-xs text-zinc-400 leading-relaxed">
              Confirm your de-identified profile metadata to complete registration and log in:
            </p>
            
            <form onSubmit={handleSsoConsentSubmit} className="space-y-3">
              <div>
                <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">SSO Email Address</label>
                <input
                  type="email"
                  value={ssoDetails.email}
                  onChange={(e) => setSsoDetails({ ...ssoDetails, email: e.target.value })}
                  required
                  className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                />
                <span className="text-[9px] text-zinc-500 block mt-1">
                  * Role detection: email containing 'admin' $\rightarrow$ Admin; ends in '.edu' or containing 'teacher' $\rightarrow$ Teacher; else $\rightarrow$ Student.
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">First Name</label>
                  <input
                    type="text"
                    value={ssoDetails.firstName}
                    onChange={(e) => setSsoDetails({ ...ssoDetails, firstName: e.target.value })}
                    required
                    className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>
                <div>
                  <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Last Name</label>
                  <input
                    type="text"
                    value={ssoDetails.lastName}
                    onChange={(e) => setSsoDetails({ ...ssoDetails, lastName: e.target.value })}
                    required
                    className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>
              </div>
              
              <div className="flex gap-3 pt-3">
                <button
                  type="submit"
                  className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs uppercase tracking-wider transition-all"
                >
                  Agree & Connect
                </button>
                <button
                  type="button"
                  onClick={() => setShowSsoConsentModal(false)}
                  className="flex-1 py-2 bg-zinc-850 hover:bg-zinc-800 text-zinc-400 font-bold rounded-lg text-xs uppercase tracking-wider transition-all"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

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
            {currentUser.role === "school_admin" && (
              <button
                onClick={() => setRole("school_admin")}
                className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                  role === "school_admin"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                School Admin Portal
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

            <form onSubmit={authMode === "login" ? handleLogin : (roleInput === "teacher" && classCodeInput ? handleRegisterInvite : handleRegister)} className="space-y-4">
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
                      className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors bg-zinc-900"
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

                  {roleInput === "teacher" && (
                    <div>
                      <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Invitation Code</label>
                      <input
                        type="text"
                        value={classCodeInput}
                        onChange={(e) => setClassCodeInput(e.target.value)}
                        placeholder="e.g. TCH-ABCD-1234"
                        required
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

            <div className="relative my-4 flex items-center justify-center">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-zinc-800" />
              </div>
              <span className="relative bg-zinc-900 px-3 text-[10px] uppercase font-bold text-zinc-500">Or Continue With</span>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-4">
              <button
                type="button"
                onClick={() => handleSsoLogin('google')}
                className="flex items-center justify-center gap-2 py-2 px-3 bg-zinc-950 hover:bg-zinc-800 border border-zinc-850 rounded-lg text-xs font-bold text-zinc-200 transition-all hover:scale-[1.02]"
              >
                <svg className="h-4 w-4" viewBox="0 0 24 24">
                  <path fill="#EA4335" d="M12.24 10.285V14.4h6.887c-.648 2.41-2.519 4.114-5.136 4.114A5.99 5.99 0 0 1 8 12.5a5.99 5.99 0 0 1 5.99-6.012c1.49 0 2.858.547 3.916 1.448l3.137-3.137C19.123 2.99 16.742 2 13.99 2A9.99 9.99 0 0 0 4 11.99 9.99 9.99 0 0 0 13.99 22c5.99 0 9.873-4.14 9.873-10.05 0-.674-.06-1.258-.19-1.665H12.24Z"/>
                </svg>
                Google
              </button>
              <button
                type="button"
                onClick={() => handleSsoLogin('clever')}
                className="flex items-center justify-center gap-2 py-2 px-3 bg-zinc-950 hover:bg-zinc-850 border border-zinc-850 rounded-lg text-xs font-bold text-zinc-200 transition-all hover:scale-[1.02]"
              >
                <span className="text-sky-400 font-black text-sm tracking-tighter mr-1">C</span>
                Clever
              </button>
            </div>

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
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
          {joinError && joinError.includes("Seat limit") && (
            <div className="bg-rose-500/10 border border-rose-500/30 text-rose-450 p-4 rounded-2xl flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <span className="text-xl">⚠️</span>
                <div>
                  <h4 className="text-sm font-bold text-white">Campus Seat License Limit Reached</h4>
                  <p className="text-xs text-zinc-400 mt-0.5">Your campus has exceeded its active seat quota. Please contact your district administrator to purchase additional seats.</p>
                </div>
              </div>
              <button 
                onClick={() => setJoinError("")}
                className="px-3 py-1 bg-zinc-850 hover:bg-zinc-800 text-zinc-300 text-xs font-bold rounded-lg border border-zinc-700 transition shrink-0"
              >
                Dismiss
              </button>
            </div>
          )}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
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
                  {/* Level Tabs Selector */}
                  <div className="flex gap-4 mb-6 border-b border-zinc-800 pb-2">
                    <button
                      onClick={() => setActiveLevel(1)}
                      className={`pb-2 text-sm font-bold uppercase tracking-wider transition-all border-b-2 ${
                        activeLevel === 1
                          ? "text-indigo-400 border-indigo-500"
                          : "text-zinc-500 border-transparent hover:text-zinc-300"
                      }`}
                    >
                      Level 1: Transcription
                    </button>
                    <button
                      onClick={() => {
                        if (isCompleted) {
                          setActiveLevel(2);
                        }
                      }}
                      disabled={!isCompleted}
                      className={`pb-2 text-sm font-bold uppercase tracking-wider transition-all border-b-2 flex items-center gap-1.5 ${
                        activeLevel === 2
                          ? "text-indigo-400 border-indigo-500"
                          : !isCompleted
                          ? "text-zinc-650 border-transparent cursor-not-allowed"
                          : "text-zinc-500 border-transparent hover:text-zinc-300"
                      }`}
                    >
                      Level 2: Translation
                      {!isCompleted && <span className="text-[9px] bg-zinc-800 text-zinc-500 px-1.5 py-0.5 rounded font-black">LOCKED</span>}
                    </button>
                    <button
                      onClick={() => {
                        if (isTranslationCompleted) {
                          setActiveLevel(3);
                          if (!bondingStartTime) {
                            setBondingStartTime(Date.now());
                            logTelemetryEvent("level_start", { bondingTarget: "H2O" }, "chemical_bonding_3", "OAS.B.PS1.1");
                          }
                        }
                      }}
                      disabled={!isTranslationCompleted}
                      className={`pb-2 text-sm font-bold uppercase tracking-wider transition-all border-b-2 flex items-center gap-1.5 ${
                        activeLevel === 3
                          ? "text-indigo-400 border-indigo-500"
                          : !isTranslationCompleted
                          ? "text-zinc-650 border-transparent cursor-not-allowed"
                          : "text-zinc-500 border-transparent hover:text-zinc-300"
                      }`}
                    >
                      Level 3: Bonding
                      {!isTranslationCompleted && <span className="text-[9px] bg-zinc-800 text-zinc-500 px-1.5 py-0.5 rounded font-black">LOCKED</span>}
                    </button>
                  </div>

                  {activeLevel === 1 && (
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
                              ✓ DNA Strand fully transcribed into mRNA transcript!
                            </p>
                            <button
                              onClick={() => setActiveLevel(2)}
                              className="px-8 py-3.5 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-450 hover:to-purple-500 text-white font-bold rounded-xl shadow-lg shadow-indigo-500/20 transform hover:scale-105 transition-all duration-300 active:scale-95 text-xs uppercase tracking-wider"
                            >
                              Proceed to Level 2: Translation →
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

                  {activeLevel === 2 && (
                    <>
                      {/* Level 2 Progress Cards */}
                      <div className="grid grid-cols-3 gap-4 mb-8">
                        <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                          <span className="text-xs text-zinc-500">Translation Progress</span>
                          <div className="text-lg font-bold text-white mt-0.5">
                            {translationIndex} / {getCodons().length}
                          </div>
                        </div>
                        <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                          <span className="text-xs text-zinc-500">Translation Errors</span>
                          <div className={`text-lg font-bold mt-0.5 ${translationErrors > 0 ? "text-rose-400" : "text-emerald-400"}`}>
                            {translationErrors}
                          </div>
                        </div>
                        <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                          <span className="text-xs text-zinc-500">Accuracy</span>
                          <div className="text-lg font-bold text-white mt-0.5">
                            {translationIndex + translationErrors > 0
                              ? `${Math.round((translationIndex / (translationIndex + translationErrors)) * 100)}%`
                              : "100%"}
                          </div>
                        </div>
                      </div>

                      {/* Codon translation screen */}
                      <div className="space-y-8 bg-zinc-950/80 border border-zinc-850 p-6 rounded-2xl mb-8">
                        {/* mRNA template codons */}
                        <div>
                          <div className="text-xs font-semibold text-zinc-500 mb-3 uppercase tracking-wide">
                            {"Ribosome Translation Site (mRNA -> tRNA)"}
                          </div>
                          <div className="flex justify-center items-center gap-8 py-6 bg-zinc-900/40 rounded-xl border border-zinc-800 relative">
                            {/* Ribosome illustration */}
                            <div className="absolute inset-x-0 h-10 bg-indigo-950/20 border-y border-indigo-900/30 flex items-center justify-center text-[10px] uppercase font-bold text-indigo-400/60 tracking-widest select-none">
                              Ribosome A-Site
                            </div>
                            
                            {getCodons().map((codon, idx) => {
                              const isCurrent = idx === translationIndex && !isTranslationCompleted;
                              const isDone = idx < translationIndex;
                              return (
                                <div
                                  key={idx}
                                  className={`z-10 h-16 w-20 rounded-xl flex flex-col justify-center items-center font-bold text-base border transition-all ${
                                    isCurrent
                                      ? "bg-indigo-900/40 border-indigo-500 scale-110 shadow-lg shadow-indigo-500/20 ring-2 ring-indigo-500/30"
                                      : isDone
                                      ? "bg-zinc-950 border-zinc-800 text-zinc-550 line-through animate-pulse"
                                      : "bg-zinc-900 border-zinc-800 text-zinc-500"
                                  }`}
                                >
                                  <span className="text-[10px] text-zinc-650 font-bold mb-1">Codon {idx + 1}</span>
                                  {codon}
                                </div>
                              );
                            })}
                          </div>
                        </div>

                        {/* Growing Amino Acid Chain */}
                        <div>
                          <div className="text-xs font-semibold text-zinc-500 mb-2 uppercase tracking-wide">
                            Growing Peptide Chain (Protein Synthesis)
                          </div>
                          <div className="h-16 bg-zinc-950 p-4 rounded-xl border border-zinc-850 flex items-center gap-3 overflow-x-auto">
                            {translationChain.length === 0 ? (
                              <span className="text-zinc-600 text-xs italic">No amino acids linked yet. Pair tRNA to start chain.</span>
                            ) : (
                              translationChain.map((aa, idx) => (
                                <React.Fragment key={idx}>
                                  <div className="px-3 py-1.5 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-lg text-xs font-bold text-white shadow-md shadow-emerald-500/10 flex items-center gap-1.5 animate-bounce">
                                    <span className="h-2 w-2 rounded-full bg-white/80 animate-ping" />
                                    {aa}
                                  </div>
                                  {idx < translationChain.length - 1 && (
                                    <span className="text-indigo-400 font-bold text-sm">✦</span>
                                  )}
                                </React.Fragment>
                              ))
                            )}
                          </div>
                        </div>
                      </div>

                      {/* tRNA anticodon matching controls */}
                      <div className="bg-zinc-950/40 border border-zinc-800/60 p-6 rounded-2xl text-center">
                        {isTranslationCompleted ? (
                          <div className="space-y-4 py-2 flex flex-col items-center justify-center">
                            <p className="text-sm text-emerald-400 font-semibold animate-pulse">
                              ✓ Protein translation complete! 3-letter amino acid chain synthesized successfully.
                            </p>
                            <div className="flex gap-4">
                              <button
                                onClick={() => {
                                  setActiveLevel(3);
                                  if (!bondingStartTime) {
                                    setBondingStartTime(Date.now());
                                    logTelemetryEvent("level_start", { bondingTarget: "H2O" }, "chemical_bonding_3", "OAS.B.PS1.1");
                                  }
                                }}
                                className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-450 hover:to-purple-500 text-white font-bold rounded-xl shadow-lg shadow-indigo-500/20 transform hover:scale-105 transition-all duration-300 active:scale-95 text-xs uppercase tracking-wider"
                              >
                                Proceed to Level 3: Chemical Bonding →
                              </button>
                              <button
                                onClick={handleSubmitSimulation}
                                className="px-6 py-3 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold rounded-xl border border-zinc-700 transform hover:scale-105 transition-all duration-300 active:scale-95 text-xs uppercase tracking-wider"
                              >
                                Submit & Exit
                              </button>
                            </div>
                          </div>
                        ) : (
                          <>
                            <p className="text-sm text-zinc-400 mb-5 font-medium">
                              Select the matching tRNA anticodon to bind with mRNA codon <strong className="text-white font-mono">{getCodons()[translationIndex]}</strong>:
                            </p>

                            <div className="flex flex-wrap justify-center gap-4">
                              {["UAC", "GGC", "UUU", "AAA"].map((anticodon) => (
                                <button
                                  key={anticodon}
                                  onClick={() => handleCodonMatch(anticodon)}
                                  className={`h-20 w-24 rounded-xl border flex flex-col justify-center items-center font-bold text-xs bg-gradient-to-b transition-all transform hover:scale-105 active:scale-95 shadow-md ${ANTICODON_COLORS[anticodon] || 'from-zinc-800 to-zinc-900 border-zinc-700 text-zinc-400'}`}
                                >
                                  <span className="text-[9px] opacity-75 font-bold mb-1">tRNA anticodon</span>
                                  <span className="text-sm font-black tracking-wider">{anticodon}</span>
                                  <span className="text-[8px] mt-1 text-white/80 font-bold bg-black/20 px-1 py-0.5 rounded">
                                    {anticodon === "UAC" ? "Met" : anticodon === "GGC" ? "Pro" : anticodon === "UUU" ? "Lys" : "Phe"}
                                  </span>
                                </button>
                              ))}
                            </div>
                          </>
                        )}
                      </div>
                    </>
                  )}

                  {activeLevel === 3 && (
                    <>
                      {/* Level 3 Progress Cards */}
                      <div className="grid grid-cols-3 gap-4 mb-8">
                        <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                          <span className="text-xs text-zinc-500">Target Standard</span>
                          <div className="text-lg font-bold text-white mt-0.5 font-mono">
                            OAS B.PS1.1
                          </div>
                        </div>
                        <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                          <span className="text-xs text-zinc-500">Errors Logged</span>
                          <div className={`text-lg font-bold mt-0.5 ${bondingErrors > 0 ? "text-rose-400" : "text-emerald-400"}`}>
                            {bondingErrors}
                          </div>
                        </div>
                        <div className="bg-zinc-950/60 border border-zinc-800/80 p-3.5 rounded-xl text-center">
                          <span className="text-xs text-zinc-500">Stability</span>
                          <div className="text-lg font-bold text-white mt-0.5">
                            {bondingCompleted ? (
                              <span className="text-emerald-400 font-bold">STABLE</span>
                            ) : (
                              <span className="text-amber-500 font-bold animate-pulse">UNSTABLE</span>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Compound selection tabs */}
                      <div className="bg-zinc-950/80 border border-zinc-850 p-6 rounded-2xl mb-8 space-y-6">
                        <div className="flex justify-between items-center border-b border-zinc-850 pb-4">
                          <div>
                            <span className="text-[10px] uppercase font-black text-indigo-400 tracking-wider">Level 3: Chemical Bonding Puzzle</span>
                            <h3 className="text-sm font-bold text-white mt-0.5">Satisfy the Octet Rule</h3>
                          </div>
                          <div className="flex gap-2 bg-zinc-900 p-1 rounded-lg border border-zinc-800">
                            <button
                              onClick={() => {
                                if (!bondingCompleted) {
                                  setBondingTarget("H2O");
                                  logTelemetryEvent("level_start", { bondingTarget: "H2O" }, "chemical_bonding_3", "OAS.B.PS1.1");
                                }
                              }}
                              className={`px-3 py-1.5 rounded-md text-xs font-bold transition ${
                                bondingTarget === "H2O"
                                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/10"
                                  : "text-zinc-400 hover:text-zinc-200"
                              }`}
                            >
                              Water (H₂O) Covalent
                            </button>
                            <button
                              onClick={() => {
                                if (!bondingCompleted) {
                                  setBondingTarget("NaCl");
                                  logTelemetryEvent("level_start", { bondingTarget: "NaCl" }, "chemical_bonding_3", "OAS.B.PS1.1");
                                }
                              }}
                              className={`px-3 py-1.5 rounded-md text-xs font-bold transition ${
                                bondingTarget === "NaCl"
                                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/10"
                                  : "text-zinc-400 hover:text-zinc-200"
                              }`}
                            >
                              Salt (NaCl) Ionic
                            </button>
                          </div>
                        </div>

                        {/* Interactive Bonding Canvas */}
                        <div className="bg-zinc-950/40 p-6 rounded-xl border border-zinc-850 flex flex-col items-center justify-center min-h-[220px]">
                          {bondingTarget === "H2O" ? (
                            // Covalent Water
                            <div className="w-full space-y-6">
                              <div className="flex justify-center items-center gap-12">
                                {/* H1 Atom */}
                                <div className="flex flex-col items-center gap-3">
                                  <div className="h-14 w-14 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-white font-black text-sm relative">
                                    H₁
                                    {/* Electron shell representation */}
                                    <div className="absolute -inset-2.5 rounded-full border border-dashed border-zinc-700/50 flex items-center justify-center">
                                      {bondingSharedH1 === 0 && (
                                        <span className="absolute right-0 top-1/2 -translate-y-1/2 h-2 w-2 rounded-full bg-indigo-400 shadow shadow-indigo-500" />
                                      )}
                                    </div>
                                  </div>
                                  <button
                                    onClick={() => handleShareElectron("H1", bondingSharedH1 === 0)}
                                    className={`px-3 py-1 text-[10px] font-bold rounded-lg transition ${
                                      bondingSharedH1 === 1
                                        ? "bg-indigo-650/40 border border-indigo-500 text-indigo-300"
                                        : "bg-zinc-800 hover:bg-zinc-700 text-zinc-300"
                                    }`}
                                  >
                                    {bondingSharedH1 === 1 ? "Shared ✓" : "Share Electron"}
                                  </button>
                                </div>

                                {/* Oxygen central atom */}
                                <div className="h-24 w-24 rounded-full bg-gradient-to-tr from-indigo-950/50 to-indigo-900/20 border-2 border-indigo-650 flex flex-col items-center justify-center text-white font-black text-xl relative shadow-lg shadow-indigo-500/5">
                                  O
                                  <span className="text-[9px] text-indigo-400 font-bold mt-1 font-mono">
                                    Valence: {6 + bondingSharedH1 + bondingSharedH2}
                                  </span>

                                  {/* Valence electrons representations */}
                                  <div className="absolute top-1 right-1/2 translate-x-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                  <div className="absolute bottom-1 right-1/2 translate-x-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                  <div className="absolute left-1 top-1/2 -translate-y-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                  <div className="absolute right-1 top-1/2 -translate-y-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                  
                                  {/* Sharing regions */}
                                  {bondingSharedH1 === 1 && (
                                    <div className="absolute -left-5 top-1/2 -translate-y-1/2 flex gap-1">
                                      <span className="h-2 w-2 rounded-full bg-indigo-400" />
                                      <span className="h-2 w-2 rounded-full bg-indigo-500" />
                                    </div>
                                  )}
                                  {bondingSharedH2 === 1 && (
                                    <div className="absolute -right-5 top-1/2 -translate-y-1/2 flex gap-1">
                                      <span className="h-2 w-2 rounded-full bg-indigo-500" />
                                      <span className="h-2 w-2 rounded-full bg-indigo-400" />
                                    </div>
                                  )}
                                </div>

                                {/* H2 Atom */}
                                <div className="flex flex-col items-center gap-3">
                                  <div className="h-14 w-14 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-white font-black text-sm relative">
                                    H₂
                                    <div className="absolute -inset-2.5 rounded-full border border-dashed border-zinc-700/50 flex items-center justify-center">
                                      {bondingSharedH2 === 0 && (
                                        <span className="absolute left-0 top-1/2 -translate-y-1/2 h-2 w-2 rounded-full bg-indigo-400 shadow shadow-indigo-500" />
                                      )}
                                    </div>
                                  </div>
                                  <button
                                    onClick={() => handleShareElectron("H2", bondingSharedH2 === 0)}
                                    className={`px-3 py-1 text-[10px] font-bold rounded-lg transition ${
                                      bondingSharedH2 === 1
                                        ? "bg-indigo-650/40 border border-indigo-500 text-indigo-300"
                                        : "bg-zinc-800 hover:bg-zinc-700 text-zinc-300"
                                    }`}
                                  >
                                    {bondingSharedH2 === 1 ? "Shared ✓" : "Share Electron"}
                                  </button>
                                </div>
                              </div>
                              <p className="text-[11px] text-zinc-500 text-center max-w-sm mx-auto leading-relaxed">
                                Hydrogens have 1 valence electron each. Oxygen has 6. Share 1 electron from each Hydrogen into the central Oxygen's valence shell to form single covalent bonds.
                              </p>
                            </div>
                          ) : (
                            // Ionic Salt
                            <div className="w-full space-y-6">
                              <div className="flex justify-center items-center gap-16">
                                {/* Sodium cation */}
                                <div className="flex flex-col items-center gap-3">
                                  <div className="h-16 w-16 rounded-full bg-zinc-900 border border-zinc-850 flex flex-col items-center justify-center text-white font-black text-base relative">
                                    Na
                                    <span className="text-[9px] text-zinc-550 font-bold font-mono">
                                      {bondingNaTransfer ? "+" : "Valence: 1"}
                                    </span>
                                    {!bondingNaTransfer && (
                                      <span className="absolute -top-1.5 left-1/2 -translate-x-1/2 h-2 w-2 rounded-full bg-indigo-400 shadow shadow-indigo-500" />
                                    )}
                                  </div>
                                  <button
                                    onClick={() => handleTransferElectron(!bondingNaTransfer)}
                                    className={`px-3 py-1 text-[10px] font-bold rounded-lg transition ${
                                      bondingNaTransfer
                                        ? "bg-indigo-650/40 border border-indigo-500 text-indigo-300"
                                        : "bg-zinc-800 hover:bg-zinc-700 text-zinc-300"
                                    }`}
                                  >
                                    {bondingNaTransfer ? "Transferred ✓" : "Transfer Electron"}
                                  </button>
                                </div>

                                {/* Chlorine anion */}
                                <div className="flex flex-col items-center gap-3">
                                  <div className="h-20 w-20 rounded-full bg-gradient-to-tr from-zinc-900 to-zinc-950 border-2 border-zinc-800 flex flex-col items-center justify-center text-white font-black text-base relative">
                                    Cl
                                    <span className="text-[9px] text-zinc-500 font-bold font-mono">
                                      {bondingNaTransfer ? "-" : "Valence: 7"}
                                    </span>
                                    
                                    <div className="absolute top-1 right-1/2 translate-x-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                    <div className="absolute bottom-1 right-1/2 translate-x-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                    <div className="absolute left-1 top-1/2 -translate-y-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                    <div className="absolute right-1 top-1/2 -translate-y-1/2 h-2 w-2 rounded-full bg-indigo-500" />
                                    <div className="absolute top-3.5 left-3.5 h-2 w-2 rounded-full bg-indigo-500" />
                                    <div className="absolute top-3.5 right-3.5 h-2 w-2 rounded-full bg-indigo-500" />
                                    <div className="absolute bottom-3.5 left-3.5 h-2 w-2 rounded-full bg-indigo-500" />
                                    {bondingNaTransfer && (
                                      <div className="absolute bottom-3.5 right-3.5 h-2 w-2 rounded-full bg-indigo-400 shadow shadow-indigo-500" />
                                    )}
                                  </div>
                                  <div className="h-6" />
                                </div>
                              </div>
                              <p className="text-[11px] text-zinc-500 text-center max-w-sm mx-auto leading-relaxed">
                                Sodium has 1 electron in its outer shell; Chlorine has 7. Transfer Sodium's valence electron to Chlorine to satisfy the octet rule for both.
                              </p>
                            </div>
                          )}
                        </div>

                        {/* Interactive Action Controls */}
                        <div className="flex gap-4">
                          <button
                            onClick={handleOctetCheck}
                            disabled={bondingCompleted}
                            className="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white font-bold rounded-xl transition text-xs uppercase tracking-wider"
                          >
                            Check Octet Rule
                          </button>
                          <button
                            onClick={handleValenceReset}
                            disabled={bondingCompleted}
                            className="px-6 py-3 bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white rounded-xl transition text-xs uppercase tracking-wider"
                          >
                            Reset Valence
                          </button>
                        </div>
                      </div>

                      {/* Level 3 logs and completion action */}
                      <div className="bg-zinc-950/40 border border-zinc-800/60 p-6 rounded-2xl text-center">
                        {bondingCompleted ? (
                          <div className="space-y-4 py-2 flex flex-col items-center justify-center">
                            <p className="text-sm text-emerald-400 font-semibold animate-pulse">
                              ✓ Chemical bonding completed successfully!
                            </p>
                            <button
                              onClick={handleSubmitBondingSimulation}
                              className="px-8 py-3.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-bold rounded-xl shadow-lg shadow-emerald-500/20 transform hover:scale-105 transition-all duration-300 active:scale-95 text-xs uppercase tracking-wider"
                            >
                              Submit Level 3 Simulation Results
                            </button>
                          </div>
                        ) : (
                          <div className="text-zinc-500 text-xs py-2">
                            Select shared/transferred electrons above, and verify octet configuration.
                          </div>
                        )}
                      </div>
                    </>
                  )}
                </>
              )}
            </div>
          </div>

          {/* Feedback & Telemetry Visualizer Sidebar */}
          <div className="space-y-6">
            {/* Classroom Connection Card */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 shadow-xl space-y-3">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider text-zinc-400">
                🏫 Classroom Connection
              </h3>
              
              {classroomInfo || (currentUser && currentUser.classroom_name) ? (
                <div className="p-3 bg-zinc-950/60 border border-zinc-850 rounded-lg text-xs space-y-1">
                  <p className="text-zinc-550 font-bold uppercase text-[9px]">Linked Classroom</p>
                  <p className="text-white font-bold">{classroomInfo ? classroomInfo.classroom_name : currentUser.classroom_name}</p>
                  <p className="text-indigo-400 font-mono font-bold text-[10px]">Code: {classroomInfo ? classroomInfo.class_code : currentUser.class_code}</p>
                </div>
              ) : (
                <form onSubmit={handleJoinClassroom} className="space-y-3">
                  <p className="text-[11px] text-zinc-500 leading-relaxed">Join your teacher's classroom to share your standard mastery reports.</p>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Enter Class Code"
                      value={classCodeJoin}
                      onChange={(e) => setClassCodeJoin(e.target.value)}
                      className="flex-1 bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                    />
                    <button type="submit" className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-bold transition">
                      Join
                    </button>
                  </div>
                  {joinMessage && <p className="text-[10px] text-emerald-400 font-bold">{joinMessage}</p>}
                  {joinError && <p className="text-[10px] text-rose-400 font-bold">{joinError}</p>}
                </form>
              )}
            </div>

            {/* Live Feedback Logs */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 shadow-xl h-72 flex flex-col">
              <h3 className="text-sm font-bold text-white mb-3 uppercase tracking-wider text-zinc-400">
                Action Feedback Log
              </h3>
              <div className="flex-1 overflow-y-auto space-y-2.5 pr-2 scrollbar-thin scrollbar-thumb-zinc-800">
                {activeLevel === 1 ? (
                  feedbackLog.length === 0 ? (
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
                  )
                ) : activeLevel === 2 ? (
                  translationFeedbackLog.length === 0 ? (
                    <p className="text-zinc-500 text-xs italic text-center mt-16">
                      No translation steps taken yet. Pair tRNA to begin translation.
                    </p>
                  ) : (
                    translationFeedbackLog.map((log, idx) => (
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
                  )
                ) : (
                  bondingFeedbackLog.length === 0 ? (
                    <p className="text-zinc-500 text-xs italic text-center mt-16">
                      No bonding attempts made yet. Share/transfer electrons to begin.
                    </p>
                  ) : (
                    bondingFeedbackLog.map((log, idx) => (
                      <div
                        key={idx}
                        className={`p-2.5 rounded-lg border text-xs flex gap-2.5 items-start ${
                          log.status === "SUCCESS"
                            ? "bg-emerald-500/5 border-emerald-500/20 text-emerald-300"
                            : log.status === "RESET"
                            ? "bg-zinc-800 border-zinc-700 text-zinc-400"
                            : "bg-rose-500/5 border-rose-500/20 text-rose-300"
                        }`}
                      >
                        <span className="font-mono text-[10px] text-zinc-500 pt-0.5">
                          {log.timestamp}
                        </span>
                        <div>{log.message}</div>
                      </div>
                    ))
                  )
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

              <button
                onClick={() => {
                  setShowSyncModal(true);
                  setSyncLogs([]);
                }}
                className="px-3 py-1.5 text-xs font-semibold bg-indigo-650 hover:bg-indigo-600 text-white rounded-lg border border-indigo-500/30 transition flex items-center gap-2"
              >
                <span>🔄</span> Sync Classroom Roster
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
                    <th className="py-3">BKT LS1.1 (Life Sci)</th>
                    <th className="py-3">BKT PS1.1 (Phys Sci)</th>
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
                          <td className="py-3.5 font-bold font-mono text-indigo-400">
                            {student.bkt_mastery ?? "17.5"}%
                          </td>
                          <td className="py-3.5 font-bold font-mono text-indigo-400">
                            {student.bkt_bonding_mastery ?? "15.0"}%
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

            {/* B2B Seat Purchasing, Invite generation, and Manual Quota overrides */}
            <div className="lg:col-span-2 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* B2B Seat Purchasing */}
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>💳</span> B2B Campus Seat Purchasing
                  </h3>
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    Purchase additional student seat blocks for any campus in the district ($6.00 / seat / year).
                  </p>
                  {adminKpisData && adminKpisData.campuses && (
                    <form onSubmit={(e) => {
                      e.preventDefault();
                      const targetCampus = e.target.elements.campus.value;
                      const count = parseInt(e.target.elements.seats.value, 10);
                      if (targetCampus && count > 0) {
                        handleBuySeats(targetCampus, count);
                      }
                    }} className="space-y-3">
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Select Campus</label>
                          <select name="campus" required className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none bg-zinc-900">
                            <option value="">-- Select --</option>
                            {adminKpisData.campuses.map(c => (
                              <option key={c.id} value={c.id}>{c.name}</option>
                            ))}
                          </select>
                        </div>
                        <div>
                          <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Seats Count</label>
                          <input type="number" name="seats" defaultValue="50" min="10" required className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none" />
                        </div>
                      </div>
                      <button type="submit" className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs uppercase tracking-wider transition-all">
                        Purchase Seat Block
                      </button>
                    </form>
                  )}
                </div>

                {/* Teacher Invite Panel */}
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-4 font-sans">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>✉️</span> Generate Teacher Invites
                  </h3>
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    Issue secure invite codes linking teachers directly to their designated campuses.
                  </p>
                  
                  <form onSubmit={handleCreateInvite} className="space-y-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Teacher Email</label>
                        <input 
                          type="email" 
                          value={inviteEmailInput} 
                          onChange={(e) => setInviteEmailInput(e.target.value)} 
                          placeholder="teacher@school.edu" 
                          required 
                          className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors" 
                        />
                      </div>
                      <div>
                        <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Designated Campus</label>
                        {adminKpisData && adminKpisData.campuses ? (
                          <select 
                            value={inviteCampusIdInput} 
                            onChange={(e) => setInviteCampusIdInput(e.target.value)} 
                            required 
                            className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none bg-zinc-900"
                          >
                            <option value="">-- Select --</option>
                            {adminKpisData.campuses.map(c => (
                              <option key={c.id} value={c.id}>{c.name}</option>
                            ))}
                          </select>
                        ) : (
                          <select required className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none bg-zinc-900">
                            <option value="">No Campuses</option>
                          </select>
                        )}
                      </div>
                    </div>
                    <button type="submit" className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs uppercase tracking-wider transition-all">
                      Generate Invite Code
                    </button>
                  </form>

                  {inviteSuccessMessage && (
                    <div className="p-3 bg-zinc-950 border border-zinc-850 rounded-lg space-y-2">
                      <p className="text-[11px] text-emerald-400 font-bold">{inviteSuccessMessage}</p>
                      {generatedInviteCode && (
                        <div className="flex gap-2 items-center">
                          <input 
                            type="text" 
                            readOnly 
                            value={`http://localhost:3000/?invite_code=${generatedInviteCode}`} 
                            className="flex-1 bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-[10px] font-mono text-zinc-300 focus:outline-none cursor-pointer"
                            onClick={(e) => e.target.select()}
                          />
                          <span className="text-[9px] uppercase font-bold text-zinc-500">Copied url</span>
                        </div>
                      )}
                    </div>
                  )}
                  {inviteErrorMessage && (
                    <p className="text-[11px] text-rose-400 font-semibold">{inviteErrorMessage}</p>
                  )}
                </div>
              </div>

              {/* Manual Quota Override */}
              <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-4">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <span>⚙️</span> District Quota Overrides
                </h3>
                <p className="text-xs text-zinc-500 leading-relaxed">
                  District Admin overrides to manually adjust campus seat allocations (without B2B Stripe transactions).
                </p>
                
                <form onSubmit={handleAdjustQuota} className="flex flex-col sm:flex-row gap-3 items-end">
                  <div className="flex-1">
                    <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Select Campus</label>
                    {adminKpisData && adminKpisData.campuses ? (
                      <select 
                        value={adjustCampusIdInput} 
                        onChange={(e) => setAdjustCampusIdInput(e.target.value)} 
                        required 
                        className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none bg-zinc-900"
                      >
                        <option value="">-- Select --</option>
                        {adminKpisData.campuses.map(c => (
                          <option key={c.id} value={c.id}>{c.name}</option>
                        ))}
                      </select>
                    ) : (
                      <select required className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none bg-zinc-900">
                        <option value="">No Campuses</option>
                      </select>
                    )}
                  </div>
                  <div className="w-32">
                    <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">New Limit</label>
                    <input 
                      type="number" 
                      value={adjustSeatLimitInput} 
                      onChange={(e) => setAdjustSeatLimitInput(e.target.value)} 
                      placeholder="e.g. 500" 
                      required 
                      className="w-full bg-zinc-950 border border-zinc-850 rounded-lg px-3 py-2 text-xs text-white focus:outline-none" 
                    />
                  </div>
                  <button type="submit" className="py-2 px-6 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 font-bold rounded-lg text-xs uppercase tracking-wider transition-colors h-9">
                    Update Limit
                  </button>
                </form>
                {adjustQuotaSuccessMessage && (
                  <p className="text-[11px] text-emerald-400 font-bold">{adjustQuotaSuccessMessage}</p>
                )}
                {adjustQuotaErrorMessage && (
                  <p className="text-[11px] text-rose-400 font-semibold">{adjustQuotaErrorMessage}</p>
                )}
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
                    <div className="flex-1">
                      <div className="flex justify-between items-start">
                        <div>
                          <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-wider">Student Profile</span>
                          <h3 className="text-xl font-bold text-white mt-0.5 flex items-center gap-2">
                            {parentReportData.child_name}
                            {parentReportData.is_premium ? (
                              <span className="text-[9px] bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-2 py-0.5 rounded font-black uppercase tracking-wider shadow-md shadow-emerald-500/10 animate-pulse">PRO</span>
                            ) : (
                              <button 
                                onClick={handleGoPremium}
                                className="text-[9px] bg-zinc-800 hover:bg-zinc-700 text-zinc-300 px-2 py-0.5 rounded font-bold uppercase tracking-wider border border-zinc-700 transition"
                              >
                                Upgrade
                              </button>
                            )}
                          </h3>
                        </div>
                        
                        {parentReportData.linked_children && parentReportData.linked_children.length > 1 && (
                          <div className="flex items-center gap-2 bg-zinc-950 px-2 py-1 rounded-lg border border-zinc-800">
                            <span className="text-[9px] uppercase font-bold text-zinc-500">Child:</span>
                            <select
                              value={parentReportData.child_id}
                              onChange={(e) => fetchParentReport(e.target.value)}
                              className="bg-transparent text-xs font-bold text-white focus:outline-none border-none cursor-pointer"
                            >
                              {parentReportData.linked_children.map(c => (
                                <option key={c.id} value={c.id} className="bg-zinc-900 text-white">
                                  {c.name}
                                </option>
                              ))}
                            </select>
                          </div>
                        )}
                      </div>
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

                  {/* BKT Mastery Modeling Section */}
                  <div className="mt-5 p-5 bg-gradient-to-r from-zinc-950 to-indigo-950/20 border border-zinc-850 rounded-xl space-y-3.5">
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="text-[10px] uppercase font-black text-indigo-400 tracking-wider">Bayesian Knowledge Tracing (BKT)</span>
                        <h4 className="text-sm font-bold text-white mt-0.5">Dynamic Mastery Estimate: B.LS1.1</h4>
                      </div>
                      <div className="text-right">
                        <span className="text-xl font-mono font-black text-indigo-300">
                          {parentReportData.bkt_mastery ?? "17.5"}%
                        </span>
                      </div>
                    </div>

                    <div className="w-full bg-zinc-900 rounded-full h-2.5 overflow-hidden border border-zinc-800">
                      <div
                        className={`h-full rounded-full transition-all duration-1000 ${
                          (parentReportData.bkt_mastery ?? 17.5) >= 85
                            ? "bg-emerald-500"
                            : (parentReportData.bkt_mastery ?? 17.5) >= 70
                            ? "bg-indigo-500"
                            : (parentReportData.bkt_mastery ?? 17.5) >= 50
                            ? "bg-amber-500"
                            : "bg-rose-500"
                        }`}
                        style={{ width: `${parentReportData.bkt_mastery ?? 17.5}%` }}
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-1 text-[11px] text-zinc-400 font-mono">
                      <div className="flex justify-between p-2 bg-zinc-950/40 rounded-lg border border-zinc-850">
                        <span>Transcription (Base pairing):</span>
                        <span className="text-white font-bold">{parentReportData.bkt_transcription ?? "20.0"}%</span>
                      </div>
                      <div className="flex justify-between p-2 bg-zinc-950/40 rounded-lg border border-zinc-850">
                        <span>Translation (Codon match):</span>
                        <span className="text-white font-bold">{parentReportData.bkt_translation ?? "15.0"}%</span>
                      </div>
                    </div>
                  </div>

                  {/* BKT Mastery Modeling Section (Physical Sciences - B.PS1.1) */}
                  <div className="mt-4 p-5 bg-gradient-to-r from-zinc-950 to-indigo-950/20 border border-zinc-850 rounded-xl space-y-3.5">
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="text-[10px] uppercase font-black text-indigo-400 tracking-wider">Bayesian Knowledge Tracing (BKT)</span>
                        <h4 className="text-sm font-bold text-white mt-0.5">Dynamic Mastery Estimate: B.PS1.1</h4>
                      </div>
                      <div className="text-right">
                        <span className="text-xl font-mono font-black text-indigo-300">
                          {parentReportData.bkt_bonding_mastery ?? "15.0"}%
                        </span>
                      </div>
                    </div>

                    <div className="w-full bg-zinc-900 rounded-full h-2.5 overflow-hidden border border-zinc-800">
                      <div
                        className={`h-full rounded-full transition-all duration-1000 ${
                          (parentReportData.bkt_bonding_mastery ?? 15.0) >= 85
                            ? "bg-emerald-500"
                            : (parentReportData.bkt_bonding_mastery ?? 15.0) >= 70
                            ? "bg-indigo-500"
                            : (parentReportData.bkt_bonding_mastery ?? 15.0) >= 50
                            ? "bg-amber-500"
                            : "bg-rose-500"
                        }`}
                        style={{ width: `${parentReportData.bkt_bonding_mastery ?? 15.0}%` }}
                      />
                    </div>

                    <div className="pt-1 text-[11px] text-zinc-400 font-mono">
                      <div className="flex justify-between p-2 bg-zinc-950/40 rounded-lg border border-zinc-850">
                        <span>Valence Shell Electron Sharing & Ionic Transfers:</span>
                        <span className="text-white font-bold">{parentReportData.bkt_bonding_mastery ?? "15.0"}%</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4">
                    <BktGrowthChart history={parentReportData.bkt_history} />
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

              {/* Right Column: Household Management & Home Labs */}
              <div className="space-y-6">
                {/* Household Management Card */}
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-4">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-1">👨‍👩‍👧‍👦 Household Children</h3>
                    <p className="text-xs text-zinc-500 leading-relaxed">
                      Manage linked children and slots. Base premium ($60/yr) includes 1 child slot. Add more for $30/yr.
                    </p>
                  </div>
                  
                  <div className="bg-zinc-950 p-3.5 rounded-xl border border-zinc-850 text-xs space-y-2">
                    <div className="flex justify-between text-zinc-400">
                      <span>Premium child slots:</span>
                      <span className="text-white font-bold font-mono">{parentReportData.premium_slots}</span>
                    </div>
                    <div className="flex justify-between text-zinc-400">
                      <span>Linked kids count:</span>
                      <span className="text-white font-bold font-mono">{parentReportData.linked_children ? parentReportData.linked_children.length : 1}</span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => setShowAddChildForm(!showAddChildForm)}
                      className="flex-1 py-2 bg-zinc-800 hover:bg-zinc-750 text-zinc-200 border border-zinc-700 font-bold rounded-lg text-xs uppercase tracking-wider transition-all text-center"
                    >
                      Add Child
                    </button>
                    <button
                      onClick={handleBuyAdditionalSlot}
                      className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs uppercase tracking-wider transition-all text-center"
                    >
                      Buy Slot ($30)
                    </button>
                  </div>

                  {showAddChildForm && (
                    <form onSubmit={handleAddChild} className="p-3 bg-zinc-950 border border-zinc-850 rounded-xl space-y-3">
                      <div>
                        <label className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">Child's Name</label>
                        <input
                          type="text"
                          value={newChildName}
                          onChange={(e) => setNewChildName(e.target.value)}
                          placeholder="e.g. Liam Smith"
                          required
                          className="w-full bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                        />
                      </div>
                      <button type="submit" className="w-full py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-xs font-bold transition">
                        Link Child
                      </button>
                    </form>
                  )}
                  {addChildMessage && <p className="text-[11px] text-emerald-400 font-bold">{addChildMessage}</p>}
                  {addChildError && <p className="text-[11px] text-rose-450 font-bold">{addChildError}</p>}
                </div>

                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl relative overflow-hidden flex flex-col h-full justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-1">🏡 At-Home Science Connection</h3>
                    <p className="text-xs text-zinc-500 mb-4">
                      Simple hands-on labs you can run together to reinforce the active OAS standard in the kitchen!
                    </p>

                    <div className="space-y-4">
                      {parentReportData.home_activity_cards.map((card, idx) => {
                        const isLocked = !parentReportData.is_premium && idx > 0;
                        return (
                          <div key={idx} className={`bg-zinc-950 border border-zinc-850 p-4 rounded-xl hover:border-zinc-700 transition relative overflow-hidden ${isLocked ? 'brightness-50 select-none' : ''}`}>
                            <span className="text-[9px] uppercase font-bold text-indigo-400 tracking-wider block">
                              {card.difficulty}
                            </span>
                            <h4 className="text-sm font-bold text-white mt-1">
                              {card.title}
                            </h4>
                            <p className="text-xs text-zinc-400 mt-1.5 leading-relaxed">
                              {card.description}
                            </p>
                            {isLocked && (
                              <div className="absolute inset-0 bg-zinc-950/90 flex flex-col items-center justify-center p-3 text-center border border-zinc-850 rounded-xl">
                                <span className="text-sm">🔒</span>
                                <h5 className="text-xs font-bold text-white mt-1">Premium Activity Locked</h5>
                                <button
                                  onClick={handleGoPremium}
                                  className="mt-2 px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-[10px] font-bold uppercase transition"
                                >
                                  Unlock All Labs
                                </button>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      )}

      {role === "school_admin" && (
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-white">School Administrator Quota Portal</h2>
              <p className="text-sm text-zinc-400">Manage metered seat allocations, campus accounts status, and download billing invoices.</p>
            </div>
            <button
              onClick={fetchSchoolAdminData}
              disabled={isLoadingSchoolAdminData}
              className="px-3 py-1.5 text-xs font-semibold bg-zinc-850 hover:bg-zinc-750 text-zinc-200 rounded-lg border border-zinc-700 transition"
            >
              {isLoadingSchoolAdminData ? "Refreshing..." : "Refresh Portal"}
            </button>
          </div>

          {schoolAdminData ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column: Campus Status & Active Quotas */}
              <div className="lg:col-span-2 space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
                    <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Campus Name</span>
                    <div className="text-xl font-black text-white mt-1">{schoolAdminData.campus_name}</div>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
                    <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Seat Limit</span>
                    <div className="text-2xl font-mono font-bold text-indigo-400 mt-1">{schoolAdminData.seat_limit}</div>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-2xl">
                    <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Active Seats Used</span>
                    <div className="text-2xl font-mono font-bold text-white mt-1">
                      {schoolAdminData.active_students} / {schoolAdminData.seat_limit}
                    </div>
                  </div>
                </div>

                {/* Quota Gauge Card */}
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <span className="text-[10px] uppercase font-black text-indigo-400 tracking-wider">Metered seat utilization</span>
                      <h4 className="text-sm font-bold text-white mt-0.5">Active Campus Allocation Percentage</h4>
                    </div>
                    <div className="text-right">
                      <span className="text-xl font-mono font-black text-white">
                        {schoolAdminData.seat_limit > 0
                          ? Math.round((schoolAdminData.active_students / schoolAdminData.seat_limit) * 100)
                          : 0}%
                      </span>
                    </div>
                  </div>

                  <div className="w-full bg-zinc-950 rounded-full h-3 overflow-hidden border border-zinc-850">
                    <div
                      className={`h-full rounded-full transition-all duration-1000 ${
                        (schoolAdminData.active_students / schoolAdminData.seat_limit) >= 0.9
                          ? "bg-rose-500"
                          : (schoolAdminData.active_students / schoolAdminData.seat_limit) >= 0.7
                          ? "bg-amber-500"
                          : "bg-indigo-500"
                      }`}
                      style={{
                        width: `${
                          schoolAdminData.seat_limit > 0
                            ? Math.min(100, (schoolAdminData.active_students / schoolAdminData.seat_limit) * 100)
                            : 0
                        }%`
                      }}
                    />
                  </div>

                  <div className="pt-2 flex justify-between items-center">
                    <div className="text-xs text-zinc-500">
                      Status:{" "}
                      <span
                        className={`font-bold px-2 py-0.5 rounded text-[10px] uppercase ${
                          schoolAdminData.subscription_status === "active"
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                            : "bg-rose-500/10 text-rose-450 border border-rose-500/20"
                        }`}
                      >
                        {schoolAdminData.subscription_status}
                      </span>
                    </div>
                    <button
                      onClick={() => handleBuySeats(schoolAdminData.campus_id, 50)}
                      className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs transition shadow-md shadow-indigo-600/10"
                    >
                      Buy +50 Seats ($300)
                    </button>
                  </div>
                </div>

                {/* Past Billing Statements & Invoicing Receipts */}
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-4">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-zinc-400">Past Payment Invoices</h3>
                  {schoolAdminData.invoices.length === 0 ? (
                    <p className="text-zinc-500 text-xs italic py-6 text-center">No past payment statements found for this campus.</p>
                  ) : (
                    <div className="divide-y divide-zinc-850">
                      {schoolAdminData.invoices.map((inv) => (
                        <div key={inv.id} className="py-3 flex justify-between items-center text-xs">
                          <div>
                            <p className="text-white font-bold">{inv.stripe_invoice_id}</p>
                            <p className="text-[10px] text-zinc-500 font-mono mt-0.5">
                              {new Date(inv.created_at).toLocaleDateString()} • {inv.seats_purchased} seats
                            </p>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="font-mono font-bold text-white">${inv.amount_paid.toFixed(2)}</span>
                            <a
                              href={inv.invoice_pdf_url}
                              target="_blank"
                              rel="noreferrer"
                              className="px-2.5 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded border border-zinc-700 transition text-[10px] font-bold"
                            >
                              Download PDF
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Right Column: Campus Invite Codes */}
              <div className="space-y-6">
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-4">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-1">🏫 Teacher Registration Links</h3>
                    <p className="text-xs text-zinc-500 leading-relaxed">
                      Generated invitation codes linked to this campus. Teachers joining with these links will register under your seat license limit automatically.
                    </p>
                  </div>

                  {schoolAdminData.invites.length === 0 ? (
                    <p className="text-zinc-500 text-xs italic py-4 text-center">No invite codes generated yet.</p>
                  ) : (
                    <div className="space-y-2">
                      {schoolAdminData.invites.map((inv, idx) => (
                        <div key={idx} className="p-3 bg-zinc-950 border border-zinc-850 rounded-xl flex justify-between items-center text-xs">
                          <div>
                            <span className="font-mono font-bold text-indigo-400 select-all">{inv.code}</span>
                            <span className="text-[9px] text-zinc-550 block font-mono mt-0.5">
                              {new Date(inv.created_at).toLocaleDateString()}
                            </span>
                          </div>
                          <div>
                            {inv.is_used ? (
                              <span className="text-[9px] px-2 py-0.5 bg-zinc-800 text-zinc-500 rounded font-bold uppercase">Used</span>
                            ) : (
                              <span className="text-[9px] px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded font-bold uppercase">Available</span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center text-zinc-500 italic">
              Loading school admin dashboard data...
            </div>
          )}
        </main>
      )}
      </>
      )}
    </div>
  );
}
