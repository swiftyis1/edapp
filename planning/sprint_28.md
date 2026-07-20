# Sprint 12: Drone Engineering & Flight Physics Simulator (Weeks 23 & 24)

**Status:** 🗄️ Backlog
**Theme:** Implement a drone assembly workbench, 3D lift/thrust physics modeler, and flight telemetry ingestion services.

---

## 📋 Iteration Checklist

### Week 23: Drone Assembly Workbench & Thrust Modeler
*   [ ] **1. Drone Components Database Schema**
    *   Create models to track frame configurations, motor KV ratings, propeller pitch, and battery voltages.
*   [ ] **2. Lift, Thrust & Aerodynamics Physics Engine**
    *   Build a 2D/3D physics calculator computing thrust-to-weight ratios, hover efficiencies, and battery discharge rates.

### Week 24: Flight In-App Telemetry & Logs
*   [ ] **3. Real-Time Flight Path Log Ingestion**
    *   Build `/api/telemetry/drone/` endpoint to ingest flight coordinates, tilt angles, motor RPMs, and power efficiency payloads.
*   [ ] **4. Drone Flight Diagnostics Panel**
    *   Add a diagnostics visualizer in the Student Portal showcasing motor temperature warnings and center-of-gravity calibration errors.
