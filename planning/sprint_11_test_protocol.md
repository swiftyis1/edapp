# Sprint 11 Manual Testing Protocol

Use this protocol to verify the new DOK workspaces, randomized option shuffling, and BKT telemetry calculations for **B.LS1.2 (Multicellular Hierarchical Systems)** and **B.LS1.3 (Homeostasis)**.

**Verification Status:** ✅ VERIFIED BY USER (2026-07-20)

---

## Part 1: B.LS1.2 (Multicellular Hierarchical Systems) UI Validation

### 1. DOK 1: Hierarchical Sorter
1. **Navigate to App:** Open `http://localhost:3000`.
2. **Select Standard:** Choose **OAS B.LS1.2: Multicellular Systems** in the top dropdown.
3. **Select DOK:** Click **DOK 1**.
4. **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
   * *Note: Options are randomized. Read the choices to match the correct biological answers.*
5. **Verify Workspace Unlocked:** Once completed, scroll down to the **Hierarchy Level Sorter** workspace.
6. **Interact:** Click the **▲** and **▼** buttons next to each hierarchy item to sort them from smallest to largest:
   ```
   1. Organelle
   2. Cell
   3. Tissue
   4. Organ
   5. Organ System
   6. Organism
   ```
7. **Verify Completion:** Once sorted correctly, verify the status bar displays **Complete** with a success message.

---

### 2. DOK 2: Tissue Matrix Alignment
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 tissue-related checklist questions.
3. **Interact:** Scroll down to the **Tissue Matrix Alignment** workspace. Match the dropdowns:
   * **Epithelial Tissue:** Stomach lining layer
   * **Connective Tissue:** Bone joints/blood
   * **Muscle Tissue:** Heart wall pump
   * **Nervous Tissue:** Brain cortex lining
4. **Verify Completion:** Ensure the status displays **Complete**.

---

### 3. DOK 3: Cardio/Respiratory Simulator
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 circulatory-system checklist questions.
3. **Interact:** Scroll down to the **Dual-System Oxygenation Balance** workspace.
4. **Adjust Sliders:**
   * Adjust **Breathing Rate** slider to between `25` and `35` breaths/min.
   * Adjust **Heart Rate** slider to between `120` and `140` bpm.
   * *Verify Oxygen Saturation jumps to 98% and Carbon Dioxide (pCO2) drops to 38 mmHg.*
5. **Lock in Setpoint:** Click **Verify System Stability**. Ensure status displays **Complete**.

---

### 4. DOK 4: Bio-mimetic Kidney Synthesizer
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 kidney-anatomy checklist questions.
3. **Interact:** Scroll down to the **Kidney Synthesizer** workspace. Configure the dropdowns:
   * **Filtration Membrane:** `Cellulose acetate (semi-permeable membrane)`
   * **Flow Pump Driver:** `Peristaltic micro-pump (replicates pulse blood pressure)`
   * **Biocompatible Coating:** `Differentiated endothelial cell lining (prevents clotting)`
4. **Verify Synthesis:** Click **Test Kidney Compatibility**. Ensure status displays **Complete**.

---

## Part 2: B.LS1.3 (Maintaining Homeostasis) UI Validation

### 1. DOK 1: Feedback Loop Classifier
1. **Select Standard:** Choose **OAS B.LS1.3: Homeostasis Regulation** in the top dropdown.
2. **Select DOK:** Click **DOK 1**.
3. **Answer Quiz:** Answer the 3 feedback checklist questions.
4. **Interact:** Scroll down to the **Feedback Loop Classifier** workspace. Classify the scenarios:
   * **Sweat glands activate...**: `Negative Feedback`
   * **Platelets release chemicals...**: `Positive Feedback`
   * **Insulin hormone lowers...**: `Negative Feedback`
   * **Uterine contractions intensify...**: `Positive Feedback`
5. **Verify Completion:** Ensure status displays **Complete**.

---

### 2. DOK 2: Thermoregulation Simulator
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 thermoregulation checklist questions.
3. **Interact:** Scroll down to the **Thermoregulation Simulator** workspace.
4. **Adjust Temp Stress:** Move the **Environmental Temp Stress** slider to a hot temperature (e.g., `40°C`).
5. **Compensate:** Adjust the **Vasodilation & Sweat Active Rate** slider to keep **Core Body Temperature** at exactly `37.0°C` (at `40°C` env temp, the active rate should be tuned to `80%`).
6. **Lock Setpoint:** Click **Lock Core Temperature**. Ensure status displays **Complete**.

---

### 3. DOK 3: Endocrine Glucose Control
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 glucose regulation checklist questions.
3. **Interact:** Scroll down to the **Endocrine Glucose Control** workspace.
4. **Stabilize Glucose:**
   * Starting glucose level is `150 mg/dL` (Hyperglycemia).
   * Click **Inject Insulin (-70)** to drop glucose to `80 mg/dL` (normal target range: `70-100`).
5. **Verify Homeostasis:** Click **Verify Homeostasis Setpoint**. Ensure status displays **Complete**.

---

### 4. DOK 4: PID Artificial Pancreas Tuning
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 PID controller checklist questions.
3. **Interact:** Scroll down to the **PID Artificial Pancreas Controller** workspace.
4. **Tune Controller:** Enter values into the text boxes:
   * **Kp (Proportional):** `2.5`
   * **Ki (Integral):** `0.5`
   * **Kd (Derivative):** `1.2`
5. **Verify Tuning:** Click **Simulate Closed Loop**. Ensure status displays **Complete**.

---

## Part 3: Dashboard Mastery Tracking

1. **Simulate Student Telemetry:**
   * Run the Django verification test script in your terminal to populate BKT telemetry:
     ```powershell
     cd backend
     .\venv\Scripts\python.exe manage.py verify_sprint11_bkt
     ```
2. **Open Dashboard:** In the top bar of the application, click **Parent Dashboard** or **Teacher Reports**.
3. **Verify Mastery Estimates:** Check that **B.LS1.2** and **B.LS1.3** masteries are rendered dynamically with progress bars and color-coded mastery bands matching the database estimates.
