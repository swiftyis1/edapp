# Sprint 4: Game Content Extension, BKT Modeling & Hardening (Weeks 7 & 8)

**Theme:** Implement DNA Translation puzzle, integrate Bayesian Knowledge Tracing (BKT) prediction modeling service, and run production builds, load testing, and database optimizations.

---

## Sprint Goals & Scope

*   **Objective:** Complete Level 2 in-game transcription-to-translation gameplay, construct a dynamic machine learning pipeline to estimate learning states, and finalize the codebase for production readiness.
*   **Approach:** Build a premium codon-matching drag-and-drop game interface, implement BKT modeling in Python, and perform query performance optimization.

---

## 📋 Iteration Checklist

### Week 7: In-Game DNA Translation & Telemetry

*   [x] **1. Translation Puzzle Level Design**
    *   Build a drag-and-drop codon-matching level where students match tRNA anticodons to mRNA codons to build an amino acid chain.
*   [x] **2. Level 2 Telemetry Dispatch**
    *   Emit specialized events: `codon_match_attempt`, `amino_acid_added`, and `translation_complete` with error counts and duration payloads.
*   [x] **3. DRF Telemetry Storage for Translation**
    *   Map new translation payload formats to PostgreSQL JSONB columns.

---

### Week 8: Bayesian Knowledge Tracing & Production Hardening

*   [x] **4. Python BKT Modeling Pipeline**
    *   Implement a Bayesian Knowledge Tracing (BKT) service to update transition, slip, guess, and knowledge probabilities based on base-pairing and translation telemetry.
*   [x] **5. Live score calculation**
    *   Run BKT updates asynchronously in Django when sessions finish to predict standard mastery.
*   [x] **6. Database & Cache Tuning**
    *   Add indexes to PostgreSQL JSONB columns on frequently filtered fields (`student_id`, `event_type`).
    *   Implement Redis/Django cache caching for roster analytics to keep load times under 200ms.
*   [x] **7. Production Bundle Hardening**
    *   Run Next.js build (`npm run build`) to resolve static generation and hydration errors.
    *   Configure clean environment variable files and remove debug endpoints.
