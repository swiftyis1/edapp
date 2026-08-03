# Unified Testing Protocols Checklist (Sprints 11-26)

This document consolidates all manual and telemetry verification protocols for Sprints 11 through 26. Use the checkboxes to track complete verification of the entire application suite.

## Sprint 11 Verification Checklist

### [ ] Part 1: B.LS1.2 (Multicellular Hierarchical Systems) UI Validation

#### [ ] 1. DOK 1: Hierarchical Sorter

- [ ] **Navigate to App:** Open `http://localhost:3000`.
- [ ] **Select Standard:** Choose **OAS B.LS1.2: Multicellular Systems** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] *Note: Options are randomized. Read the choices to match the correct biological answers.*
- [ ] **Verify Workspace Unlocked:** Once completed, scroll down to the **Hierarchy Level Sorter** workspace.
- [ ] **Interact:** Click the **▲** and **▼** buttons next to each hierarchy item to sort them from smallest to largest:
```
- [ ] Organelle
- [ ] Cell
- [ ] Tissue
- [ ] Organ
- [ ] Organ System
- [ ] Organism
```
- [ ] **Verify Completion:** Once sorted correctly, verify the status bar displays **Complete** with a success message.
#### [ ] 2. DOK 2: Tissue Matrix Alignment

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 tissue-related checklist questions.
- [ ] **Interact:** Scroll down to the **Tissue Matrix Alignment** workspace. Match the dropdowns:
- [ ] **Epithelial Tissue:** Stomach lining layer
- [ ] **Connective Tissue:** Bone joints/blood
- [ ] **Muscle Tissue:** Heart wall pump
- [ ] **Nervous Tissue:** Brain cortex lining
- [ ] **Verify Completion:** Ensure the status displays **Complete**.
#### [ ] 3. DOK 3: Cardio/Respiratory Simulator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 circulatory-system checklist questions.
- [ ] **Interact:** Scroll down to the **Dual-System Oxygenation Balance** workspace.
- [ ] **Adjust Sliders:**
- [ ] Adjust **Breathing Rate** slider to between `25` and `35` breaths/min.
- [ ] Adjust **Heart Rate** slider to between `120` and `140` bpm.
- [ ] *Verify Oxygen Saturation jumps to 98% and Carbon Dioxide (pCO2) drops to 38 mmHg.*
- [ ] **Lock in Setpoint:** Click **Verify System Stability**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Bio-mimetic Kidney Synthesizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 kidney-anatomy checklist questions.
- [ ] **Interact:** Scroll down to the **Kidney Synthesizer** workspace. Configure the dropdowns:
- [ ] **Filtration Membrane:** `Cellulose acetate (semi-permeable membrane)`
- [ ] **Flow Pump Driver:** `Peristaltic micro-pump (replicates pulse blood pressure)`
- [ ] **Biocompatible Coating:** `Differentiated endothelial cell lining (prevents clotting)`
- [ ] **Verify Synthesis:** Click **Test Kidney Compatibility**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS1.3 (Maintaining Homeostasis) UI Validation

#### [ ] 1. DOK 1: Feedback Loop Classifier

- [ ] **Select Standard:** Choose **OAS B.LS1.3: Homeostasis Regulation** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 feedback checklist questions.
- [ ] **Interact:** Scroll down to the **Feedback Loop Classifier** workspace. Classify the scenarios:
- [ ] **Sweat glands activate...**: `Negative Feedback`
- [ ] **Platelets release chemicals...**: `Positive Feedback`
- [ ] **Insulin hormone lowers...**: `Negative Feedback`
- [ ] **Uterine contractions intensify...**: `Positive Feedback`
- [ ] **Verify Completion:** Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Thermoregulation Simulator

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 thermoregulation checklist questions.
- [ ] **Interact:** Scroll down to the **Thermoregulation Simulator** workspace.
- [ ] **Adjust Temp Stress:** Move the **Environmental Temp Stress** slider to a hot temperature (e.g., `40°C`).
- [ ] **Compensate:** Adjust the **Vasodilation & Sweat Active Rate** slider to keep **Core Body Temperature** at exactly `37.0°C` (at `40°C` env temp, the active rate should be tuned to `80%`).
- [ ] **Lock Setpoint:** Click **Lock Core Temperature**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Endocrine Glucose Control

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 glucose regulation checklist questions.
- [ ] **Interact:** Scroll down to the **Endocrine Glucose Control** workspace.
- [ ] **Stabilize Glucose:**
- [ ] Starting glucose level is `150 mg/dL` (Hyperglycemia).
- [ ] Click **Inject Insulin (-70)** to drop glucose to `80 mg/dL` (normal target range: `70-100`).
- [ ] **Verify Homeostasis:** Click **Verify Homeostasis Setpoint**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: PID Artificial Pancreas Tuning

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 PID controller checklist questions.
- [ ] **Interact:** Scroll down to the **PID Artificial Pancreas Controller** workspace.
- [ ] **Tune Controller:** Enter values into the text boxes:
- [ ] **Kp (Proportional):** `2.5`
- [ ] **Ki (Integral):** `0.5`
- [ ] **Kd (Derivative):** `1.2`
- [ ] **Verify Tuning:** Click **Simulate Closed Loop**. Ensure status displays **Complete**.
### [ ] Part 3: Dashboard Mastery Tracking

- [ ] **Simulate Student Telemetry:**
- [ ] Run the Django verification test script in your terminal to populate BKT telemetry:
```powershell
.\venv\Scripts\python.exe manage.py verify_sprint11_bkt
```
- [ ] **Open Dashboard:** In the top bar of the application, click **Parent Dashboard** or **Teacher Reports**.
- [ ] **Verify Mastery Estimates:** Check that **B.LS1.2** and **B.LS1.3** masteries are rendered dynamically with progress bars and color-coded mastery bands matching the database estimates.

---

## Sprint 12 Verification Checklist

### [ ] Part 1: B.LS1.4 (Cellular Division & Differentiation) UI Validation

#### [ ] 1. DOK 1: Mitosis Phases Sorter

