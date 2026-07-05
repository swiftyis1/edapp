# Sprint 9: LTI Integration & LMS Syncing (Weeks 17 & 18)

**Theme:** Implement LTI (Learning Tools Interoperability) 1.3 standards to sync assessment scores directly to Canvas, Schoology, and Google Classroom gradebooks.

---

## Sprint Goals & Scope

*   **Objective:** Enable schools to launch Swift Science directly from their LMS (Learning Management System) and automatically push student standard mastery scores to LMS gradebooks.
*   **Approach:** Configure LTI 1.3 Advantage authentication, configure tool registration keys, and build LTI grade passback services.

---

## 📋 Iteration Checklist

### Week 17: LTI 1.3 Advantage Tool Registration

*   [ ] **1. LTI 1.3 OIDC Auth Flow**
    *   Implement LTI 1.3 OpenID Connect launch flow to authenticate students and teachers launching the app from Canvas/Schoology.
*   [ ] **2. LMS Platform Keysets**
    *   Create a Django keystore to manage public/private JWKS endpoints for secure message signature validation with LMS platforms.
*   [ ] **3. Deep Linking Launch**
    *   Implement LTI Deep Linking support, allowing teachers to select specific gameplay levels (e.g. DNA Transcription) as assignments.

---

### Week 18: Assignment and Grade Services (AGS)

*   [ ] **4. LTI Grade Passback View**
    *   Implement LTI Assignment and Grade Services (AGS) to post estimated OPI scores and mastery grades to the LMS gradebook upon game completion.
*   [ ] **5. Dynamic Grade Sync Config**
    *   Build a settings interface in the Teacher Dashboard to toggle automatic grade passback and configure score scaling parameters.
*   [ ] **6. Grade Sync Logs**
    *   Build a verification utility showing teachers sync status logs and retrying failed score transmissions.
