# Sprint 9: Google Classroom OAuth2 & Course Ingestion (Weeks 17 & 18)

**Theme:** Implement teacher OAuth2 credentials flow, import class rosters, and fetch active coursework templates.

---

## 📋 Iteration Checklist

### Week 17: OAuth2 Consent Flow & Credentials Storage
*   [x] **1. GCP Credentials & Redirect Views**
    *   Register credentials in Google Cloud Platform Console. Implement OAuth2 redirect, authorization code exchange, and secure callback views in Django.
*   [x] **2. Credential Encryption Middleware**
    *   Set up encryption service to encrypt teacher Access and Refresh tokens before storing them in the `UserProfile` database records.

### Week 18: Google Course & Roster Import
*   [x] **3. Ingest Course List & Student Rosters**
    *   Call Google Classroom API `courses.list` and `courses.students.list` endpoints to fetch active teacher classrooms.
*   [x] **4. Course Ingest & Mapping UI**
    *   Build the frontend import dashboard allowing teachers to list courses, sync student rosters, and automatically map student emails to our user database.
*   [x] **5. Ingest Coursework Tasks**
    *   Call Classroom API `courses.courseWork.list` to retrieve active classroom assignments and display them in a mapping table.
