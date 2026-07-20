# Sprint 14 Manual Testing Protocol

Use this protocol to verify the carrying capacity factors, biodiversity indices, and real-time BKT telemetry updates for **B.LS2.1 (Carrying Capacity Factors)** and **B.LS2.2 (Biodiversity Factors)**.

**Verification Status:** 🏃 PENDING USER TESTING

---

## Part 1: B.LS2.1 (Carrying Capacity Factors) UI Validation

### 1. DOK 1: Environmental Factors Sorter
1. **Navigate to App:** Open `http://localhost:3000`.
2. **Select Standard:** Choose **OAS B.LS2.1: Carrying Capacity Factors** in the top dropdown.
3. **Select DOK:** Click **DOK 1**.
4. **Answer Quiz:** Answer the 3-question DOK 1 checklist quiz.
   * *Note: Options are randomized. Read the choices to match the correct biological answers.*
5. **Verify Workspace Unlocked:** Once completed, scroll down to the **Environmental Factors Sorter** workspace.
6. **Interact:** Select the correct limiting factor category from each dropdown:
   * **Spread of infectious disease in a herd:** `Density-Dependent`
   * **A sudden forest wildfire:** `Density-Independent`
   * **Competition for nesting sites:** `Density-Dependent`
   * **A severe seasonal flood:** `Density-Independent`
7. **Verify Completion:** Click **Verify Factors**. Ensure status displays **Complete**.

---

### 2. DOK 2: r/K Selection Strategies
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 life-history checklist questions.
3. **Interact:** Scroll down to the **r/K Selection Strategies** workspace. Match each species to its strategy:
   * **Leopard Frog:** `r-selected (opportunistic)`
   * **African Elephant:** `K-selected (equilibrium)`
   * **Dandelion Plant:** `r-selected (opportunistic)`
4. **Verify Completion:** Click **Verify Strategies**. Ensure status displays **Complete**.

---

### 3. DOK 3: Limiting Sandbox
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 population density and carrying capacity shift questions.
3. **Interact:** Scroll down to the **Limiting Sandbox** workspace. Calibrate limiting factor sliders:
   * **Drought Severity:** Slide to exactly `50%`
   * **Predation Intensity:** Slide to exactly `30%`
4. **Verify Completion:** Click **Calibrate Sandbox**. Ensure status displays **Complete**.

---

### 4. DOK 4: Sustainable Yield Tuner
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 maximum sustainable yield and Lotka-Volterra checklist questions.
3. **Interact:** Scroll down to the **Sustainable Yield Tuner** workspace. Calibrate parameters:
   * **Harvest Rate:** Slide to exactly `50%` (Maximum Sustainable Yield K/2 target)
4. **Verify Completion:** Click **Verify Harvest Rate**. Ensure status displays **Complete**.

---

## Part 2: B.LS2.2 (Biodiversity Factors) UI Validation

### 1. DOK 1: Ecosystem Services Sorter
1. **Select Standard:** Choose **OAS B.LS2.2: Biodiversity Factors** in the top dropdown.
2. **Select DOK:** Click **DOK 1**.
3. **Answer Quiz:** Answer the 3 ecosystem services checklist questions.
4. **Interact:** Scroll down to the **Ecosystem Services Sorter** workspace. Match services to classes:
   * **Crops & Timber production:** `Provisioning Service`
   * **Wetlands clean water purification & flood buffering:** `Regulating Service`
   * **Nutrient cycling & soil formation base layers:** `Supporting Service`
   * **Ecotourism & national parks recreation value:** `Cultural Service`
5. **Verify Completion:** Click **Verify Services**. Ensure status displays **Complete**.

---

### 2. DOK 2: Trophic Cascade Sorter
1. **Select DOK:** Click **DOK 2**.
2. **Answer Quiz:** Answer the 3 trophic cascade and succession questions.
3. **Interact:** Scroll down to the **Trophic Cascade Sorter** workspace. Arrange components in top-down trophic cascade order:
   ```
   1. Sea Otters
   2. Sea Urchins
   3. Kelp Forest
   ```
4. **Verify Completion:** Click **Verify Cascade**. Ensure status displays **Complete**.

---

### 3. DOK 3: Simpson Index Calculator
1. **Select DOK:** Click **DOK 3**.
2. **Answer Quiz:** Answer the 3 species diversity calculations and keystone questions.
3. **Interact:** Scroll down to the **Simpson Index Calculator** workspace.
4. **Select Answer:** Select the calculated value from the dropdown:
   * **Simpson Index (D):** `0.69`
5. **Verify Completion:** Click **Verify Index**. Ensure status displays **Complete**.

---

### 4. DOK 4: Disturbance Resilience Optimizer
1. **Select DOK:** Click **DOK 4**.
2. **Answer Quiz:** Answer the 3 disturbance resilience and biogeography questions.
3. **Interact:** Scroll down to the **Disturbance Resilience Optimizer** workspace. Adjust parameters:
   * **Species Richness:** Slide to exactly `15 species`
   * **Species Evenness:** Slide to exactly `100%`
4. **Verify Completion:** Click **Tune Resilience Parameters**. Ensure status displays **Complete**.

---

## Part 3: Parent report BKT Progress Verification
1. **Student Switcher:** Toggle between students in the main header.
2. **Parent Dashboard:** Scroll down to the **Parent Dashboard** panel.
3. **Verify Masteries:** Ensure two new progress bars render correctly:
   * **Dynamic Mastery Estimate: B.LS2.1**
   * **Dynamic Mastery Estimate: B.LS2.2**
4. **BKT Value Updates:** Verify that completing any activity checks updates the mastery percentages in real-time.