- [ ] **Navigate to App:** Open `http://localhost:3000`.
- [ ] **Select Standard:** Choose **OAS B.LS1.4: Cell Division & Differentiation** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] *Note: Options are randomized. Read the choices to match the correct biological answers.*
- [ ] **Verify Workspace Unlocked:** Once completed, scroll down to the **Mitosis Phases Sorter** workspace.
- [ ] **Interact:** Click the **▲** and **▼** buttons next to each phase item to sort them chronologically:
```
- [ ] Prophase
- [ ] Metaphase
- [ ] Anaphase
- [ ] Telophase
```
- [ ] **Verify Completion:** Click **Verify Sequence**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Cell Cycle Regulators Matcher

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checkpoint-related checklist questions.
- [ ] **Interact:** Scroll down to the **Cell Cycle Regulators Matcher** workspace. Select correct regulator complexes:
- [ ] **G1/S Transition:** `Cyclin E - CDK2`
- [ ] **G2/M Transition:** `Cyclin B - CDK1`
- [ ] **Metaphase-to-Anaphase Transition:** `APC/C - Cdc20`
- [ ] **Verify Completion:** Click **Verify Matches**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Stem Cell Lineage Mapper

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 stem cell and differentiation checklist questions.
- [ ] **Interact:** Scroll down to the **Stem Cell Lineage Mapper** workspace. Match each embryonic germ layer:
- [ ] **Ectoderm:** `Neuron`
- [ ] **Mesoderm:** `Red Blood Cell`
- [ ] **Endoderm:** `Pancreatic Beta Cell`
- [ ] **Verify Completion:** Click **Verify Lineages**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Cancerous Control Loop

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 cancer genetics and cell cycle aberration checklist questions.
- [ ] **Interact:** Scroll down to the **Cancerous Control Loop** workspace. Toggle proteins to their healthy, tumor-suppressive states:
- [ ] **p53 (DNA Damage Sensor):** `Active`
- [ ] **Rb (G1 Transition Gate):** `Hypophosphorylated (Active)`
- [ ] **Ras (Growth Signal GTPase):** `Wildtype (GDP bound)`
- [ ] **Verify Completion:** Click **Run Checkpoint System**. Ensure status displays **Complete** with a success confirmation.
### [ ] Part 2: B.LS1.5 (Photosynthesis Energy Transformation) UI Validation

#### [ ] 1. DOK 1: Light-Dependent Reactions I/O

- [ ] **Select Standard:** Choose **OAS B.LS1.5: Photosynthesis Energy** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 chloroplast anatomy and light reactions checklist questions.
- [ ] **Interact:** Scroll down to the **Light-Dependent Reactions I/O** workspace. Select the correct input/output molecules:
- [ ] **Water Photolysis Input Reactant:** `H2O`
- [ ] **Waste Byproduct Gas Released:** `O2`
- [ ] **Reduced Electron/Proton Carrier Product:** `NADPH`
- [ ] **Verify Completion:** Click **Verify Inputs/Outputs**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Z-Scheme Electron Flow Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 action spectra and electron transport checklist questions.
- [ ] **Interact:** Scroll down to the **Z-Scheme Sorter** workspace. Arrange components in chronological order from electron release to Photosystem I excitation:
```
- [ ] H2O Splitting
- [ ] P680*
- [ ] Plastocyanin
- [ ] P700*
```
- [ ] **Verify Completion:** Click **Verify Flow**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Pigment Absorption Spectra

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 Calvin Cycle stoichiometry and limiting factor checklist questions.
- [ ] **Interact:** Scroll down to the **Pigment Absorption Spectra** workspace. Adjust light wavelength sliders to maximize absorption:
- [ ] **Blue Wavelength:** Slide to exactly `450 nm`
- [ ] **Red Wavelength:** Slide to exactly `680 nm`
- [ ] **Verify Completion:** Click **Calculate Light Absorption**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Limiting Factors Optimizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 global warming, photoinhibition, and Rubisco genetic engineering questions.
- [ ] **Interact:** Scroll down to the **Limiting Factors Optimizer** workspace. Adjust the environmental parameters:
- [ ] **CO2 Concentration:** Slide to exactly `800 ppm`
- [ ] **Temperature:** Slide to exactly `25 °C`
- [ ] **Light Intensity:** Slide to exactly `500 W/m2`
- [ ] **Verify Completion:** Click **Simulate Calvin Cycle Yield**. Ensure status displays **Complete** with optimal output achieved.
### [ ] Part 3: Parent report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two new progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS1.4**
- [ ] **Dynamic Mastery Estimate: B.LS1.5**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 13 Verification Checklist

### [ ] Part 1: B.LS1.6 (Macromolecule Synthesis) UI Validation

#### [ ] 1. DOK 1: Monomer to Polymer Match

- [ ] **Navigate to App:** Open `http://localhost:3000`.
- [ ] **Select Standard:** Choose **OAS B.LS1.6: Macromolecule Synthesis** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] *Note: Options are randomized. Read the choices to match the correct biological answers.*
- [ ] **Verify Workspace Unlocked:** Once completed, scroll down to the **Monomer to Polymer Match** workspace.
- [ ] **Interact:** Select the correct polymer class from each monomer dropdown:
- [ ] **Amino Acid:** `Protein`
- [ ] **Nucleotide:** `Nucleic Acid`
- [ ] **Monosaccharide:** `Carbohydrate`
- [ ] **Fatty Acid:** `Lipid`
- [ ] **Verify Completion:** Click **Verify Monomers**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Fatty Acid Saturation Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 saturation-related checklist questions.
- [ ] **Interact:** Scroll down to the **Fatty Acid Saturation Sorter** workspace. Match each fatty acid:
- [ ] **Stearic Acid (No double bonds):** `Saturated (Straight)`
- [ ] **Oleic Acid (1 double bond):** `Unsaturated (Bent)`
- [ ] **Linoleic Acid (2 double bonds):** `Unsaturated (Bent)`
- [ ] **Verify Completion:** Click **Verify Saturation**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Side-Chain Interaction Match

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 side-chain and folding checklist questions.
- [ ] **Interact:** Scroll down to the **Side-Chain Interaction Match** workspace. Select correct bonds:
- [ ] **Cysteine - Cysteine Linkage:** `Covalent (Disulfide Bridge)`
- [ ] **Lysine (+) - Aspartate (-) Interaction:** `Ionic (Salt Bridge)`
- [ ] **Leucine & Valine Clustering in Core:** `Hydrophobic Effect`
- [ ] **Verify Completion:** Click **Verify Bonds**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Enzyme Inhibitor Analytics

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 enzyme kinetics and inhibitor checklist questions.
- [ ] **Interact:** Scroll down to the **Enzyme Inhibitor Analytics** workspace. Select parameters to match competitive inhibition kinetics:
- [ ] **Inhibitor Class Type:** `Competitive Inhibitor`
- [ ] **Michaelis Constant (Km):** `Increases`
- [ ] **Maximum Velocity (Vmax):** `Unchanged`
- [ ] **Verify Completion:** Click **Verify Kinetics**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS1.7 (Cellular Respiration Energy Transfer) UI Validation

#### [ ] 1. DOK 1: Glycolysis Inputs & Outputs

