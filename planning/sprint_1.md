# Sprint 1: End-to-End Telemetry Loop (Weeks 1 & 2)

**Theme:** Establish the simplest possible playable sandbox, transmit telemetry events, and store them in the database for rendering on a basic dashboard. 

---

## Sprint Goals & Scope

*   **Objective:** Build a minimal DNA Transcription & Translation simulator (frontend), connect it to a database-backed API (backend), and display real-time student activity metrics on a simple teacher dashboard.
*   **Target Standard:** **B.LS1.1** (DNA structure determines proteins, which carry out life functions).
*   **Approach:** Focus on rapid, small, iterative steps.

---

## 📋 Iteration Checklist

### Week 1: Project Setup & Basic Telemetry Send

*   [x] **1. Project Initialization**
    *   Initialize the Next.js frontend project structure in `./frontend`.
    *   Initialize the Django backend project structure in `./backend`.
    *   Configure PostgreSQL development database connection.
*   [x] **2. Simple API Stub**
    *   Create a Django endpoint `/api/telemetry/` that accepts POST requests and returns a `200 OK` or `201 Created` status (no DB writes yet).
    *   Configure CORS to allow requests from the Next.js frontend.
*   [x] **3. Barebones DNA Simulator UI & Admin Dashboard (Next.js)**
    *   Create a simple interface displaying a short template DNA strand (e.g., `TAC GGC TTA`).
    *   Add interactive buttons for selecting mRNA nucleotide bases (A, U, G, C) to match the template.
    *   Implement transcription status feedback (e.g. displaying the transcribed mRNA chain).
    *   Implement District Administrator Dashboard stub displaying active campuses, seat license metrics, and a mock EOY de-identified CSV import log.

*   [x] **4. First Telemetry Dispatch**
    *   Write a client-side telemetry sender that catches click events (e.g., base matching attempt, checking sequence accuracy, clearing chain) and sends them via `fetch` to `/api/telemetry/`.
    *   *Verification:* Verify in browser network logs that events are firing and returning successful response codes.



---

### Week 2: Database Integration & First Dashboard View

*   [x] **5. Telemetry Schema & Storage**
    *   Create Django models for `Student`, `Session`, and `TelemetryEvent`.
    *   Migrate the database to apply the telemetry schema.
    *   Update the `/api/telemetry/` endpoint to parse the incoming JSON and save it to the database.
*   [x] **6. Simple Teacher Dashboard View**
    *   Create an endpoint `/api/reports/teacher/` that aggregates telemetry events (e.g., total transcription attempts, base error counts).
    *   Build a simple Next.js table view showing:
        *   Student Name
        *   Base Match Accuracy (%)
        *   Average Time per Base Pair
        *   Total Actions Logged
*   [x] **7. Rule-Based "State" Heuristic (CCRA Performance Band Proxy)**
    *   Implement a basic rule-based classifier in Python that maps student telemetry performance (e.g., error rate, time-to-solve) to a predicted CCRA Performance Band:
        *   High accuracy/fast speed $\rightarrow$ **Advanced (327-399)**
        *   Normal accuracy/moderate speed $\rightarrow$ **Proficient (300-326)**
        *   Minor errors/high retries $\rightarrow$ **Basic (278-299)**
        *   High error rate (>30%)/low engagement $\rightarrow$ **Below Basic (200-277)**
    *   Surface these predicted score ranges and color-coded status highlights on the teacher's dashboard (flagging anyone in the Basic/Below Basic range).
*   [x] **8. Walkthrough Demo**
    *   Play the DNA simulator, confirm transcription data is saved in PostgreSQL, and watch the teacher dashboard update in real time.

