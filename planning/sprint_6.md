# Sprint 6: Roster SSO Sync & Multi-Standard Dashboards (Weeks 11 & 12)

**Theme:** Implement Clever and Google Classroom roster syncing endpoints, and upgrade all dashboards to display multi-standard BKT mastery reports.

---

## Sprint Goals & Scope

*   **Objective:** Automate roster management for teachers via SSO classroom syncing, and render multi-standard BKT learning progress across Life Sciences and Physical Sciences.
*   **Approach:** Connect Google Classroom and Clever API endpoints to auto-create students and sync rosters, and render live probability progress bars on the frontend.

---

## 📋 Iteration Checklist

### Week 11: Clever & Google Classroom Roster Sync

*   [ ] **1. OAuth2 SSO Roster Endpoints**
    *   Implement `/api/sync/google-classroom/` and `/api/sync/clever/` to sync classrooms, periods, and student registrations.
*   [ ] **2. Auto-Registration Mapping**
    *   Create student profile mappings to bind Clever/Google identifiers to local database records automatically during sync events.
*   [ ] **3. Sync Roster Actions**
    *   Build a "Sync Classroom Roster" button in the Teacher Dashboard and display execution progress logs.

---

### Week 12: Multi-Standard Dashboards

*   [ ] **4. Dashboards Mastery Upgrade**
    *   Upgrade Student, Parent, and Teacher dashboard views to support multiple active OAS standards: `B.LS1.1` (DNA) and `B.PS1.1` (Bonding).
*   [ ] **5. Dynamic BKT Progress Bars**
    *   Display live BKT mastery probabilities ($P(L_t)$) as animated, color-coded progress bars instead of raw percentages.
*   [ ] **6. Student Growth Charts**
    *   Add a temporal growth chart showing how the student's mastery probability evolved over sessions.