- [ ] **Select Standard:** Choose **OAS B.LS1.7: Cellular Respiration** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 glycolysis checklist questions.
- [ ] **Interact:** Scroll down to the **Glycolysis Inputs & Outputs** workspace. Select roles:
- [ ] **Glucose molecule starting state:** `Reactant (Starting Substrate)`
- [ ] **Cytosolic NADH molecule:** `Carrier Product (Reduced Electron Carrier)`
- [ ] **Net 2 ATP yield:** `Energy Output (Direct Cellular Energy)`
- [ ] **Verify Completion:** Click **Verify Inputs/Outputs**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Krebs Cycle Carbon Tracker Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 citric acid cycle carbon counting questions.
- [ ] **Interact:** Scroll down to the **Krebs Cycle Carbon Tracker** workspace. Sort intermediates from 2C to 6C to 5C to 4C:
```
- [ ] Acetyl-CoA
- [ ] Citrate
- [ ] Alpha-Ketoglutarate
- [ ] Oxaloacetate
```
- [ ] **Verify Completion:** Click **Verify Flow**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Mitochondrial Poison Simulator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 ETC inhibitors and chemiosmosis questions.
- [ ] **Interact:** Scroll down to the **Mitochondrial Poison Simulator** workspace. Match poisons to sites:
- [ ] **Rotenone (Insecticide):** `Complex I (NADH Dehydrogenase)`
- [ ] **Cyanide / Carbon Monoxide:** `Complex IV (Cytochrome Oxidase)`
- [ ] **DNP (2,4-Dinitrophenol):** `Proton Uncoupler (Inner membrane leakage)`
- [ ] **Verify Completion:** Click **Verify Targets**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Metabolic Flux Biofuel Optimizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 metabolic engineering and endosymbiotic origin questions.
- [ ] **Interact:** Scroll down to the **Metabolic Flux Biofuel Optimizer** workspace. Adjust parameters:
- [ ] **Glucose Feed Rate:** Slide to exactly `50 g/L`
- [ ] **Oxygen Aeration Rate:** Slide to exactly `0%`
- [ ] **Reactor Temperature:** Slide to exactly `30 °C`
- [ ] **Verify Completion:** Click **Tune Metabolic Flux**. Ensure status displays **Complete**.
### [ ] Part 3: Parent report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two new progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS1.6**
- [ ] **Dynamic Mastery Estimate: B.LS1.7**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 14 Verification Checklist

### [ ] Part 1: B.LS2.1 (Carrying Capacity Factors) UI Validation

#### [ ] 1. DOK 1: Environmental Factors Sorter

- [ ] **Navigate to App:** Open `http://localhost:3000`.
- [ ] **Select Standard:** Choose **OAS B.LS2.1: Carrying Capacity Factors** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] *Note: Options are randomized. Read the choices to match the correct biological answers.*
- [ ] **Verify Workspace Unlocked:** Once completed, scroll down to the **Environmental Factors Sorter** workspace.
- [ ] **Interact:** Select the correct limiting factor category from each dropdown:
- [ ] **Spread of infectious disease in a herd:** `Density-Dependent`
- [ ] **A sudden forest wildfire:** `Density-Independent`
- [ ] **Competition for nesting sites:** `Density-Dependent`
- [ ] **A severe seasonal flood:** `Density-Independent`
- [ ] **Verify Completion:** Click **Verify Factors**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: r/K Selection Strategies

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 life-history checklist questions.
- [ ] **Interact:** Scroll down to the **r/K Selection Strategies** workspace. Match each species to its strategy:
- [ ] **Leopard Frog:** `r-selected (opportunistic)`
- [ ] **African Elephant:** `K-selected (equilibrium)`
- [ ] **Dandelion Plant:** `r-selected (opportunistic)`
- [ ] **Verify Completion:** Click **Verify Strategies**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Limiting Sandbox

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 population density and carrying capacity shift questions.
- [ ] **Interact:** Scroll down to the **Limiting Sandbox** workspace. Calibrate limiting factor sliders:
- [ ] **Drought Severity:** Slide to exactly `50%`
- [ ] **Predation Intensity:** Slide to exactly `30%`
- [ ] **Verify Completion:** Click **Calibrate Sandbox**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Sustainable Yield Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 maximum sustainable yield and Lotka-Volterra checklist questions.
- [ ] **Interact:** Scroll down to the **Sustainable Yield Tuner** workspace. Calibrate parameters:
- [ ] **Harvest Rate:** Slide to exactly `50%` (Maximum Sustainable Yield K/2 target)
- [ ] **Verify Completion:** Click **Verify Harvest Rate**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS2.2 (Biodiversity Factors) UI Validation

#### [ ] 1. DOK 1: Ecosystem Services Sorter

- [ ] **Select Standard:** Choose **OAS B.LS2.2: Biodiversity Factors** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 ecosystem services checklist questions.
- [ ] **Interact:** Scroll down to the **Ecosystem Services Sorter** workspace. Match services to classes:
- [ ] **Crops & Timber production:** `Provisioning Service`
- [ ] **Wetlands clean water purification & flood buffering:** `Regulating Service`
- [ ] **Nutrient cycling & soil formation base layers:** `Supporting Service`
- [ ] **Ecotourism & national parks recreation value:** `Cultural Service`
- [ ] **Verify Completion:** Click **Verify Services**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Trophic Cascade Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 trophic cascade and succession questions.
- [ ] **Interact:** Scroll down to the **Trophic Cascade Sorter** workspace. Arrange components in top-down trophic cascade order:
```
- [ ] Sea Otters
- [ ] Sea Urchins
- [ ] Kelp Forest
```
- [ ] **Verify Completion:** Click **Verify Cascade**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Simpson Index Calculator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 species diversity calculations and keystone questions.
- [ ] **Interact:** Scroll down to the **Simpson Index Calculator** workspace.
- [ ] **Select Answer:** Select the calculated value from the dropdown:
- [ ] **Simpson Index (D):** `0.69`
- [ ] **Verify Completion:** Click **Verify Index**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Disturbance Resilience Optimizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 disturbance resilience and biogeography questions.
- [ ] **Interact:** Scroll down to the **Disturbance Resilience Optimizer** workspace. Adjust parameters:
- [ ] **Species Richness:** Slide to exactly `15 species`
- [ ] **Species Evenness:** Slide to exactly `100%`
- [ ] **Verify Completion:** Click **Tune Resilience Parameters**. Ensure status displays **Complete**.
### [ ] Part 3: Parent report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two new progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS2.1**
- [ ] **Dynamic Mastery Estimate: B.LS2.2**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 15 Verification Checklist

### [ ] Part 1: B.LS2.3 (Cycling of Matter) UI Validation

#### [ ] 1. DOK 1: Matter Cycle Match

