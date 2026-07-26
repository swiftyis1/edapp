import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Student, Classroom, StudentBKTState, UserProfile

class Command(BaseCommand):
    help = "Verifies real-time B.LS4.3 and B.LS4.4 BKT updates"

    def handle(self, *args, **options):
        client = Client()
        
        # Clean up
        User.objects.filter(username__in=["sprint20_student", "sprint20_teacher"]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 20")
        self.stdout.write("==================================================")

        # Setup teacher
        teacher_user = User.objects.create_user(username="sprint20_teacher", email="teacher@sprint20.edu")
        UserProfile.objects.get_or_create(user=teacher_user, role="teacher")
        classroom = Classroom.objects.create(name="Sprint 20 Biology", class_code="BIO20", teacher=teacher_user)
        
        # Setup student
        student_user = User.objects.create_user(username="sprint20_student", email="student@sprint20.edu")
        UserProfile.objects.get_or_create(user=student_user, role="student")
        student = Student.objects.create(name="Sprint20 Student", user=student_user, classroom=classroom)
        
        client.force_login(student_user)
        
        # Test Case 1: Post B.LS4.3 telemetry (Advantageous Traits)
        self.stdout.write("\n[TEST 1] Testing B.LS4.3 (Advantageous Traits) telemetry updates...")
        session_id = uuid.uuid4()
        
        # 1 incorrect, 2 correct
        for idx, correct in enumerate([False, True, True]):
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-07-26T12:00:00Z",
                    "event_type": "dok1_activity_check",
                    "level_id": "selective_pressure_match",
                    "construct_tag": "OAS.B.LS4.3",
                    "payload": {
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            
            bkt_state = StudentBKTState.objects.get(student=student)
            self.stdout.write(f"  - Post {idx + 1} ({'correct' if correct else 'incorrect'}): Advantage Mastery = {bkt_state.advantage_p_know * 100:.2f}%")
            
        assert bkt_state.advantage_p_know != 0.15

        # Test Case 2: Post B.LS4.4 telemetry (Natural Selection Adaptation)
        self.stdout.write("\n[TEST 2] Testing B.LS4.4 (Natural Selection Adaptation) telemetry updates...")
        for idx, correct in enumerate([True, True]):
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-07-26T12:05:00Z",
                    "event_type": "dok2_activity_check",
                    "level_id": "speciation_type_match",
                    "construct_tag": "OAS.B.LS4.4",
                    "payload": {
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            
            bkt_state = StudentBKTState.objects.get(student=student)
            self.stdout.write(f"  - Post {idx + 1} ({'correct' if correct else 'incorrect'}): Adaptation Mastery = {bkt_state.adaptation_p_know * 100:.2f}%")
            
        assert bkt_state.adaptation_p_know != 0.15

        # Test Case 3: Verify Parent Report response
        self.stdout.write("\n[TEST 3] Verifying B.LS4.3 and B.LS4.4 masteries in Parent Report...")
        response = client.get(f"/api/reports/parent/?student_id={student.id}")
        assert response.status_code == 200
        parent_data = response.json()
        assert parent_data["bkt_advantage_mastery"] == round(bkt_state.advantage_p_know * 100, 1)
        assert parent_data["bkt_adaptation_mastery"] == round(bkt_state.adaptation_p_know * 100, 1)
        self.stdout.write(self.style.SUCCESS(f"  - Parent report returns: Advantage = {parent_data['bkt_advantage_mastery']}%, Adaptation = {parent_data['bkt_adaptation_mastery']}%"))

        # Test Case 4: Verify Teacher Report response
        self.stdout.write("\n[TEST 4] Verifying B.LS4.3 and B.LS4.4 masteries in Teacher Report...")
        client.force_login(teacher_user)
        response = client.get("/api/reports/teacher/")
        assert response.status_code == 200
        teacher_data = response.json()
        student_entry = next(s for s in teacher_data if s["id"] == str(student.id))
        assert student_entry["bkt_advantage_mastery"] == round(bkt_state.advantage_p_know * 100, 1)
        assert student_entry["bkt_adaptation_mastery"] == round(bkt_state.adaptation_p_know * 100, 1)
        self.stdout.write(self.style.SUCCESS(f"  - Teacher report returns: Advantage = {student_entry['bkt_advantage_mastery']}%, Adaptation = {student_entry['bkt_adaptation_mastery']}%"))

        # Clean up
        student.delete()
        classroom.delete()
        teacher_user.delete()
        student_user.delete()
        
        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 20 BKT TESTS PASSED!"))
        self.stdout.write("==================================================")
