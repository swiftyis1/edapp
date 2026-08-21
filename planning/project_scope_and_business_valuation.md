# Swift Science & Swift CS: Project Scope, Technical Briefing, & Business Valuation

This document serves as a comprehensive master overview of the **Swift** educational platform, covering both the **Swift Science** (OAS Biology & Physical Sciences) and **Swift CS** (Python Programming & AP CS A) product lines. It compiles system architecture, psychometric modeling, curriculum standards, technical implementations, and commercialization strategies into a single document. Upload this file to Gemini (or share with stakeholders) to provide a complete understanding of the project's technical scope and business value.

---

## 1. Executive Summary & Vision

**Swift** is an adaptive, standard-aligned educational platform built for secondary school assessment and learning across STEM disciplines. It solves two critical pain points in U.S. public education: **preparing students for high-stakes science and computer science assessments, and providing teachers with real-time, actionable diagnostics to prevent student failure.**

Rather than using passive study tools or static multiple-choice drills, the Swift platform combines:
1. **Interactive Simulation & Coding Workspaces** where students actively manipulate scientific models (e.g., transcribing DNA, balancing chemical equations) or write and compile code.
2. **Checklist Gating Quizzes** that require foundational concept mastery before unlocking advanced workspaces.
3. **A Predictive Psychometric Engine** using Bayesian Knowledge Tracing (BKT) and Item Response Theory (IRT) to forecast students' state test scores.
4. **Google Classroom & Roster Sync** allowing teachers to import classes and push gradebooks with a single click.
5. **Roles-Based Dashboards** for Students, Teachers, Parents, and District Administrators.

---

## 2. Technical Stack & Component Architecture

The platform is built on a modern, decoupled web architecture optimized for high-frequency telemetry ingestion, client-side compilation, and real-time dashboard updates.

```
       +-----------------------------------------------------+
       |               React / Next.js Frontend              |
       |  (Student Simulator, Wasm Editor & Teacher Panel)   |
       +--------------------------+--------------------------+
                                  |
                                  | REST API Telemetry, Roster & Grades
                                  v
       +-----------------------------------------------------+
       |                Django Backend Server                |
       |   (Auth, Google OAuth, Grading & Telemetry Sync)    |
       +--------------------+---------------------+----------+
                            |                     |
      Query Student state   |                     | Update Telemetry
                            v                     v
       +--------------------+-------+     +-------+----------+
       |   Student BKT & IRT State   |     |    PostgreSQL    |
       |        (JSONB Store)        |     |  (JSONB Events)  |
       +----------------------------+     +------------------+
```

### Core Technologies
* **Frontend**: Next.js 16+ (React), styled with Vanilla CSS and TailwindCSS for a premium, dark-mode glassmorphic aesthetic. Graphic simulation engines are implemented in React Canvas/interactive SVGs.
* **Client-Side WebAssembly (Wasm)**: Pre-loads the Pyodide Python 3.11 runtime from Cloudflare Edge CDNs directly into the client's browser, enabling instant execution and **$0 cloud egress/run costs**.
* **Backend**: Django & Django REST Framework (DRF) running on Python 3.11. The backend manages the student/class/district hierarchy, handles authentication, and exposes the REST endpoints.
* **Database**: PostgreSQL with custom JSONB schemas to log fine-grained process telemetry without locking database tables during peak classroom usage.
* **SSO & Rostering**: Built-in OAuth2 integrations with **Google Classroom** and **Clever SSO** to support automatic rostering and single-sign-on.
* **Billing & Monetization**: Full **Stripe** integration supporting B2C monthly/annual subscriptions and B2B school/district seat licensing checks with automated invoicing.

---

## 3. Pedagogical Core & Standards Alignment

### A. Swift Science (OAS Biology & Physical Sciences)
Swift Science is built around the **Oklahoma Academic Standards (OAS)** for Biology and Physical Sciences, mapping directly to the Oklahoma Grade 11 College- and Career-Readiness Assessment (CCRA) Science Test.
* **Depth of Knowledge (DOK) Levels & Gating**: For each covered standard, the curriculum is divided into **4 DOK Levels**, with **5 distinct activities per DOK level**.
* **The Gating Checklist**: Every activity has an associated pool of 10 competency questions. The student must answer 3 randomized questions correctly to unlock the simulation workspace.
* **Standard-Aligned Simulators**: DNA base-pairing, codon lookup wheels, tissue matrix matching, cardiopulmonary simulators, kidney synthesis workbenches, Punnett squares, pedigrees, natural selection cladograms, and global carbon cycling modelers.