- [ ] **Select Standard:** Choose **OAS B.LS2.3: Cycling of Matter** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Matter Cycle Match** workspace.
- [ ] **Interact:** Select the correct cycle for each nutrient from the dropdowns:
- [ ] **Carbon Dioxide (CO2) Gas:** `Carbon Cycle`
- [ ] **Phosphate Mineral Sediments:** `Phosphorus Cycle`
- [ ] **Ammonia & Nitrogen Gas:** `Nitrogen Cycle`
- [ ] **Water Vapor & Precipitation:** `Hydrologic Cycle`
- [ ] **Verify Completion:** Click **Verify Cycles**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Aerobic vs. Anaerobic Processes

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Aerobic vs. Anaerobic Processes** workspace. Match each process:
- [ ] **Aerobic Respiration:** `Aerobic`
- [ ] **Denitrification by soil bacteria:** `Anaerobic`
- [ ] **Methanogenesis in wetland muds:** `Anaerobic`
- [ ] **Nitrification:** `Aerobic`
- [ ] **Verify Completion:** Click **Verify Processes**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Matter Flux Sandbox

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Matter Flux Sandbox** workspace. Calibrate sliders:
- [ ] **Soil Moisture Level:** Slide to exactly `60%`
- [ ] **Nitrification Efficiency:** Slide to exactly `80%`
- [ ] **Verify Completion:** Click **Calibrate Flux Sandbox**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Eutrophication Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Eutrophication Tuner** workspace. Calibrate parameters:
- [ ] **Phosphorus Runoff Limit:** Slide to exactly `10 ppm`
- [ ] **Dissolved Oxygen (DO) Goal:** Slide to exactly `8 ppm`
- [ ] **Verify Completion:** Click **Tune Eutrophication**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS2.4 (Ecosystem Energy Flow) UI Validation

#### [ ] 1. DOK 1: Trophic Level Match

- [ ] **Select Standard:** Choose **OAS B.LS2.4: Ecosystem Energy Flow** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Trophic Level Match** workspace. Match organisms to levels:
- [ ] **Marine Phytoplankton:** `Primary Producer (Autotroph)`
- [ ] **Zooplankton grazers:** `Primary Consumer (Herbivore)`
- [ ] **Northern Anchovy small schooling fish:** `Secondary Consumer (Carnivore)`
- [ ] **Bluefin Tuna large pelagic predator:** `Tertiary Consumer (Apex Predator)`
- [ ] **Verify Completion:** Click **Verify Levels**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Energy 10% Rule Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Energy 10% Rule Sorter** workspace. Arrange components in decreasing energy order:
```
- [ ] 10,000 J
- [ ] 1,000 J
- [ ] 100 J
- [ ] 10 J
```
- [ ] **Verify Completion:** Click **Verify Energy Sorter**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Trophic Biomass Matcher

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Trophic Biomass Matcher** workspace.
- [ ] **Select Answer:** Select values from the dropdowns:
- [ ] **Phytoplankton Producers:** `Low`
- [ ] **Zooplankton Primary Consumers:** `High`
- [ ] **Small Schooling Fish Secondary Consumers:** `Medium`
- [ ] **Verify Completion:** Click **Verify Biomass Matches**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Ecosystem Efficiency Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Ecosystem Efficiency Tuner** workspace. Adjust parameters:
- [ ] **Solar Insolation:** Slide to exactly `5000 W/m2`
- [ ] **Ecological Transfer Efficiency:** Slide to exactly `10%`
- [ ] **Verify Completion:** Click **Tune Efficiency**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two new progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS2.3**
- [ ] **Dynamic Mastery Estimate: B.LS2.4**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 16 Verification Checklist

### [ ] Part 1: B.LS2.5 (Carbon Cycling Spheres) UI Validation

#### [ ] 1. DOK 1: Carbon Reservoirs Sorter

- [ ] **Select Standard:** Choose **OAS B.LS2.5: Carbon Cycling Spheres** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Carbon Reservoirs Sorter** workspace.
- [ ] **Interact:** Select the correct planetary sphere for each carbon pool from the dropdowns:
- [ ] **Atmospheric CO2 Gas:** `Atmosphere`
- [ ] **Fossil Coal & Limestone Sediments:** `Geosphere`
- [ ] **Living Vegetation cellulose:** `Biosphere`
- [ ] **Dissolved Bicarbonate Ions:** `Hydrosphere`
- [ ] **Verify Completion:** Click **Verify Reservoirs**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Carbon Process Match

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Carbon Process Match** workspace. Match process paths:
- [ ] **Plant Photosynthesis:** `Atmosphere to Biosphere`
- [ ] **Industrial Coal Combustion:** `Geosphere to Atmosphere`
- [ ] **Volcanic outgassing:** `Geosphere to Atmosphere`
- [ ] **Ocean dissolution absorption:** `Atmosphere to Hydrosphere`
- [ ] **Verify Completion:** Click **Verify Processes**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Carbon Flux Simulator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Carbon Flux Simulator** workspace. Calibrate sliders:
- [ ] **Fossil Fuel Emissions:** Slide to exactly `5 GtC/yr`
- [ ] **Ocean Carbon Sink:** Slide to exactly `3 GtC/yr`
- [ ] **Verify Completion:** Click **Verify Flux Balanced**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Global Temperature Optimizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Global Temperature Optimizer** workspace. Calibrate parameters:
- [ ] **Atmospheric CO2 Concentration:** Slide to exactly `350 ppm`
- [ ] **Global Albedo Index:** Slide to exactly `30%`
- [ ] **Verify Completion:** Click **Optimize Temperature**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS2.6 (Ecosystem Stability Evaluation) UI Validation

#### [ ] 1. DOK 1: Stability Factors Sorter

- [ ] **Select Standard:** Choose **OAS B.LS2.6: Ecosystem Stability Evaluation** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Stability Factors Sorter** workspace. Match terms to definitions:
- [ ] **Ability to withstand perturbation or direct disruption without change:** `Resistance`
- [ ] **Speed and capacity of an ecosystem to recover following a disturbance:** `Resilience`
- [ ] **A state of balance around a physiological or environmental setpoint:** `Dynamic Equilibrium`
- [ ] **Verify Completion:** Click **Verify Terms**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Succession Colonizer Match

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Succession Colonizer Match** workspace. Match stage:
- [ ] **Lichens & pioneer mosses:** `Pioneer Stage (Initial colonization)`
- [ ] **Grasses, herbaceous perennials & shrubs:** `Intermediate Stage`
- [ ] **Oak & hickory climax trees:** `Climax Stage`
- [ ] **Verify Completion:** Click **Verify Succession**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Disturbance Severity Sandbox

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Disturbance Severity Sandbox** workspace.
- [ ] **Select Answer:** Slide values to targets:
- [ ] **Fire Return Interval:** Slide to exactly `20 years`
- [ ] **Disturbance Severity:** Slide to exactly `40%`
- [ ] **Verify Completion:** Click **Verify Disturbance Sandbox**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Ecosystem Recovery Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Ecosystem Recovery Planner** workspace. Adjust parameters:
- [ ] **Reforestation Planting Density:** Slide to exactly `200 trees/acre`
- [ ] **Soil Nitrogen Content:** Slide to exactly `80 ppm`
- [ ] **Verify Completion:** Click **Verify Recovery Planner**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two new progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS2.5**
- [ ] **Dynamic Mastery Estimate: B.LS2.6**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 17 Verification Checklist

