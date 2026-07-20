# State Standards Activity Design Template

This document defines the baseline architectural and interactive template for implementing any state standard activity set in Swift Science.

---

## Baseline Structure

Every state standard activity set must strictly adhere to the following hierarchical blueprint:

1. **Standard & DOK Levels**:
   * Each standard (e.g., Biology `OAS.B.LS1.1`, Physical Science `OAS.B.PS1.1`) has **4 Depth of Knowledge (DOK) Levels**.
   * DOK levels are represented by tab selectors at the top of the interface.

2. **5 Activities per DOK**:
   * Each DOK level contains **5 distinct activity selector cards**.
   * Selecting an activity card loads the corresponding Task Definition.

3. **Checklist Quiz & Locking (The Baseline Template)**:
   * Every interactive activity must present the student with **3 random questions** drawn from a **bank of 10 questions** in the Task Definition area.
   * Below the questions is the **Activity Workspace** (e.g., simulation canvas, chemical bonding grid, codon matchup drill).
   * **The Lock**: The Activity Workspace starts in a locked state (`🔒 Locked`) and is disabled.
   * **The Unlock**: The student must answer all 3 questions correctly. Once all 3 questions are correct, the lock is lifted (`✓ UNLOCKED`), and the Activity Workspace becomes interactive.
   * **Shuffling**: Provide a "🎲 Swap Questions" or "Regenerate Questions" button to allow re-rolling the questions from the bank of 10.

---

## Telemetry Tracking

Every activity must track and dispatch two standardized telemetry events:
* `dok[X]_activity_check`: Dispatched on each question answer attempt (recording correctness, options, and attempt count).
* `dok[X]_activity_complete`: Dispatched once all 3 questions are answered correctly and the workspace is unlocked.
