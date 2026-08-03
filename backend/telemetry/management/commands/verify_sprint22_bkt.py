import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Student, Classroom, StudentBKTState, UserProfile

class Command(BaseCommand):
    help = "Verifies real-time PS.PS1.5 and PS.PS1.7 BKT updates"

    def handle(self, *args, **options):
        client = Client()
        User.objects.filter(username__in=["sprint22_student", "sprint22_teacher"]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 22")
        self.stdout.write("==================================================")

        teacher_user = User.objects.create_user(username="sprint22_teacher", email="teacher@sprint22.edu")
        UserProfile.objects.get_or_create(user=teacher_user, role="teacher")
        classroom = Classroom.objects.create(name="Sprint 22 Physical Sciences", class_code="SCI22", teacher=teacher_user)
        
        student_user = User.objects.create_user(username="sprint22_student", email="student@sprint22.edu")
        UserProfile.objects.get_or_create(user=student_user, role="student")
        student = Student.objects.create(name="Sprint22 Student", user=student_user, classroom=classroom)
        
        client.force_login(student_user)
        
        # Test Case 1: Post PS.PS1.5 (Reaction Rates Factors)
        self.stdout.write("\n[TEST 1] Testing PS.PS1.5 (Reaction Rates) telemetry updates...")
        session_id = uuid.uuid4()
        for idx, correct in enumerate([False, True, True]):
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-08-02T12:00:00Z",
                    "event_type": "dok1_activity_check",
                    "level_id": "rates_workspace",
                    "construct_tag": "OAS.PS.PS1.5",
                    "payload": {
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            bkt_state = StudentBKTState.objects.get(student=student)
            self.stdout.write(f"  - Post {idx + 1}: Rates Mastery = {bkt_state.rates_p_know * 100:.2f}%")
        assert bkt_state.rates_p_know != 0.15

        # Test Case 2: Post PS.PS1.7 (Conservation of Mass)
        self.stdout.write("\n[TEST 2] Testing PS.PS1.7 (Conservation of Mass) telemetry updates...")
        for idx, correct in enumerate([True, True]):
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-08-02T12:05:00Z",
                    "event_type": "dok2_activity_check",
                    "level_id": "conservation_workspace",
                    "construct_tag": "OAS.PS.PS1.7",
                    "payload": {
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            bkt_state = StudentBKTState.objects.get(student=student)
            self.stdout.write(f"  - Post {idx + 1}: Conservation Mastery = {bkt_state.conservation_p_know * 100:.2f}%")
        assert bkt_state.conservation_p_know != 0.15

        # Test Case 3: Verify Parent Report response
        self.stdout.write("\n[TEST 3] Verifying BKT masteries in Parent Report...")
        response = client.get(f"/api/reports/parent/?student_id={student.id}")
        assert response.status_code == 200
        parent_data = response.json()
        assert parent_data["bkt_rates_mastery"] == round(bkt_state.rates_p_know * 100, 1)
        assert parent_data["bkt_conservation_mastery"] == round(bkt_state.conservation_p_know * 100, 1)
        self.stdout.write(self.style.SUCCESS(f"  - Parent report returns: Rates = {parent_data['bkt_rates_mastery']}%, Conservation = {parent_data['bkt_conservation_mastery']}%"))

        # Test Case 4: Verify Teacher Report response
        self.stdout.write("\n[TEST 4] Verifying BKT masteries in Teacher Report...")
        client.force_login(teacher_user)
        response = client.get("/api/reports/teacher/")
        assert response.status_code == 200
        teacher_data = response.json()
        student_entry = next(s for s in teacher_data if s["id"] == str(student.id))
        assert student_entry["bkt_rates_mastery"] == round(bkt_state.rates_p_know * 100, 1)
        assert student_entry["bkt_conservation_mastery"] == round(bkt_state.conservation_p_know * 100, 1)
        self.stdout.write(self.style.SUCCESS(f"  - Teacher report returns: Rates = {student_entry['bkt_rates_mastery']}%, Conservation = {student_entry['bkt_conservation_mastery']}%"))

        # Clean up
        student.delete()
        classroom.delete()
        teacher_user.delete()
        student_user.delete()
        
        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 22 BKT TESTS PASSED!"))
        self.stdout.write("==================================================")