### [ ] Part 1: B.LS2.8 (Group Behavior Evidence) UI Validation

#### [ ] 1. DOK 1: Group Behavior Sorter

- [ ] **Select Standard:** Choose **OAS B.LS2.8: Group Behavior Evidence** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Group Behavior Sorter** workspace.
- [ ] **Interact:** Select individual or social behavior from the dropdowns:
- [ ] **Cooperative hunting in wolf packs:** `Social Group Behavior`
- [ ] **Visual flocking alignment in starlings:** `Social Group Behavior`
- [ ] **Monarch butterfly migration direction:** `Individual Behavior`
- [ ] **Hibernation of a black bear:** `Individual Behavior`
- [ ] **Verify Completion:** Click **Verify Behaviors**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Evolutionary Benefit Match

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Evolutionary Benefit Match** workspace. Match benefits:
- [ ] **Pack Cooperative Hunting:** `Higher per-capita net energy intake`
- [ ] **Herd Safety Signaling & Alarm Calls:** `Lower per-capita predation risk`
- [ ] **Herding Defensive Circle Formation:** `Protection of vulnerable young`
- [ ] **Verify Completion:** Click **Verify Advantages**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Flocking Density Sandbox

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Flocking Density Sandbox** workspace. Calibrate sliders:
- [ ] **Alignment Weight:** Slide to exactly `50%`
- [ ] **Cohesion Force:** Slide to exactly `40%`
- [ ] **Verify Completion:** Click **Verify Flocking Sandbox**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Group Foraging Optimizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Group Foraging Optimizer** workspace. Calibrate parameters:
- [ ] **Group Size:** Slide to exactly `12 members`
- [ ] **Scouting Radius:** Slide to exactly `8 miles`
- [ ] **Verify Completion:** Click **Calibrate Foraging**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS3.1 (Inheritable Traits Coding) UI Validation

#### [ ] 1. DOK 1: DNA to Protein Flow

- [ ] **Select Standard:** Choose **OAS B.LS3.1: Genetics Inheritable Traits** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **DNA to Protein Flow** workspace. Match descriptions:
- [ ] **Transcription:** `Synthesizing RNA from a DNA template`
- [ ] **Translation:** `Building amino acid chains from mRNA codons`
- [ ] **Replication:** `Copying DNA genome prior to cell division`
- [ ] **Verify Completion:** Click **Verify Flow**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Genotypic Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Genotypic Sorter** workspace. Classify crosses:
- [ ] **Cross BB x bb:** `F1 Monohybrid Cross (all Bb)`
- [ ] **Cross Bb x Bb:** `Monohybrid F2 Segregation (3:1 Phenotype)`
- [ ] **Cross RrYy x RrYy:** `Dihybrid F2 Assortment (9:3:3:1 Phenotype)`
- [ ] **Verify Completion:** Click **Verify Crosses**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Punnett Square Calculator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Punnett Square Calculator** workspace.
- [ ] **Select Answer:** Choose the dominant-to-recessive ratio:
- [ ] **Select Phenotypic Ratio:** `3:1 (Dominant:Recessive)`
- [ ] **Verify Completion:** Click **Verify Ratio**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Gene Linkage Map Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Gene Linkage Map Tuner** workspace. Adjust parameters:
- [ ] **Recombination Frequency A-B:** Slide to exactly `15%`
- [ ] **Recombination Frequency B-C:** Slide to exactly `10%`
- [ ] **Verify Completion:** Click **Chromosome Map Verified**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two new progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS2.8**
- [ ] **Dynamic Mastery Estimate: B.LS3.1**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 18 Verification Checklist

### [ ] Part 1: B.LS3.2 (Genetic Variation Viable Errors) UI Validation

#### [ ] 1. DOK 1: Meiosis Stage Match

- [ ] **Select Standard:** Choose **OAS B.LS3.2: Genetic Variation Viable Errors** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Meiosis Stage Match** workspace.
- [ ] **Interact:** Select the correct meiotic stage for each event from the dropdowns:
- [ ] **Homologous chromosomes align & cross over:** `Prophase I`
- [ ] **Sister chromatids separate to poles:** `Anaphase II`
- [ ] **Homologous pairs separate to poles:** `Anaphase I`
- [ ] **Verify Completion:** Click **Verify Meiosis Stages**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Mutation Type Match

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Mutation Type Match** workspace. Match mutation events:
- [ ] **Insertion of single base shifting reading frame:** `Frameshift Mutation`
- [ ] **C to T transition changing codon to Stop:** `Nonsense Mutation`
- [ ] **Substitution changing codon but keeping same amino acid:** `Silent Mutation`
- [ ] **Verify Completion:** Click **Verify Mutations**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Crossing Over Sandbox

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Crossing Over Sandbox** workspace. Calibrate sliders:
- [ ] **Chiasmata Count:** Slide to exactly `2 chiasmata`
- [ ] **Meiotic Spindle Tension:** Slide to exactly `70%`
- [ ] **Verify Completion:** Click **Verify Crossing Over**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Mutation Survival Optimizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Mutation Survival Optimizer** workspace. Calibrate parameters:
- [ ] **Mutagen Dosage:** Slide to exactly `5 rads`
- [ ] **DNA Repair Efficiency:** Slide to exactly `90%`
- [ ] **Verify Completion:** Click **Verify Survival Planner**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS3.3 (Statistics of Trait Distribution) UI Validation

#### [ ] 1. DOK 1: Distribution Types Match

- [ ] **Select Standard:** Choose **OAS B.LS3.3: Statistics of Trait Distribution** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Distribution Types Match** workspace. Match traits:
- [ ] **Human height / Polygenic inheritance:** `Normal Distribution (Bell Curve)`
- [ ] **Pea seed color / Single-gene dominant:** `Bimodal / Discrete Distribution`
- [ ] **Direct directional selection impact:** `Skewed Distribution`
- [ ] **Verify Completion:** Click **Verify Distributions**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Selection Type Match

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Selection Type Match** workspace. Classify events:
- [ ] **Extremes favored, intermediates selected against:** `Disruptive Selection`
- [ ] **One extreme favored, shifting mean value:** `Directional Selection`
- [ ] **Intermediates favored, narrowing variance range:** `Stabilizing Selection`
- [ ] **Verify Completion:** Click **Verify Selection Types**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Trait Frequency Calculator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Trait Frequency Calculator** workspace.
- [ ] **Select Answer:** Solve for allele frequency:
- [ ] **Select Allele Frequency q:** `q = 0.30`
- [ ] **Verify Completion:** Click **Verify Hardy-Weinberg**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Hardy-Weinberg Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Hardy-Weinberg Tuner** workspace. Adjust parameters:
- [ ] **Initial p Allele Frequency:** Slide to exactly `70%`
- [ ] **Selection Coefficient against q:** Slide to exactly `20%`
- [ ] **Verify Completion:** Click **Verify Tuner**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two new progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS3.2**
- [ ] **Dynamic Mastery Estimate: B.LS3.3**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 19 Verification Checklist

