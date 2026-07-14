# Sprint 5: Physical Sciences, Standard B.PS1.1 & BKT Engine (Weeks 9 & 10)

**Theme:** Create game Level 3 (Chemical Bonding aligned to OAS B.PS1.1), configure chemical bonding telemetry logging, and integrate the Bayesian Knowledge Tracing (BKT) learning state engine.

---

## Sprint Goals & Scope

*   **Objective:** Expand game content into the physical sciences domain (Matter and its Interactions), emit structural atomic bonding telemetry, and construct a real-time BKT service to estimate student learning states.
*   **Approach:** Build a covalent/ionic bond drag-and-drop simulation canvas, and implement a BKT learning state updating algorithm in Django.

---

## 📋 Iteration Checklist

### Week 9: Level 3 Chemical Bonding (OAS B.PS1.1)

*   [x] **1. Level 3 Interactive Canvas**
    *   Design an interactive puzzle where students drag valence electrons to construct stable covalent (e.g. $H_2O$, $CO_2$) and ionic (e.g. $NaCl$) chemical bonds.
*   [x] **2. Chemical Bonding Telemetry**
    *   Emit telemetry events: `electron_share_attempt`, `octet_rule_check`, `bond_completed`, and `valence_reset`.
*   [x] **3. DRF Telemetry Storage**
    *   Add Level 3 validation schema and log bonding actions under the `OAS.B.PS1.1` construct tag in PostgreSQL JSONB.

---

### Week 10: Real-Time BKT Engine integration

*   [x] **4. Bayesian Knowledge Tracing (BKT) Service**
    *   Implement standard BKT parameters: initial knowledge $P(L_0)$, transition $P(T)$, slip $P(S)$, and guess $P(G)$ for each OAS standard tag.
*   [x] **5. Dynamic Probability Updates**
    *   Create a backend utility `bkt_service.py` to recursively update the student's mastery probability $P(L_t)$ upon receiving telemetry actions.
*   [x] **6. Performance Verification**
    *   Validate BKT state changes on consecutive correct/incorrect base-pairing and octet-matching events.
