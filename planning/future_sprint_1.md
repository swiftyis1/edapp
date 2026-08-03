# Future Sprint 1: FAA Part 107 Exam Prep & Drone Ground School (Weeks 21 & 22)

**Status:** 🗄️ Backlog
**Theme:** Implement a Part 107 ground school training simulator with dynamic study modules, mock exams, and teacher telemetry tracking for FAA regulations.

---

## 📋 Iteration Checklist

### Week 21: Part 107 Quiz Engine & Interactive Modules
*   [ ] **1. Ground School Curriculum Database Schema**
    *   Create `Part107Question` and `StudentPart107Progress` models to track student scores by regulation area (Weather, Loading, Operations, Airspace, Regulations).
*   [ ] **2. Sectional Chart Visualizer**
    *   Implement an interactive Leaflet/Canvas overlay displaying FAA sectional charts (airspace boundaries, airports, obstructions) for airspace classification queries.

### Week 22: Mock Exam Simulator & Teacher Logs
*   [ ] **3. Realistic FAA 60-Question Mock Exam**
    *   Create a timed exam simulator replicating the real FAA exam constraints, dynamically sampling from target competency areas.
*   [ ] **4. Part 107 Ground School Dashboard Panel**
    *   Add a tab to the Teacher Dashboard displaying sectional map query accuracy, mock exam passing rates, and regulation weak spots.