### [ ] Part 1: B.LS4.1 (Common Ancestry Evidence) UI Validation

#### [ ] 1. DOK 1: Anatomical Sorter

- [ ] **Select Standard:** Choose **OAS B.LS4.1: Common Ancestry Evidence** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question checklist quiz correctly.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Anatomical Sorter** workspace.
- [ ] **Interact:** Classify each structure type from the dropdown:
- [ ] **Human arm skeletal layout:** `Homologous Structure`
- [ ] **Whale flipper skeletal layout:** `Homologous Structure`
- [ ] **Insect wing vs. bird wing:** `Analogous Structure`
- [ ] **Bat wing skeletal layout:** `Homologous Structure`
- [ ] **Verify Completion:** Click **Verify Structures**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Evolutionary Evidence Match

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Evolutionary Evidence Match** workspace. Select the definitions:
- [ ] **Fossil record transition sequences:** `Chronological sequencing of skeletal forms`
- [ ] **Amino acid sequence similarity:** `Biochemical comparison of shared proteins`
- [ ] **Vestigial structures:** `Evolutionary remnants of ancestral lifestyles`
- [ ] **Verify Completion:** Click **Verify Evidence**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Phylogenetic Tree Sandbox

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Phylogenetic Tree Sandbox** workspace. Calibrate sliders:
- [ ] **Root Evolutionary Distance:** Slide to exactly `40 Mya`
- [ ] **Node Bifurcation Angle:** Slide to exactly `30°`
- [ ] **Verify Completion:** Click **Verify Cladogram Sandbox**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Cladogram Optimizer

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Cladogram Optimizer** workspace. Calibrate parameters:
- [ ] **Species Count:** Slide to exactly `6 species`
- [ ] **Outgroup Distance Index:** Slide to exactly `8 index`
- [ ] **Verify Completion:** Click **Optimize Cladogram**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS4.2 (Natural Selection Drivers) UI Validation

#### [ ] 1. DOK 1: Four Postulates Match

- [ ] **Select Standard:** Choose **OAS B.LS4.2: Natural Selection Drivers** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Verify Workspace Unlocked:** Scroll down to the workspace. Match postulates:
- [ ] **Overproduction of Offspring:** Match to the correct definition.
- [ ] **Inheritable Variation:** Match to the correct definition.
- [ ] **Struggle for Existence:** Match to the correct definition.
- [ ] **Differential Reproductive Success:** Match to the correct definition.
- [ ] **Verify Completion:** Click **Verify Postulates**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Selective Pressure Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Selective Pressure Sorter** workspace. Classify pressures:
- [ ] **Temperature, Salinity:** `Abiotic Pressure`
- [ ] **Predation, Competitors:** `Biotic Pressure`
- [ ] **Verify Completion:** Click **Verify Pressures**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Population Growth Simulator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Population Growth Simulator** workspace. Calibrate parameters:
- [ ] **Carrying Capacity (K):** Slide to exactly `400 individuals`
- [ ] **Growth Rate (r):** Slide to exactly `0.4`
- [ ] **Verify Completion:** Click **Run Simulation**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Resource Competition Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Resource Competition Tuner** workspace. Calibrate sliders:
- [ ] **Species A Consumption Rate:** Slide to exactly `4 units/day`
- [ ] **Species B Consumption Rate:** Slide to exactly `2 units/day`
- [ ] **Verify Completion:** Click **Run Competition Model**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure two progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS4.1**
- [ ] **Dynamic Mastery Estimate: B.LS4.2**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 20 Verification Checklist

### [ ] Part 1: B.LS4.3 (Advantageous Traits Frequency) UI Validation

#### [ ] 1. DOK 1: Selective Pressure Match

- [ ] **Select Standard:** Choose **OAS B.LS4.3: Advantageous Traits Frequency** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question checklist quiz correctly.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Selective Pressure Match** workspace.
- [ ] **Interact:** Select the correct outcomes from the dropdowns:
- [ ] **Widespread Antibiotic usage:** `Selects for plasmid-borne resistance alleles`
- [ ] **Coal factory soot on birch trees:** `Selects for melanic (darker) phenotype moths`
- [ ] **Agricultural herbicide application:** `Selects for detoxifying enzyme mutation alleles`
- [ ] **Verify Completion:** Click **Verify Selection Outcomes**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Trait Advantage Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Trait Advantage Sorter** workspace. Classify events:
- [ ] **Lactose tolerance mutation in pastoral populations:** `Positive Selection (Advantageous)`
- [ ] **Tay-Sachs recessive lethal allele:** `Negative Selection (Deleterious)`
- [ ] **Random survival of red feathers after wildfire:** `Genetic Drift (Neutral / Stochastic)`
- [ ] **Verify Completion:** Click **Classify Trait Advantages**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Allele Frequency Calculator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Allele Frequency Calculator** workspace.
- [ ] **Select Answer:** Solve for next-generation allele frequencies:
- [ ] **Select q Allele Frequency:** `q = 0.30`
- [ ] **Verify Completion:** Click **Calculate Frequencies**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Advantageous Drift Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Advantageous Drift Tuner** workspace. Calibrate parameters:
- [ ] **Advantageous Allele Mutation Rate:** Slide to exactly `2.0%`
- [ ] **Bottleneck Population Size:** Slide to exactly `50`
- [ ] **Verify Completion:** Click **Verify Drift Model**. Ensure status displays **Complete**.
### [ ] Part 2: B.LS4.4 (Natural Selection Adaptation) UI Validation

#### [ ] 1. DOK 1: Adaptation Types Match

- [ ] **Select Standard:** Choose **OAS B.LS4.4: Natural Selection Adaptation** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Adaptation Types Match** workspace.
- [ ] **Interact:** Match adaptation categories:
- [ ] **Fever/shivering core biochemical regulation:** `Physiological Adaptation`
- [ ] **Seasonal bird migration / Pack hunting:** `Behavioral Adaptation`
- [ ] **Cacti spines / Camouflage coloration:** `Structural Adaptation`
- [ ] **Verify Completion:** Click **Verify Adaptation Types**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Speciation Driver Match

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Speciation Driver Match** workspace. Classify drivers:
- [ ] **Glacier severing a beetle population:** `Allopatric (Geographic Isolation)`
- [ ] **Different mating song calls in same forest:** `Sympatric (Behavioral Divergence)`
- [ ] **Foraging on different insect hosts in canopy:** `Sympatric (Ecological Niche Shift)`
- [ ] **Verify Completion:** Click **Verify Speciation Drivers**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Speciation Radiation Sandbox

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Speciation Radiation Sandbox** workspace. Calibrate sliders:
- [ ] **Island Migration Rate:** Slide to exactly `20%`
- [ ] **Selection Coefficient (s):** Slide to exactly `0.3`
- [ ] **Verify Completion:** Click **Verify Radiation Driver**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: Adaptive Landscape Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Adaptive Landscape Tuner** workspace. Calibrate sliders:
- [ ] **Fitness Peak Elevation:** Slide to exactly `90%`
- [ ] **Phenotypic Variance Width:** Slide to exactly `10%`
- [ ] **Verify Completion:** Click **Verify Adaptive Landscape**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS4.3**
- [ ] **Dynamic Mastery Estimate: B.LS4.4**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 21 Verification Checklist

