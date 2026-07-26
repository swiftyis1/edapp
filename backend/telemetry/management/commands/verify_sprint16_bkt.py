import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Student, Classroom, StudentBKTState, UserProfile

class Command(BaseCommand):
    help = "Verifies real-time B.LS2.5 and B.LS2.6 BKT updates"

    def handle(self, *args, **options):
        client = Client()
        
        # Clean up
        User.objects.filter(username__in=["sprint16_student", "sprint16_teacher"]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 16")
        self.stdout.write("==================================================")

        # Setup teacher
        teacher_user = User.objects.create_user(username="sprint16_teacher", email="teacher@sprint16.edu")
        UserProfile.objects.get_or_create(user=teacher_user, role="teacher")
        classroom = Classroom.objects.create(name="Sprint 16 Biology", class_code="BIO16", teacher=teacher_user)
        
        # Setup student
        student_user = User.objects.create_user(username="sprint16_student", email="student@sprint16.edu")
        UserProfile.objects.get_or_create(user=student_user, role="student")
        student = Student.objects.create(name="Sprint16 Student", user=student_user, classroom=classroom)
        
        client.force_login(student_user)
        
        # Test Case 1: Post B.LS2.5 telemetry (Carbon Cycling Spheres)
        self.stdout.write("\n[TEST 1] Testing B.LS2.5 (Carbon Cycling Spheres) telemetry updates...")
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
                    "level_id": "carbon_reservoirs",
                    "construct_tag": "OAS.B.LS2.5",
                    "payload": {
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            
            bkt_state = StudentBKTState.objects.get(student=student)
            self.stdout.write(f"  - Post {idx + 1} ({'correct' if correct else 'incorrect'}): Carbon Mastery = {bkt_state.carbon_p_know * 100:.2f}%")
            
        assert bkt_state.carbon_p_know != 0.15

        # Test Case 2: Post B.LS2.6 telemetry (Ecosystem Stability Evaluation)
        self.stdout.write("\n[TEST 2] Testing B.LS2.6 (Ecosystem Stability Evaluation) telemetry updates...")
        for idx, correct in enumerate([True, True]):
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-07-26T12:05:00Z",
                    "event_type": "dok2_activity_check",
                    "level_id": "succession_colonizers",
                    "construct_tag": "OAS.B.LS2.6",
                    "payload": {
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            
            bkt_state = StudentBKTState.objects.get(student=student)
            self.stdout.write(f"  - Post {idx + 1} ({'correct' if correct else 'incorrect'}): Stability Mastery = {bkt_state.stability_p_know * 100:.2f}%")
            
        assert bkt_state.stability_p_know != 0.15

        # Test Case 3: Verify Parent Report response
        self.stdout.write("\n[TEST 3] Verifying B.LS2.5 and B.LS2.6 masteries in Parent Report...")
        response = client.get(f"/api/reports/parent/?student_id={student.id}")
        assert response.status_code == 200
        parent_data = response.json()
        assert parent_data["bkt_carbon_mastery"] == round(bkt_state.carbon_p_know * 100, 1)
        assert parent_data["bkt_stability_mastery"] == round(bkt_state.stability_p_know * 100, 1)
        self.stdout.write(self.style.SUCCESS(f"  - Parent report returns: Carbon = {parent_data['bkt_carbon_mastery']}%, Stability = {parent_data['bkt_stability_mastery']}%"))

        # Test Case 4: Verify Teacher Report response
        self.stdout.write("\n[TEST 4] Verifying B.LS2.5 and B.LS2.6 masteries in Teacher Report...")
        client.force_login(teacher_user)
        response = client.get("/api/reports/teacher/")
        assert response.status_code == 200
        teacher_data = response.json()
        student_entry = next(s for s in teacher_data if s["id"] == str(student.id))
        assert student_entry["bkt_carbon_mastery"] == round(bkt_state.carbon_p_know * 100, 1)
        assert student_entry["bkt_stability_mastery"] == round(bkt_state.stability_p_know * 100, 1)
        self.stdout.write(self.style.SUCCESS(f"  - Teacher report returns: Carbon = {student_entry['bkt_carbon_mastery']}%, Stability = {student_entry['bkt_stability_mastery']}%"))

        # Clean up
        student.delete()
        classroom.delete()
        teacher_user.delete()
        student_user.delete()
        
        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 16 BKT TESTS PASSED!"))
        self.stdout.write("==================================================")
