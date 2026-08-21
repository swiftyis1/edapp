# Sprint 10: Google Classroom Grade Pushing & Auditing (Weeks 19 & 20)

**Theme:** Grade synchronization pipeline, infinite loop safety controls, and production launch validation.

---

## 📋 Iteration Checklist

### Week 19: Google Classroom Grade Pushing Integration
*   [x] **1. Grade Synchronization Service**
    *   Build a service that calls the Google Classroom API `courses.courseWork.studentSubmissions.patch` endpoint to write in-app auto-graded and manually reviewed scores back to student submission objects as `draftGrade`.
*   [x] **2. Throttled Sync Batching Queue**
    *   Implement Celery-based sync pipeline to throttle API requests. Gracefully catch and retry on `429 Too Many Requests` Google API errors.

### Week 20: Security, Resource Sandboxing, & Final Pilot Testing
*   [x] **3. WebAssembly Memory & Loop Audits**
    *   Conduct automated testing on the Pyodide Web Worker sandbox. Verify that memory leaks or execution timeouts (5-second threshold) safely terminate the worker without crashing client browsers.
*   [x] **4. End-to-End Grade Sync Validation**
    *   Run manual testing protocols using mock student Google accounts. Import coursework, submit answers, and verify that grades sync successfully into the Google Classroom Gradebook interface under draft status.