### [ ] Part 1: B.LS4.5 (Species Extinction & Environmental Shifts) UI Validation

#### [ ] 1. DOK 1: Stressor Matching

- [ ] **Select Standard:** Choose **OAS B.LS4.5: Species Extinction & Environmental Shifts** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3-question checklist quiz correctly.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Stressor Matching** workspace.
- [ ] **Interact:** Select the correct risk levels from the dropdowns:
- [ ] **Complete Habitat Loss / Deforestation:** `Extreme Risk (Direct Extirpation)`
- [ ] **Decadal Climate Change Shifts:** `High Risk (Requires Range Shift)`
- [ ] **Localized Overexploitation:** `Moderate Risk (Targeted Harvesting)`
- [ ] **Background Invasive Species Pressure:** `Low Risk (Localized Competition)`
- [ ] **Verify Completion:** Click **Verify Stressors**. Ensure status displays **Complete** (indicated by ✓ Stressors Mapped).
#### [ ] 2. DOK 2: Environmental Shift Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Environmental Shift Sorter** workspace. Classify factors:
- [ ] **Decadal Drought Frequency:** `Abiotic`
- [ ] **Invasive Predator Colonization:** `Biotic`
- [ ] **Fungal Pathogen Epidemic:** `Biotic`
- [ ] **Increased Wildfire Frequency:** `Abiotic`
- [ ] **Verify Completion:** Click **Verify Factors**. Ensure status displays **Complete** (indicated by ✓ Factors Sorted).
#### [ ] 3. DOK 3: Trait Survival Simulator

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Trait Survival Simulator** workspace. Calibrate parameters:
- [ ] **Initial Trait Value:** Slide to exactly `40`
- [ ] **Temperature Shift Rate:** Slide to exactly `4 °C/decade`
- [ ] **Verify Completion:** Click **Run Adaptive Simulation**. Ensure status displays **Complete** (indicated by ✓ Simulation Optimally Tuned).
#### [ ] 4. DOK 4: Extinction Risk Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Extinction Risk Planner** workspace. Calibrate parameters:
- [ ] **Conservation Funding:** Slide to exactly `$8M`
- [ ] **Corridor Connections:** Slide to exactly `4 zones`
- [ ] **Verify Completion:** Click **Evaluate Conservation Plan**. Ensure status displays **Complete** (indicated by ✓ Viability Plan Approved).
### [ ] Part 2: PS.PS1.2 (Electron States & Chemical Reactions) UI Validation

#### [ ] 1. DOK 1: Electron Configuration Match

- [ ] **Select Standard:** Choose **OAS PS.PS1.2: Electron States & Chemical Reactions** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Verify Workspace Unlocked:** Scroll down to the **Electron Configuration Match** workspace.
- [ ] **Interact:** Match elements:
- [ ] **Sodium (Na):** `1 Valence Electron (Group 1 Metal)`
- [ ] **Chlorine (Cl):** `7 Valence Electrons (Group 17 Halogen)`
- [ ] **Oxygen (O):** `6 Valence Electrons (Group 16 Nonmetal)`
- [ ] **Neon (Ne):** `8 Valence Electrons (Complete Octet)`
- [ ] **Verify Completion:** Click **Verify Configurations**. Ensure status displays **Complete** (indicated by ✓ Valence Configurations Mapped).
#### [ ] 2. DOK 2: Reaction Class Sorter

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Reaction Class Sorter** workspace. Classify reactions:
- [ ] **2H₂ + O₂ → 2H₂O:** `Synthesis`
- [ ] **CaCO₃ → CaO + CO₂:** `Decomposition`
- [ ] **CH₄ + 2O₂ → CO₂ + 2H₂O:** `Combustion`
- [ ] **Zn + 2HCl → ZnCl₂ + H₂:** `Replacement`
- [ ] **Verify Completion:** Click **Verify Reactions**. Ensure status displays **Complete** (indicated by ✓ Reactions Classified).
#### [ ] 3. DOK 3: Balancing Equation Solver

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Balancing Equation Solver** workspace. Calibrate coefficients:
- [ ] **Reactant N2 Coefficient (a):** Slide to exactly `1`
- [ ] **Reactant H2 Coefficient (b):** Slide to exactly `3`
- [ ] **Product NH3 Coefficient (c):** Slide to exactly `2`
- [ ] **Verify Completion:** Click **Verify Equation Balancing**. Ensure status displays **Complete** (indicated by ✓ Equation Balanced).
#### [ ] 4. DOK 4: Reaction Energy Landscape Tuner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll down to the **Reaction Energy Landscape Tuner** workspace. Calibrate parameters:
- [ ] **Activation Energy (Ea):** Slide to exactly `40 kJ`
- [ ] **Net Reaction Energy (ΔH):** Slide to exactly `-60 kJ`
- [ ] **Verify Completion:** Click **Tuner Energy Landscape**. Ensure status displays **Complete** (indicated by ✓ Reaction Energy Landscape Optimized).
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: B.LS4.5**
- [ ] **Dynamic Mastery Estimate: PS.PS1.2**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 22 Verification Checklist

### [ ] Part 1: PS.PS1.5 (Reaction Rates Factors) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS1.5: Reaction Rates Factors** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions correctly to unlock the workspace.
- [ ] **Interact:** Select the matching descriptions for each concept:
- [ ] **Concept A: Fundamental Principle:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B: System Variables:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C: Boundary Conditions:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete** (indicated by ✓ Verified Concept).
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll to the workspace and sort the items:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete** (indicated by ✓ Verified Sorting).
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Adjust variables to hit the target:
- [ ] **Primary Variable:** Slide to exactly `30%` (or tune until output is in `75 - 85` units)
- [ ] **Secondary Variable:** Slide to exactly `50%` (or tune until output is in `75 - 85` units)
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete** (indicated by ✓ Calibration Validated).
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Configure system parameters:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete** (indicated by ✓ System Design Approved).
### [ ] Part 2: PS.PS1.7 (Conservation of Mass) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS1.7: Conservation of Mass** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select matching descriptions:
- [ ] **Concept A:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Sort:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Calibrate sliders (e.g., `30%` and `50%`) to get output in the target zone `75 - 85`.
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: PS.PS1.5**
- [ ] **Dynamic Mastery Estimate: PS.PS1.7**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 23 Verification Checklist

