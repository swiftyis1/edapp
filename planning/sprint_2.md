# Sprint 2: Analytics, Auth & Dashboards (Weeks 3 & 4)

**Theme:** Implement authentication, build parent and teacher reporting dashboards, and construct the scoring engine to estimate CCRA Performance Bands from telemetry logs.

---

## Sprint Goals & Scope

*   **Objective:** Secure the app with Role-Based Access Control (RBAC), create standard dashboards for teachers and parents, and implement the scoring logic to classify student ability into OPI scaled score bands.
*   **Approach:** Keep views responsive and lightweight, with scoring logic cleanly separated into configuration-backed Python services.

---

## 📋 Iteration Checklist

### Week 3: User Auth & Teacher Dashboard

*   [ ] **1. Role-Based Authentication (RBAC)**
    *   Set up Django authentication with support for three user profiles: `Student`, `Teacher`, and `Parent`.
    *   Configure JWT or session-based authentication in Next.js.
    *   Implement route guards in Next.js to restrict dashboard access based on roles.
*   [ ] **2. Roster Management API**
    *   Create Django endpoints to allow teachers to create a classroom, generate a Class Code, and view their student roster.
    *   Create student endpoints to join a classroom using a Class Code.
*   [ ] **3. Teacher Dashboard UI (Next.js)**
    *   Build a responsive, premium dashboard view for teachers.
    *   Display classroom aggregates: average transcription speed, overall accuracy, and total active sessions.
    *   Render the student roster table featuring:
        *   Student Name/ID
        *   Completed DNA Sequences
        *   Base Match Accuracy (%)
        *   Predicted CCRA Performance Band (Color-coded)
*   [ ] **4. Accountability Flagging**
    *   Highlight students predicted to score below the **300 Proficient cutoff** (Below Basic and Basic bands).
    *   Add visual warning tooltips and basic recommendation suggestions (e.g., "Student struggles with G-C pairing; recommend additional guided practice").

---

### Week 4: Parent Dashboard & Telemetry Scoring Engine

*   [ ] **5. Parent Dashboard UI (Next.js)**
    *   Build a simplified, highly encouraging portal for parents.
    *   Render progress charts showing daily/weekly gameplay time and standard mastery indicators.
    *   Implement "Home Activity Cards" containing simple, hands-on science experiments matching the child's active in-app learning path.
*   [ ] **6. In-Game Scoring Service Integration**
    *   Migrate the rule-based telemetry classifier from Sprint 1 into a robust, configurable `ScoringService` in Django.
    *   Pull scaling constants ($A$ and $B$) and category cutoffs from the database config table.
    *   Verify that student telemetry records dynamically update their OPI score estimates.
*   [ ] **7. De-identified CSV Import Pipeline**
    *   Build a secure Django admin endpoint `/api/admin/import-eoy/` to ingest de-identified EOY CSV data (featuring serial `user_id` and raw scores).
    *   Implement in-memory joining logic to align CSV scores with gameplay records while purging all raw identifiers.
*   [ ] **8. End-to-End Demo**
    *   Log in as a student, run a DNA simulation session with errors, and verify that the teacher dashboard updates their predicted CCRA score and flags them for intervention.
