# Sprint 13 Manual Testing Protocol

Use this protocol to verify the new DOK workspaces, randomized option shuffling, and BKT telemetry calculations for **B.LS1.6 (Macromolecule Synthesis)** and **B.LS1.7 (Cellular Respiration Energy Transfer)**.

**Verification Status:** 🏃 PENDING USER TESTING

---

## Part 1: B.LS1.6 (Macromolecule Synthesis) UI Validation

### 1. DOK 1: Monomer to Polymer Match
1. **Navigate to App:** Open `http://localhost:3000`.
2. **Select Standard:** Choose **OAS B.LS1.6: Macromolecule Synthesis** in the top dropdown.
3. **Select DOK:** Click **DOK 1**.
4. **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
   * *Note: Options are randomized. Read the choices to match the correct biological answers.*
5. **Verify Workspace Unlocked:** Once completed, scroll down to the **Monomer to Polymer Match** workspace.
6. **Interact:** Select the correct polymer class from each monomer dropdown:
   * **Amino Acid:** `Protein`
   * **Nucleotide:** `Nucleic Acid`
   * **Monosaccharide:** `Carbohydrate`
   * **Fatty Acid:** `Lipid`
7. **Verify Completion:** Click **Verify Monomers**. Ensure status displays **Complete**.

---

### 2. DOK 2: Fatty Acid Saturation Sorter
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 saturation-related checklist questions.
3. **Interact:** Scroll down to the **Fatty Acid Saturation Sorter** workspace. Match each fatty acid:
   * **Stearic Acid (No double bonds):** `Saturated (Straight)`
   * **Oleic Acid (1 double bond):** `Unsaturated (Bent)`
   * **Linoleic Acid (2 double bonds):** `Unsaturated (Bent)`
4. **Verify Completion:** Click **Verify Saturation**. Ensure status displays **Complete**.

---

### 3. DOK 3: Side-Chain Interaction Match
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 side-chain and folding checklist questions.
3. **Interact:** Scroll down to the **Side-Chain Interaction Match** workspace. Select correct bonds:
   * **Cysteine - Cysteine Linkage:** `Covalent (Disulfide Bridge)`
   * **Lysine (+) - Aspartate (-) Interaction:** `Ionic (Salt Bridge)`
   * **Leucine & Valine Clustering in Core:** `Hydrophobic Effect`
4. **Verify Completion:** Click **Verify Bonds**. Ensure status displays **Complete**.

---

### 4. DOK 4: Enzyme Inhibitor Analytics
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 enzyme kinetics and inhibitor checklist questions.
3. **Interact:** Scroll down to the **Enzyme Inhibitor Analytics** workspace. Select parameters to match competitive inhibition kinetics:
   * **Inhibitor Class Type:** `Competitive Inhibitor`
   * **Michaelis Constant (Km):** `Increases`
   * **Maximum Velocity (Vmax):** `Unchanged`
4. **Verify Completion:** Click **Verify Kinetics**. Ensure status displays **Complete**.

---

## Part 2: B.LS1.7 (Cellular Respiration Energy Transfer) UI Validation

### 1. DOK 1: Glycolysis Inputs & Outputs
1. **Select Standard:** Choose **OAS B.LS1.7: Cellular Respiration** in the top dropdown.
2. **Select DOK:** Click **DOK 1**.
3. **Answer Quiz:** Answer the 3 glycolysis checklist questions.
4. **Interact:** Scroll down to the **Glycolysis Inputs & Outputs** workspace. Select roles:
   * **Glucose molecule starting state:** `Reactant (Starting Substrate)`
   * **Cytosolic NADH molecule:** `Carrier Product (Reduced Electron Carrier)`
   * **Net 2 ATP yield:** `Energy Output (Direct Cellular Energy)`
5. **Verify Completion:** Click **Verify Inputs/Outputs**. Ensure status displays **Complete**.

---

### 2. DOK 2: Krebs Cycle Carbon Tracker Sorter
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 citric acid cycle carbon counting questions.
3. **Interact:** Scroll down to the **Krebs Cycle Carbon Tracker** workspace. Sort intermediates from 2C to 6C to 5C to 4C:
   ```
   1. Acetyl-CoA
   2. Citrate
   3. Alpha-Ketoglutarate
   4. Oxaloacetate
   ```
4. **Verify Completion:** Click **Verify Flow**. Ensure status displays **Complete**.

---

### 3. DOK 3: Mitochondrial Poison Simulator
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 ETC inhibitors and chemiosmosis questions.
3. **Interact:** Scroll down to the **Mitochondrial Poison Simulator** workspace. Match poisons to sites:
   * **Rotenone (Insecticide):** `Complex I (NADH Dehydrogenase)`
   * **Cyanide / Carbon Monoxide:** `Complex IV (Cytochrome Oxidase)`
   * **DNP (2,4-Dinitrophenol):** `Proton Uncoupler (Inner membrane leakage)`
4. **Verify Completion:** Click **Verify Targets**. Ensure status displays **Complete**.

---

### 4. DOK 4: Metabolic Flux Biofuel Optimizer
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 metabolic engineering and endosymbiotic origin questions.
3. **Interact:** Scroll down to the **Metabolic Flux Biofuel Optimizer** workspace. Adjust parameters:
   * **Glucose Feed Rate:** Slide to exactly `50 g/L`
   * **Oxygen Aeration Rate:** Slide to exactly `0%`
   * **Reactor Temperature:** Slide to exactly `30 °C`
4. **Verify Completion:** Click **Tune Metabolic Flux**. Ensure status displays **Complete**.

---

## Part 3: Parent report BKT Progress Verification
1. **Student Switcher:** Toggle between students in the main header.
2. **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
3. **Verify Masteries:** Ensure two new progress bars render correctly:
   * **Dynamic Mastery Estimate: B.LS1.6**
   * **Dynamic Mastery Estimate: B.LS1.7**
4. **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.
