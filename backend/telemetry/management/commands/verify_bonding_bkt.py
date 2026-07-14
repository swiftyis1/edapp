import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Student, Classroom, StudentBKTState, UserProfile

class Command(BaseCommand):
    help = "Verifies Level 3 Chemical Bonding telemetry and real-time B.PS1.1 BKT calculations"

    def handle(self, *args, **options):
        client = Client()
        
        # Clean up
        User.objects.filter(username__in=["bonding_tester_student", "bonding_tester_teacher"]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 5")
        self.stdout.write("==================================================")

        # Setup teacher user & classroom
        teacher_user = User.objects.create_user(username="bonding_tester_teacher", email="teacher@bonding.edu")
        teacher_profile, _ = UserProfile.objects.get_or_create(user=teacher_user)
        teacher_profile.role = "teacher"
        teacher_profile.save()
        
        classroom = Classroom.objects.create(name="Bonding Chemistry", class_code="BND707", teacher=teacher_user)
        
        # Setup student user & profile
        student_user = User.objects.create_user(username="bonding_tester_student", email="student@bonding.edu")
        student_profile, _ = UserProfile.objects.get_or_create(user=student_user)
        student_profile.role = "student"
        student_profile.save()
        
        student = Student.objects.create(name="Ava Bonding", user=student_user, classroom=classroom)
        session_id = uuid.uuid4()
        
        client.force_login(student_user)

        # ----------------------------------------------------
        # Test Case 1: Post octet_rule_check attempts (B.PS1.1)
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 1] Dispatching Level 3 Chemical Bonding telemetry...")
        
        # We will make 1 mistake and 2 correct checks
        bonding_attempts = [
            ("octet_rule_check", False), # incorrect attempt
            ("octet_rule_check", True),  # correct attempt
            ("octet_rule_check", True)   # correct attempt
        ]
        
        for idx, (event, correct) in enumerate(bonding_attempts):
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-07-14T03:00:00Z",
                    "event_type": event,
                    "level_id": "chemical_bonding_3",
                    "construct_tag": "OAS.B.PS1.1",
                    "payload": {
                        "bonding_target": "H2O",
                        "is_correct": correct,
                        "shared_h1": 1 if correct else 0,
                        "shared_h2": 1
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            
            # Verify BKT updates recursively in real-time
            bkt_state = StudentBKTState.objects.get(student=student)
            self.stdout.write(f"  - Post {idx + 1} ({'correct' if correct else 'incorrect'}): BKT Bonding Mastery = {bkt_state.bonding_p_know * 100:.2f}%")
            
        bkt_state = StudentBKTState.objects.get(student=student)
        assert bkt_state.bonding_p_know != 0.15
        
        self.stdout.write(self.style.SUCCESS("  - B.PS1.1 BKT state updated successfully in real-time!"))

        # ----------------------------------------------------
        # Test Case 2: Fetch Parent Report and verify B.PS1.1
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 2] Verifying B.PS1.1 BKT score in Parent Report API...")
        
        response = client.get(f"/api/reports/parent/?student_id={student.id}")
        assert response.status_code == 200
        parent_data = response.json()
        assert "bkt_bonding_mastery" in parent_data
        assert parent_data["bkt_bonding_mastery"] == round(bkt_state.bonding_p_know * 100, 1)
        
        self.stdout.write(self.style.SUCCESS(f"  - Parent report returns bonding mastery = {parent_data['bkt_bonding_mastery']}%"))

        # ----------------------------------------------------
        # Test Case 3: Fetch Teacher Report and verify B.PS1.1
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 3] Verifying B.PS1.1 BKT score in Teacher Report API...")
        
        client.force_login(teacher_user)
        response = client.get("/api/reports/teacher/")
        assert response.status_code == 200
        teacher_data = response.json()
        
        student_entry = next(s for s in teacher_data if s["id"] == str(student.id))
        assert student_entry["bkt_bonding_mastery"] == round(bkt_state.bonding_p_know * 100, 1)
        
        self.stdout.write(self.style.SUCCESS(f"  - Teacher report returns student bonding mastery = {student_entry['bkt_bonding_mastery']}%"))

        # Clean up
        student.delete()
        classroom.delete()
        teacher_user.delete()
        student_user.delete()
        
        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 5 INTEGRATION VERIFICATION TESTS PASSED!"))
        self.stdout.write("==================================================")
