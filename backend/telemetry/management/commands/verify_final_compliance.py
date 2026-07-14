import json
import uuid
import zipfile
import io
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
from datetime import timedelta
from telemetry.models import Campus, Classroom, Student, StudentBKTState, TelemetryEvent, AuditLog, ReportSchedule

class Command(BaseCommand):
    help = "Verifies OSDE CSV/ZIP exports, report scheduling, database retention cleaner, and administrative audit logs"

    def handle(self, *args, **options):
        client = Client()

        # Clean up
        User.objects.filter(username__in=["district_admin_user", "student_test_user"]).delete()
        Campus.objects.filter(name="Compliance Test Campus").delete()

        self.stdout.write("==================================================")
        self.stdout.write("STARTING FINAL OSDE AUDIT & COMPLIANCE INTEGRATION VERIFICATION")
        self.stdout.write("==================================================")

        # Setup users & profiles
        admin_user = User.objects.create_user(username="district_admin_user", email="admin@district.edu")
        from telemetry.models import UserProfile
        UserProfile.objects.create(user=admin_user, role="admin")

        campus = Campus.objects.create(name="Compliance Test Campus", seat_limit=100)
        classroom = Classroom.objects.create(name="Biology Compliance Class", teacher=admin_user, class_code="COMP99", campus=campus)

        student_user = User.objects.create_user(username="student_test_user")
        student = Student.objects.create(user=student_user, name="Alice Compliance", classroom=classroom)
        
        # Setup student state
        bkt_state = StudentBKTState.objects.create(student=student)
        bkt_state.transcription_p_know = 0.95
        bkt_state.translation_p_know = 0.90
        bkt_state.bonding_p_know = 0.88
        bkt_state.save()

        # Create older telemetry event
        session = student.sessions.create()
        old_timestamp = timezone.now() - timedelta(days=400)
        old_event = TelemetryEvent.objects.create(
            client_event_id=str(uuid.uuid4()),
            student=student,
            session=session,
            timestamp=old_timestamp,
            event_type="pair_base",
            level_id="dna_transcription_1",
            construct_tag="OAS.B.LS1.1",
            payload={"is_correct": True}
        )

        client.force_login(admin_user)

        # ----------------------------------------------------
        # Test Case 1: OSDE CSV export
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 1] Testing OSDE CSV export...")
        response = client.get("/api/admin/osde-export/?export_format=csv")
        assert response.status_code == 200
        assert "text/csv" in response["Content-Type"]
        content = response.content.decode('utf-8')
        assert "Compliance Test Campus" in content
        assert "Alice Compliance" not in content # Ensure student names are de-identified/aggregated in campus table
        self.stdout.write(self.style.SUCCESS("  - OSDE CSV Compliance Report matches specification!"))

        # ----------------------------------------------------
        # Test Case 2: De-identified Telemetry ZIP archive
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 2] Testing de-identified telemetry ZIP export...")
        response = client.get("/api/admin/osde-export/?export_format=zip")
        assert response.status_code == 200
        assert "application/zip" in response["Content-Type"]
        
        # Verify ZIP contains expected csv
        zip_data = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_data) as zf:
            namelist = zf.namelist()
            assert "de_identified_telemetry.csv" in namelist
            csv_content = zf.read("de_identified_telemetry.csv").decode('utf-8')
            # Verify de-identified
            assert "Alice Compliance" not in csv_content
            assert "student_test_user" not in csv_content
            
        self.stdout.write(self.style.SUCCESS("  - FERPA-compliant de-identified telemetry ZIP contains anonymous data!"))

        # ----------------------------------------------------
        # Test Case 3: Report Scheduling
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 3] Testing progress report scheduling...")
        response = client.post(
            "/api/admin/schedule-report/",
            data=json.dumps({
                "email": "coordinator@ok.gov",
                "frequency": "monthly"
            }),
            content_type="application/json"
        )
        assert response.status_code == 200
        schedule = ReportSchedule.objects.get(email="coordinator@ok.gov")
        assert schedule.frequency == "monthly"
        self.stdout.write(self.style.SUCCESS("  - Automated report scheduling works correctly!"))

        # ----------------------------------------------------
        # Test Case 4: Data Retention Purge Task
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 4] Testing data retention purge task...")
        assert TelemetryEvent.objects.filter(id=old_event.id).exists()
        
        # Run purge view
        response = client.post("/api/admin/run-purge/")
        assert response.status_code == 200
        assert response.json()["purged_count"] >= 1
        
        # Old event should be purged
        assert not TelemetryEvent.objects.filter(id=old_event.id).exists()
        self.stdout.write(self.style.SUCCESS("  - Data retention purge deleted records older than 365 days successfully!"))

        # ----------------------------------------------------
        # Test Case 5: Audit Trail Logs
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 5] Validating administrative audit trail logs...")
        response = client.get("/api/admin/audit-logs/")
        assert response.status_code == 200
        logs = response.json()
        
        # We expect logs for: osde_export_csv, osde_export_zip, schedule_report, purge_data
        actions = [log["action_name"] for log in logs]
        assert "osde_export_csv" in actions
        assert "osde_export_zip" in actions
        assert "schedule_report" in actions
        assert "purge_data" in actions
        
        self.stdout.write(self.style.SUCCESS("  - Audit trail securely logged all compliance and admin actions!"))

        # Clean up
        User.objects.filter(username__in=["district_admin_user", "student_test_user"]).delete()
        Campus.objects.filter(name="Compliance Test Campus").delete()

        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 10 FINAL COMPLIANCE VERIFICATION TESTS PASSED!"))
        self.stdout.write("==================================================")