### [ ] Part 1: PS.PS2.5 (Electromagnetic Induction) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS2.5: Electromagnetic Induction** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions correctly to unlock the workspace.
- [ ] **Interact:** Select the matching descriptions for each concept:
- [ ] **Concept A: Fundamental Principle:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B: System Variables:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C: Boundary Conditions:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete** (indicated by ✓ Verified Concept).
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll to the workspace and sort the items:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete** (indicated by ✓ Verified Sorting).
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Adjust variables to hit the target:
- [ ] **Primary Variable:** Slide to exactly `30%` (or tune until output is in `75 - 85` units)
- [ ] **Secondary Variable:** Slide to exactly `50%` (or tune until output is in `75 - 85` units)
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete** (indicated by ✓ Calibration Validated).
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Configure system parameters:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete** (indicated by ✓ System Design Approved).
### [ ] Part 2: PS.PS3.1 (Computational Energy Flows) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS3.1: Computational Energy Flows** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select matching descriptions:
- [ ] **Concept A:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Sort:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Calibrate sliders (e.g., `30%` and `50%`) to get output in the target zone `75 - 85`.
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: PS.PS2.5**
- [ ] **Dynamic Mastery Estimate: PS.PS3.1**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 24 Verification Checklist

### [ ] Part 1: PS.PS3.2 (Macroscopic Energy Storage) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS3.2: Macroscopic Energy Storage** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions correctly to unlock the workspace.
- [ ] **Interact:** Select the matching descriptions for each concept:
- [ ] **Concept A: Fundamental Principle:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B: System Variables:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C: Boundary Conditions:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete** (indicated by ✓ Verified Concept).
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll to the workspace and sort the items:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete** (indicated by ✓ Verified Sorting).
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Adjust variables to hit the target:
- [ ] **Primary Variable:** Slide to exactly `30%` (or tune until output is in `75 - 85` units)
- [ ] **Secondary Variable:** Slide to exactly `50%` (or tune until output is in `75 - 85` units)
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete** (indicated by ✓ Calibration Validated).
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Configure system parameters:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete** (indicated by ✓ System Design Approved).
### [ ] Part 2: PS.PS3.3 (Energy Conversion Devices) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS3.3: Energy Conversion Devices** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select matching descriptions:
- [ ] **Concept A:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Sort:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Calibrate sliders (e.g., `30%` and `50%`) to get output in the target zone `75 - 85`.
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: PS.PS3.2**
- [ ] **Dynamic Mastery Estimate: PS.PS3.3**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 25 Verification Checklist

### [ ] Part 1: PS.PS3.4 (Thermal Energy Distribution) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS3.4: Thermal Energy Distribution** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions correctly to unlock the workspace.
- [ ] **Interact:** Select the matching descriptions for each concept:
- [ ] **Concept A: Fundamental Principle:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B: System Variables:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C: Boundary Conditions:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete** (indicated by ✓ Verified Concept).
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll to the workspace and sort the items:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete** (indicated by ✓ Verified Sorting).
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Adjust variables to hit the target:
- [ ] **Primary Variable:** Slide to exactly `30%` (or tune until output is in `75 - 85` units)
- [ ] **Secondary Variable:** Slide to exactly `50%` (or tune until output is in `75 - 85` units)
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete** (indicated by ✓ Calibration Validated).
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Configure system parameters:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete** (indicated by ✓ System Design Approved).
### [ ] Part 2: PS.PS4.1 (Wave Kinematics math) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS4.1: Wave Kinematics math** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select matching descriptions:
- [ ] **Concept A:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete**.
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Sort:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete**.
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Calibrate sliders (e.g., `30%` and `50%`) to get output in the target zone `75 - 85`.
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete**.
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Select:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete**.
### [ ] Part 3: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: PS.PS3.4**
- [ ] **Dynamic Mastery Estimate: PS.PS4.1**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---

## Sprint 26 Verification Checklist

### [ ] Part 1: PS.PS4.4 (Electromagnetic Radiation Absorption) UI Validation

#### [ ] 1. DOK 1: Concept Match

- [ ] **Select Standard:** Choose **OAS PS.PS4.4: Electromagnetic Radiation Absorption** in the top dropdown.
- [ ] **Select DOK:** Click **DOK 1**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions correctly to unlock the workspace.
- [ ] **Interact:** Select the matching descriptions for each concept:
- [ ] **Concept A: Fundamental Principle:** `Primary driver governing system interactions and initial state`
- [ ] **Concept B: System Variables:** `Dynamic parameters directly influencing kinetic and potential energy paths`
- [ ] **Concept C: Boundary Conditions:** `Closed system constraints ensuring total mass/energy conservation`
- [ ] **Verify Completion:** Click **Verify Concept**. Ensure status displays **Complete** (indicated by ✓ Verified Concept).
#### [ ] 2. DOK 2: Classification Sorting

- [ ] **Select DOK:** Click **DOK 2**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Scroll to the workspace and sort the items:
- [ ] **Thermodynamic Heat Transfer:** `conserved`
- [ ] **Closed Mass Exchange:** `conserved`
- [ ] **Kinetic Particle Velocity:** `kinetic`
- [ ] **Verify Completion:** Click **Verify Classification**. Ensure status displays **Complete** (indicated by ✓ Verified Sorting).
#### [ ] 3. DOK 3: Simulation Calibration

- [ ] **Select DOK:** Click **DOK 3**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Adjust variables to hit the target:
- [ ] **Primary Variable:** Slide to exactly `30%` (or tune until output is in `75 - 85` units)
- [ ] **Secondary Variable:** Slide to exactly `50%` (or tune until output is in `75 - 85` units)
- [ ] **Verify Completion:** Click **Validate Calibration**. Ensure status displays **Complete** (indicated by ✓ Calibration Validated).
#### [ ] 4. DOK 4: System Planner

- [ ] **Select DOK:** Click **DOK 4**.
- [ ] **Answer Quiz:** Answer the 3 checklist questions.
- [ ] **Interact:** Configure system parameters:
- [ ] **System Design Pattern:** `High-Yield Optimizing Multivariable Design`
- [ ] **Operational Target:** `Maximum Efficiency Flow Calibration`
- [ ] **Verify Completion:** Click **Submit System Plan**. Ensure status displays **Complete** (indicated by ✓ System Design Approved).
### [ ] Part 2: Parent Report BKT Progress Verification

- [ ] **Student Switcher:** Toggle between students in the main header.
- [ ] **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
- [ ] **Verify Masteries:** Ensure progress bars render correctly:
- [ ] **Dynamic Mastery Estimate: PS.PS4.4**
- [ ] **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.

---
