# Sprint 12 Manual Testing Protocol

Use this protocol to verify the new DOK workspaces, randomized option shuffling, and BKT telemetry calculations for **B.LS1.4 (Cellular Division & Differentiation)** and **B.LS1.5 (Photosynthesis Energy Transformation)**.

**Verification Status:** 🏃 PENDING USER TESTING

---

## Part 1: B.LS1.4 (Cellular Division & Differentiation) UI Validation

### 1. DOK 1: Mitosis Phases Sorter
1. **Navigate to App:** Open `http://localhost:3000`.
2. **Select Standard:** Choose **OAS B.LS1.4: Cell Division & Differentiation** in the top dropdown.
3. **Select DOK:** Click **DOK 1**.
4. **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
   * *Note: Options are randomized. Read the choices to match the correct biological answers.*
5. **Verify Workspace Unlocked:** Once completed, scroll down to the **Mitosis Phases Sorter** workspace.
6. **Interact:** Click the **▲** and **▼** buttons next to each phase item to sort them chronologically:
   ```
   1. Prophase
   2. Metaphase
   3. Anaphase
   4. Telophase
   ```
7. **Verify Completion:** Click **Verify Sequence**. Ensure status displays **Complete**.

---

### 2. DOK 2: Cell Cycle Regulators Matcher
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 checkpoint-related checklist questions.
3. **Interact:** Scroll down to the **Cell Cycle Regulators Matcher** workspace. Select correct regulator complexes:
   * **G1/S Transition:** `Cyclin E - CDK2`
   * **G2/M Transition:** `Cyclin B - CDK1`
   * **Metaphase-to-Anaphase Transition:** `APC/C - Cdc20`
4. **Verify Completion:** Click **Verify Matches**. Ensure status displays **Complete**.

---

### 3. DOK 3: Stem Cell Lineage Mapper
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 stem cell and differentiation checklist questions.
3. **Interact:** Scroll down to the **Stem Cell Lineage Mapper** workspace. Match each embryonic germ layer:
   * **Ectoderm:** `Neuron`
   * **Mesoderm:** `Red Blood Cell`
   * **Endoderm:** `Pancreatic Beta Cell`
4. **Verify Completion:** Click **Verify Lineages**. Ensure status displays **Complete**.

---

### 4. DOK 4: Cancerous Control Loop
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 cancer genetics and cell cycle aberration checklist questions.
3. **Interact:** Scroll down to the **Cancerous Control Loop** workspace. Toggle proteins to their healthy, tumor-suppressive states:
   * **p53 (DNA Damage Sensor):** `Active`
   * **Rb (G1 Transition Gate):** `Hypophosphorylated (Active)`
   * **Ras (Growth Signal GTPase):** `Wildtype (GDP bound)`
4. **Verify Completion:** Click **Run Checkpoint System**. Ensure status displays **Complete** with a success confirmation.

---

## Part 2: B.LS1.5 (Photosynthesis Energy Transformation) UI Validation

### 1. DOK 1: Light-Dependent Reactions I/O
1. **Select Standard:** Choose **OAS B.LS1.5: Photosynthesis Energy** in the top dropdown.
2. **Select DOK:** Click **DOK 1**.
3. **Answer Quiz:** Answer the 3 chloroplast anatomy and light reactions checklist questions.
4. **Interact:** Scroll down to the **Light-Dependent Reactions I/O** workspace. Select the correct input/output molecules:
   * **Water Photolysis Input Reactant:** `H2O`
   * **Waste Byproduct Gas Released:** `O2`
   * **Reduced Electron/Proton Carrier Product:** `NADPH`
5. **Verify Completion:** Click **Verify Inputs/Outputs**. Ensure status displays **Complete**.

---

### 2. DOK 2: Z-Scheme Electron Flow Sorter
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 action spectra and electron transport checklist questions.
3. **Interact:** Scroll down to the **Z-Scheme Sorter** workspace. Arrange components in chronological order from electron release to Photosystem I excitation:
   ```
   1. H2O Splitting
   2. P680*
   3. Plastocyanin
   4. P700*
   ```
4. **Verify Completion:** Click **Verify Flow**. Ensure status displays **Complete**.

---

### 3. DOK 3: Pigment Absorption Spectra
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 Calvin Cycle stoichiometry and limiting factor checklist questions.
3. **Interact:** Scroll down to the **Pigment Absorption Spectra** workspace. Adjust light wavelength sliders to maximize absorption:
   * **Blue Wavelength:** Slide to exactly `450 nm`
   * **Red Wavelength:** Slide to exactly `680 nm`
4. **Verify Completion:** Click **Calculate Light Absorption**. Ensure status displays **Complete**.

---

### 4. DOK 4: Limiting Factors Optimizer
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 global warming, photoinhibition, and Rubisco genetic engineering questions.
3. **Interact:** Scroll down to the **Limiting Factors Optimizer** workspace. Adjust the environmental parameters:
   * **CO2 Concentration:** Slide to exactly `800 ppm`
   * **Temperature:** Slide to exactly `25 °C`
   * **Light Intensity:** Slide to exactly `500 W/m2`
4. **Verify Completion:** Click **Simulate Calvin Cycle Yield**. Ensure status displays **Complete** with optimal output achieved.

---

## Part 3: Parent report BKT Progress Verification
1. **Student Switcher:** Toggle between students in the main header.
2. **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
3. **Verify Masteries:** Ensure two new progress bars render correctly:
   * **Dynamic Mastery Estimate: B.LS1.4**
   * **Dynamic Mastery Estimate: B.LS1.5**
4. **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.
