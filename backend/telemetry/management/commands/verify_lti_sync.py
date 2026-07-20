import json
import uuid
import jwt
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Student, Classroom, LTIGradeSyncLog, UserProfile, StudentBKTState

class Command(BaseCommand):
    help = "Verifies LTI 1.3 OIDC login redirects, user mapping callback, automatic AGS grade passback, and retry actions"

    def handle(self, *args, **options):
        client = Client()

        # Clean up
        User.objects.filter(username__in=["lti_teacher_jane", "lti_student_bob"]).delete()
        Classroom.objects.filter(lti_context_id="canvas_course_bio_101").delete()

        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 9")
        self.stdout.write("==================================================")

        # ----------------------------------------------------
        # Test Case 1: LTI 1.3 OIDC login redirects
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 1] Initiating OIDC login flow...")
        
        response = client.get("/api/lti/login/?role=student")
        assert response.status_code == 302
        redirect_url = response["Location"]
        assert "/api/lti/launch/" in redirect_url
        assert "id_token=" in redirect_url
        
        self.stdout.write(self.style.SUCCESS("  - OIDC login initiate view correctly generated launch redirection!"))

        # ----------------------------------------------------
        # Test Case 2: LTI Launch Callback (Auto-User/Classroom Mapping)
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 2] Parsing launch callback token...")
        
        # Extract id_token from redirect url
        token_part = redirect_url.split("id_token=")[1].split("&")[0]
        
        response = client.get(f"/api/lti/launch/?id_token={token_part}")
        assert response.status_code == 302
        frontend_url = response["Location"]
        assert "http://localhost:3000/?lti_token=" in frontend_url
        assert "role=student" in frontend_url

        # Check DB states
        student_user = User.objects.get(username="lti_student_bob")
        assert student_user.profile.role == "student"
        
        student = Student.objects.get(user=student_user)
        assert student.lti_user_id == "lti_student_bob"
        assert student.classroom.lti_context_id == "canvas_course_bio_101"
        assert student.classroom.name == "Simulation Biology Course"
        
        self.stdout.write(self.style.SUCCESS("  - User and classroom mapped correctly from id_token launch payload!"))

        # ----------------------------------------------------
        # Test Case 3: Automatic Grade Passback (AGS) on Gameplay Completion
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 3] Simulating student gameplay level completion...")

        # Setup student BKT state
        bkt_state, _ = StudentBKTState.objects.get_or_create(student=student)
        bkt_state.transcription_p_know = 0.85
        bkt_state.translation_p_know = 0.70
        bkt_state.bonding_p_know = 0.60
        bkt_state.mutation_p_know = 0.70
        bkt_state.save()

        # Post completion event
        session_id = uuid.uuid4()
        client.force_login(student_user)
        
        response = client.post(
            "/api/telemetry/",
            data=json.dumps({
                "event_id": str(uuid.uuid4()),
                "student_id": str(student.id),
                "session_id": str(session_id),
                "timestamp": "2026-07-14T04:00:00Z",
                "event_type": "session_complete",
                "level_id": "dna_transcription_1",
                "payload": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201

        # Check that LTIGradeSyncLog item is created
        log = LTIGradeSyncLog.objects.filter(student=student).first()
        assert log is not None
        assert log.level_id == "dna_transcription_1"
        # Average mastery = (0.85 + 0.70 + 0.70 + 0.60) / 4 = 0.7125 -> OPI score = 200 + 0.7125 * 199 = 341
        assert log.score == 341
        assert log.status == "Success"

        self.stdout.write(self.style.SUCCESS(f"  - LTI Gradebook Passback automatically triggered! Synced OPI: {log.score}"))

        # ----------------------------------------------------
        # Test Case 4: Teacher logs query & manual retry
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 4] Simulating teacher configuration updates & grade retry...")
        
        # Link teacher to the mapped course classroom
        teacher_user = student.classroom.teacher
        client.force_login(teacher_user)

        # Config update
        response = client.post(
            "/api/lti/config/",
            data=json.dumps({
                "enable_sync": True,
                "score_scale": "opi"
            }),
            content_type="application/json"
        )
        assert response.status_code == 200

        # Query logs
        response = client.get("/api/lti/sync-logs/")
        assert response.status_code == 200
        logs = response.json()
        assert len(logs) == 1
        assert logs[0]["student_name"] == student.name
        
        # Retry log item
        response = client.post(
            "/api/lti/retry-sync/",
            data=json.dumps({"log_id": str(log.id)}),
            content_type="application/json"
        )
        assert response.status_code == 200
        assert "Successfully re-synced" in response.json()["message"]

        self.stdout.write(self.style.SUCCESS("  - Teacher LTI config settings and manual retry passed successfully!"))

        # Clean up
        User.objects.filter(username__in=["lti_teacher_jane", "lti_student_bob"]).delete()
        Classroom.objects.filter(lti_context_id="canvas_course_bio_101").delete()

        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 9 INTEGRATION VERIFICATION TESTS PASSED!"))
        self.stdout.write("==================================================")