### B. Swift CS (Computer Science & AP CS A Equivalent)
Swift CS provides a complete interactive python workspace aligned with high school programming requirements and AP CSA concepts.
* **Interactive Code Workspace**: An IDE featuring a live syntax-focused editor and a custom console terminal output.
* **10 Curriculum Sprints**:
  1. *Variables & Expressions* (AP CS A Unit 1)
  2. *Selection & Loops* (AP CS A Unit 2)
  3. *Functions & Scoping* (AP CS A Unit 1/2)
  4. *Custom Class Design* (AP CS A Unit 3)
  5. *Inheritance Hierarchies* (AP CS A Unit 3)
  6. *Lists & ArrayLists* (AP CS A Unit 4)
  7. *2D Coordinate Grids* (AP CS A Unit 4)
  8. *Search & Sort Algorithms* (AP CS A Unit 3/4)
  9. *Recursion & Advanced Sort* (AP CS A Unit 4)
  10. *Social & Ethical Impact* (AP CS A Unit 3)
* **Auto-Grade Assertion Runners**: Submissions undergo automated tests (e.g. validating function inputs/outputs) to grade tasks instantly.
* **Execution Safety Limits**: Client-side execution includes loop safety analysis (preventing infinite `while` loops) and iteration boundary clamps (max 1,000,000 operations) to prevent browser hangs.

---

## 4. Psychometrics & Latent Score Prediction

The platform's value relies on its ability to predict student performance on state tests. Instead of raw-score grading, Swift Science implements two psychometric models.

### A. Bayesian Knowledge Tracing (BKT)
For each concept, the platform estimates the probability that a student has mastered the skill ($P(L_t)$). It tracks four parameters in the database:
1. $P(L_0)$ - **Prior Mastery**: The probability the student knew the skill before using the platform.
2. $P(T)$ - **Transition (Learn Rate)**: The probability of acquiring the skill on an activity attempt.
3. $P(G)$ - **Guess**: The probability of answering correctly despite not having mastered the skill.
4. $P(S)$ - **Slip**: The probability of making an error despite having mastered the skill.

The backend updates the probability of mastery in real-time using standard BKT updates upon receiving telemetry check events.

### B. Item Response Theory (IRT) Pattern Scoring
The Oklahoma CCRA exam uses IRT pattern scoring. To match this, Swift Science treats simulation challenges as test items, measuring student latent ability ($\theta$):

$$P(X_{ij} = 1 \mid \theta_j) = \frac{1}{1 + e^{-\alpha_i(\theta_j - \beta_i)}}$$

Where $\theta_j$ is the student's latent science ability, $\beta_i$ is the level's psychometric difficulty, and $\alpha_i$ is the level's discrimination factor. The platform uses the **Graded Response Model (GRM)** to group student performance into ordinal categories (e.g., Category 0: relies on hints; Category 1: solves with errors; Category 2: solves efficiently with zero errors).

### C. Oklahoma Performance Index (OPI) Mapping
Estimated student ability ($\theta$) is scaled to the official OPI scale ($200 - 399$):

$$S_j = A \cdot \theta_j + B$$

To calibrate the constants $A$ and $B$, Swift Science uses **Equipercentile Equating** matching student normal distributions to historical state-wide assessment results, and **Anchor Items** grounded in released CCRA assessment questions.

---

## 5. Implementation Roadmap Status

Swift has completed a highly structured developmental roadmap. Over **26 distinct sprints**, the core stack, BKT engines, and standard simulations were fully built and verified:

