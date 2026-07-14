import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Student, Classroom, StudentBKTHistory, UserProfile

class Command(BaseCommand):
    help = "Verifies Google Classroom/Clever roster sync, user auto-creations, and BKT historical tracks"

    def handle(self, *args, **options):
        client = Client()
        
        # Clean up
        User.objects.filter(username__in=[
            "sync_teacher", "selena_gomez", "justin_bieber", "harry_styles",
            "albert_einstein", "marie_curie", "isaac_newton"
        ]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 6")
        self.stdout.write("==================================================")

        # Setup teacher user & profile
        teacher_user = User.objects.create_user(username="sync_teacher", email="teacher@sync.edu")
        teacher_profile, _ = UserProfile.objects.get_or_create(user=teacher_user)
        teacher_profile.role = "teacher"
        teacher_profile.save()
        
        client.force_login(teacher_user)

        # ----------------------------------------------------
        # Test Case 1: Post to Google Classroom Sync API
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 1] Dispatching Google Classroom Roster Sync...")
        
        response = client.post("/api/sync/google-classroom/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["classroom_name"] == "Google Classroom AP Biology"
        assert len(data["synced_students"]) == 3
        
        # Verify student user models were auto-created
        student_user = User.objects.get(username="selena_gomez")
        assert student_user.profile.role == "student"
        
        student_profile = Student.objects.get(user=student_user)
        assert student_profile.classroom.name == "Google Classroom AP Biology"
        
        self.stdout.write(self.style.SUCCESS("  - Google Classroom sync created students and classrooms successfully!"))

        # ----------------------------------------------------
        # Test Case 2: Post to Clever Sync API
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 2] Dispatching Clever Roster Sync...")
        
        response = client.post("/api/sync/clever/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["classroom_name"] == "Clever Integrated Science"
        assert len(data["synced_students"]) == 3
        
        clever_user = User.objects.get(username="albert_einstein")
        assert clever_user.profile.role == "student"
        
        self.stdout.write(self.style.SUCCESS("  - Clever sync created students and classrooms successfully!"))

        # ----------------------------------------------------
        # Test Case 3: Verify BKT History Logging
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 3] Generating base-pairing telemetry and checking BKTHistory...")
        
        session_id = uuid.uuid4()
        client.force_login(student_user)
        
        # Post 2 correct base pairing events
        for idx in range(2):
            resp = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student_profile.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-07-14T04:00:00Z",
                    "event_type": "pair_base",
                    "level_id": "dna_transcription_1",
                    "construct_tag": "OAS.B.LS1.1",
                    "payload": {
                        "index": idx,
                        "template_base": "T",
                        "attempted_base": "A",
                        "is_correct": True
                    }
                }),
                content_type="application/json"
            )
            assert resp.status_code == 201

        # Assert StudentBKTHistory items were created
        histories = StudentBKTHistory.objects.filter(student=student_profile)
        assert histories.count() == 2
        for h in histories:
            assert h.construct_tag == "OAS.B.LS1.1"
            self.stdout.write(f"  - Logged history point: {h.p_know*100:.1f}%")
            
        self.stdout.write(self.style.SUCCESS("  - Student BKT history points successfully logged in database!"))

        # ----------------------------------------------------
        # Test Case 4: Verify parent report response contains bkt_history array
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 4] Querying report view for BKT historical arrays...")
        
        response = client.get(f"/api/reports/parent/?student_id={student_profile.id}")
        assert response.status_code == 200
        report = response.json()
        assert "bkt_history" in report
        assert len(report["bkt_history"]) == 2
        assert report["bkt_history"][0]["p_know"] == round(histories[0].p_know * 100, 1)
        
        self.stdout.write(self.style.SUCCESS("  - Parent report returned student BKT history points correctly!"))

        # Clean up
        User.objects.filter(username__in=[
            "sync_teacher", "selena_gomez", "justin_bieber", "harry_styles",
            "albert_einstein", "marie_curie", "isaac_newton"
        ]).delete()
        
        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 6 INTEGRATION VERIFICATION TESTS PASSED!"))
        self.stdout.write("==================================================")
