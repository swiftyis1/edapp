import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Student, Classroom, Campus, InvoiceReceipt, UserProfile, TeacherInvite

class Command(BaseCommand):
    help = "Verifies school administrator profiles, metered billing, stripe invoicing webhooks, and quota enforcement"

    def handle(self, *args, **options):
        client = Client()

        # Clean up existing test users/campuses
        User.objects.filter(username__in=[
            "test_school_admin", "test_school_student", "test_school_teacher"
        ]).delete()
        Campus.objects.filter(name="Oakhaven High School").delete()

        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 7")
        self.stdout.write("==================================================")

        # ----------------------------------------------------
        # Test Case 1: Setup Campus, Admin User, and Roles
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 1] Setting up Oakhaven High School & School Admin profile...")
        
        campus = Campus.objects.create(
            name="Oakhaven High School",
            seat_limit=100,
            students_active=0,
            subscription_status="active"
        )
        
        admin_user = User.objects.create_user(username="test_school_admin", email="admin@oakhaven.edu")
        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.role = "school_admin"
        admin_profile.campus = campus
        admin_profile.save()

        teacher_user = User.objects.create_user(username="test_school_teacher")
        teacher_profile, _ = UserProfile.objects.get_or_create(user=teacher_user)
        teacher_profile.role = "teacher"
        teacher_profile.campus = campus
        teacher_profile.save()

        classroom = Classroom.objects.create(
            name="Honors Biology Period 1",
            teacher=teacher_user,
            campus=campus,
            class_code="OAK101"
        )

        student_user = User.objects.create_user(username="test_school_student")
        student_profile, _ = UserProfile.objects.get_or_create(user=student_user)
        student_profile.role = "student"
        student_profile.save()

        student = Student.objects.create(
            user=student_user,
            name="Student Joe",
            classroom=classroom
        )
        campus.students_active = 1
        campus.save()

        # Add teacher invite code
        TeacherInvite.objects.create(
            code="OAKINV99",
            campus=campus,
            is_used=False
        )

        self.stdout.write(self.style.SUCCESS("  - School administrator and campus test setup completed successfully."))

        # ----------------------------------------------------
        # Test Case 2: Test Stripe Webhook invoice.paid (Creates InvoiceReceipt)
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 2] Simulating Stripe invoice.paid webhook...")
        
        webhook_payload = {
            "type": "invoice.paid",
            "data": {
                "object": {
                    "id": "in_test_12345",
                    "customer": "cust_test_school",
                    "subscription": "sub_test_school",
                    "amount_paid": 30000,  # $300.00 -> 50 seats
                    "hosted_invoice_url": "https://stripe.com/mock-oakhaven-invoice.pdf"
                }
            }
        }
        
        # Link campus to subscription to match webhook lookups
        campus.stripe_subscription_id = "sub_test_school"
        campus.save()

        response = client.post(
            "/api/billing/webhook/",
            data=json.dumps(webhook_payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json()["event_processed"] == "invoice.paid"

        # Verify InvoiceReceipt is generated
        invoice = InvoiceReceipt.objects.filter(campus=campus).first()
        assert invoice is not None
        assert invoice.stripe_invoice_id == "in_test_12345"
        assert invoice.amount_paid == 300.00
        assert invoice.seats_purchased == 50
        assert invoice.invoice_pdf_url == "https://stripe.com/mock-oakhaven-invoice.pdf"
        
        self.stdout.write(self.style.SUCCESS("  - Stripe webhook 'invoice.paid' credited campus subscription and logged receipt!"))

        # ----------------------------------------------------
        # Test Case 3: Test School Admin Dashboard Report API
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 3] Querying reports/school-admin dashboard endpoint...")
        
        client.force_login(admin_user)
        response = client.get("/api/reports/school-admin/")
        assert response.status_code == 200
        data = response.json()
        
        assert data["campus_name"] == "Oakhaven High School"
        assert data["seat_limit"] == 100
        assert data["active_students"] == 1
        assert len(data["invoices"]) == 1
        assert data["invoices"][0]["stripe_invoice_id"] == "in_test_12345"
        assert len(data["invites"]) == 1
        assert data["invites"][0]["code"] == "OAKINV99"

        self.stdout.write(self.style.SUCCESS("  - School administrator dashboard data verified successfully."))

        # ----------------------------------------------------
        # Test Case 4: Simulate Payment Failure (Freeze Campus License) & Block Telemetry
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 4] Simulating Stripe invoice.payment_failed webhook (Account Freeze)...")
        
        webhook_fail_payload = {
            "type": "invoice.payment_failed",
            "data": {
                "object": {
                    "subscription": "sub_test_school",
                    "customer": "cust_test_school"
                }
            }
        }
        
        response = client.post(
            "/api/billing/webhook/",
            data=json.dumps(webhook_fail_payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        
        # Verify campus subscription_status was frozen
        campus.refresh_from_db()
        assert campus.subscription_status == "unpaid"

        # Assert student's telemetry is BLOCKED due to frozen campus account
        client.force_login(student_user)
        response = client.post(
            "/api/telemetry/",
            data=json.dumps({
                "event_id": str(uuid.uuid4()),
                "student_id": str(student.id),
                "session_id": str(uuid.uuid4()),
                "timestamp": "2026-07-14T04:00:00Z",
                "event_type": "pair_base",
                "level_id": "dna_transcription_1",
                "construct_tag": "OAS.B.LS1.1",
                "payload": {
                    "index": 0,
                    "template_base": "T",
                    "attempted_base": "A",
                    "is_correct": True
                }
            }),
            content_type="application/json"
        )
        # Expected: Payment Required block (402)
        assert response.status_code == 402
        assert "frozen or unpaid" in response.json()["message"]

        # Assert joining classroom is BLOCKED
        response = client.post(
            "/api/classroom/join/",
            data=json.dumps({"class_code": "OAK101"}),
            content_type="application/json"
        )
        # Expected: Bad Request block (400)
        assert response.status_code == 400
        assert "frozen or unpaid" in response.json()["error"]

        self.stdout.write(self.style.SUCCESS("  - Account freeze correctly blocks telemetry uploads & classroom joins!"))

        # ----------------------------------------------------
        # Test Case 5: Restore Campus License & Verify Access Resumes
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 5] Unfreezing campus account and checking telemetry resumes...")
        
        campus.subscription_status = "active"
        campus.save()

        # Telemetry should pass now
        response = client.post(
            "/api/telemetry/",
            data=json.dumps({
                "event_id": str(uuid.uuid4()),
                "student_id": str(student.id),
                "session_id": str(uuid.uuid4()),
                "timestamp": "2026-07-14T04:00:00Z",
                "event_type": "pair_base",
                "level_id": "dna_transcription_1",
                "construct_tag": "OAS.B.LS1.1",
                "payload": {
                    "index": 0,
                    "template_base": "T",
                    "attempted_base": "A",
                    "is_correct": True
                }
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        
        self.stdout.write(self.style.SUCCESS("  - Unfrozen account correctly restores normal gameplay and student access!"))

        # Clean up
        User.objects.filter(username__in=[
            "test_school_admin", "test_school_student", "test_school_teacher"
        ]).delete()
        campus.delete()

        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 7 INTEGRATION VERIFICATION TESTS PASSED!"))
        self.stdout.write("==================================================")
