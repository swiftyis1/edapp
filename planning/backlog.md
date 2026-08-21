# Product Backlog & Rapid Feature Iteration Pipeline

This document details upcoming product features, content roadmap plans, and the operational suggestion pipeline to roll out updates quickly based on classroom needs.

---

## 🚀 1. 90-Day Content Expansion Roadmap
To support career readiness and district-wide licensing, the platform will expand with new subjects every 90 days:

### 🎓 Planned Subjects & Pathways:
*   **Java Programming (AP Computer Science A)**:
    *   Autograded assignments matching AP College Board requirements.
    *   Uses client-side compiling (similar to Pyodide worker structure).
*   **FAA Part 107 Commercial Drone License Prep**:
    *   Interactive airspace maps, weather reading, and regulatory prep.
    *   Mock testing engine with score metrics tracked under teacher dashboard.
*   **Robotics Simulation**:
    *   Interactive physics-based Canvas/WebGL browser environments.
    *   Visual coding or Python controls mapping simulated robotic arms/drones.
*   **Game Design**:
    *   Interactive HTML5/Canvas gaming projects.
*   **Core Math & English (MS & HS)**:
    *   Strand-aligned remediation exercises.

---

## 📬 2. Rapid Teacher Feedback Loop Pipeline
Enable classroom teachers to request new features, bug fixes, or specific curriculum assignments directly in-app, with a target turnaround of **under 7 days** from request to production release.

### 🛠️ Technical Architecture

#### A. Database Schema (`TeacherFeedback` Model)
```python
class TeacherFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('bug', 'Report a Bug'),
        ('content', 'Request Curriculum/Assignment'),
        ('feature', 'Suggest a Feature'),
        ('other', 'General Feedback'),
    ]
    
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, default='content')
    subject_area = models.CharField(max_length=100, blank=True, help_text="e.g., Python Module 5, Part 107")
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### B. Dashboard Intake UI
*   **Teacher Panel**: A simple, floating feedback button leading to a dark glassmorphic modal form.
*   **Inputs**: Dropdown (`feedback_type`), Text (`subject_area`), TextArea (`description`).
*   **Confirmation Alert**: "Thanks! Our dev team reviews suggestions daily. New content requested is typically rolled out within a week."

#### C. Weekly Release Pipeline Workflow
1.  **Request Intake**: System aggregates new requests in `TeacherFeedback` table.
2.  **Implementation**: Leverage AI pairing to implement the code/content updates in hours.
3.  **Local Automated Testing**: Run `verify_python_curriculum` to ensure zero regression across lock/unlock gates, attempts limits, and roles.
4.  **Deployment**: Push changes to git and build production release within the 1-week SLA.