* **Sprints 1–3**: Core database setup, telemetry schema initialization, and initial Stripe B2C/B2B licensing checkouts.
* **Sprints 4–7**: School administrator dashboards, metered license limits, and Clever/Google Classroom SSO callback integration.
* **Sprints 8–10**: Integration of Biology DNA modules, telemetry event triggers, and BKT update listeners.
* **Sprints 11–15**: Extended modules, including drone engineering, flight physics, and CareerTech ML models.
* **Sprints 16–20**: SQL database sandboxes, interactive data analytics pipelines, credentials registry, and initial CCRA score calibration.
* **Sprints 21–25**: Large-scale Biology and Physical Science standard integration (e.g. LS1.4 Mitosis, LS1.5 Photosynthesis, LS1.7 Respiration, LS2.1 Carrying Capacity, PS1.1 Bonding, PS2.5 Induction).
* **Sprint 26**: Integration of PS.PS4.4 (Electromagnetic Radiation Absorption) DOK levels 1–4, initial student CS sandbox design, and Google Classroom roster syncing.
* **Python Sprints (Active Sprints)**:
  * **Sprint 1 (Completed)**: Wasm Pyodide compiler WebAssembly integration, terminal output panel, custom variables and expression tests, and telemetry API logging.
  * **Sprint 2 (Active)**: Monaco Editor integration, client-side auto-grading runner, 5-second infinite execution worker watchdog timeout, and AP CS A Unit 2 control flow/loops courseware.

---

## 6. Business Model & Monetization Strategy

Swift operates a highly scalable, dual-channel SaaS model addressing both the B2B institutional market and the B2C consumer market.

### A. The Pain Point & Economic Value Proposition
* **The B2B Problem**: Public school districts are graded on state report cards (A–F scales) based on student proficiency rates. A drop in a school's rating leads to reduced enrollment, lower property values in the district, and potential state intervention.
* **The Solution**: Swift serves as an **Early-Warning System**. By flagging students projected to score below the **Proficient threshold (300 OPI)** in science, or those falling behind in computer science coursework, it allows districts to target remedial resources *months before* the exams.
* **The ROI**: The cost of student failure (remediation, summer school, administration, and lost funding) is estimated at **$1,500 - $3,000 per student**. Catching and correcting just **5 student failures** completely covers the cost of a typical district-wide license.

### B. Pricing Structure
1. **B2B School/District Licensing**:
   * Sold on a per-student-seat annual license.
   * **Single Subject (Science OR CS)**: $15 – $25 per seat/year (depending on district size).
   * **STEM Bundle (Science AND CS)**: $25 – $40 per seat/year, representing a highly appealing value proposition for school boards looking to cover both science and CTE coding requirements in a unified environment.
2. **B2C Family Subscription**:
   * Sold directly to parents/caregivers for homework assistance, coding tutoring, and performance monitoring.
   * **Price**: $9.99/month or $79/year per child.
   * **Viral Acquisition Loop**: Teachers using the platform in class invite parents to view their child's dashboard, creating a zero-CAC (Customer Acquisition Cost) pipeline for consumer subscriptions.

---

## 7. Financial Projections & Market Potential

### Total Addressable Market (TAM)
* **TAM (U.S. Secondary Science & CS Education)**: 24 million middle and high school students in the U.S. At $25/student/year average seat price, this represents a B2B addressable market of **$600 Million/year** (up from $360M prior to the addition of the Swift CS coding catalog).
* **SAM (Serviceable Addressable Market)**: States with frameworks aligned with NGSS, OAS, or standard AP Computer Science A course offerings. This represents **$240 Million/year**.
* **SOM (Serviceable Obtainable Market - Year 3 Goal)**: Capture 3% of the SAM through targeted district marketing in high-need regions. This represents **$7.2 Million/year** in high-margin SaaS revenue.

### Unit Economics & Egress Optimization
* **Gross Margin**: **>90%** (an improvement over the initial 85%). By compiling Pyodide client-side via WebAssembly in the user's browser, **there are $0 hosting egress bills** for heavy code execution tasks. Large static library assets are served via public CDNs, reducing server-side network usage.
* **LTV/CAC Ratio**: Projected at **6:1** for B2B. Adding computer science curriculum options increases average district contract sizes while reducing churn, as schools prefer keeping all STEM course diagnostics on a single platform.

---

## 8. Data Privacy & Compliance (FERPA & COPPA)

To pilot in schools, Swift enforces strict compliance with the **Family Educational Rights and Privacy Act (FERPA)** and **Children's Online Privacy Protection Act (COPPA)**.

### Zero-PII De-identification Pipeline
1. **Data Ingestion**: When school admins upload historical state scores to refine the predictive models, student names and local state IDs are joined in memory and immediately discarded.
2. **Database Anonymization**: The database records only a cryptographically secure, randomized hash (UUIDv4) linked to gameplay telemetry, Python coding grades, and scaled scores.
3. **FERPA Safety**: No personally identifiable information (PII) is exported or written to training databases, ensuring zero compliance risk for participating districts.
