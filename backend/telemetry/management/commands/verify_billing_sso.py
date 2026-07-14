import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from telemetry.models import Campus, Classroom, Student, UserProfile, TeacherInvite

class Command(BaseCommand):
    help = "Verifies the Stripe webhook, B2C/B2B subscription, Clever/Google SSO, teacher invites, and campus seat limit checks"

    def handle(self, *args, **options):
        client = Client()
        
        # Clean up any leftovers from previous failed runs
        User.objects.filter(username__in=[
            "google_student_sso_test", "google_teacher_sso_test", 
            "clever_admin_clever_test", "test_parent_user", 
            "district_admin_invite_tester", "invited_teacher_bob",
            "verif_student_0", "verif_student_1", "verif_student_2"
        ]).delete()
        Campus.objects.filter(name__in=["SSO Verification High"]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 3")
        self.stdout.write("==================================================")

        # ----------------------------------------------------
        # Test Case 1: Google SSO Callback & Auto-detection
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 1] Testing Google SSO callback user registration & role detection...")
        
        # Test Google Student Auto-detection
        student_email = "student_sso_test@school.org"
        response = client.post(
            "/api/auth/sso/google/callback/",
            data=json.dumps({
                "email": student_email,
                "first_name": "SSO",
                "last_name": "Student"
            }),
            content_type="application/json"
        )
        if response.status_code == 200:
            res_data = response.json()
            assert res_data["role"] == "student"
            self.stdout.write(self.style.SUCCESS(f"  - Google SSO registered student successfully: {res_data['username']}"))
        else:
            self.stdout.write(self.style.ERROR(f"  - Google SSO student registration failed: {response.content}"))
            return

        # Test Google Teacher Auto-detection
        teacher_email = "teacher_sso_test@school.edu"
        response = client.post(
            "/api/auth/sso/google/callback/",
            data=json.dumps({
                "email": teacher_email,
                "first_name": "SSO",
                "last_name": "Teacher"
            }),
            content_type="application/json"
        )
        if response.status_code == 200:
            res_data = response.json()
            assert res_data["role"] == "teacher"
            self.stdout.write(self.style.SUCCESS(f"  - Google SSO registered teacher successfully: {res_data['username']}"))
        else:
            self.stdout.write(self.style.ERROR(f"  - Google SSO teacher registration failed: {response.content}"))
            return

        # ----------------------------------------------------
        # Test Case 2: Clever SSO Callback & Auto-detection
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 2] Testing Clever SSO callback role detection...")
        
        # Test Clever Admin Auto-detection
        admin_email = "admin_clever_test@district.edu"
        response = client.post(
            "/api/auth/sso/clever/callback/",
            data=json.dumps({
                "email": admin_email,
                "first_name": "SSO",
                "last_name": "Admin"
            }),
            content_type="application/json"
        )
        if response.status_code == 200:
            res_data = response.json()
            assert res_data["role"] == "admin"
            self.stdout.write(self.style.SUCCESS(f"  - Clever SSO registered Admin successfully: {res_data['username']}"))
        else:
            self.stdout.write(self.style.ERROR(f"  - Clever SSO admin registration failed: {response.content}"))
            return

        # ----------------------------------------------------
        # Test Case 3: B2C Stripe Webhook Premium Upgrade
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 3] Testing B2C Stripe webhook premium upgrade...")
        
        # Create a parent user first
        parent_user = User.objects.create_user(
            username="test_parent_user",
            email="parent_test@gmail.com",
            password="password123"
        )
        parent_profile = UserProfile.objects.create(user=parent_user, role="parent")
        
        # Simulate stripe checkout success webhook
        mock_customer = "cus_test_parent_123"
        mock_subscription = "sub_test_parent_123"
        
        response = client.post(
            "/api/billing/webhook/",
            data=json.dumps({
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "customer": mock_customer,
                        "subscription": mock_subscription,
                        "metadata": {
                            "type": "b2c",
                            "user_id": parent_user.id
                        }
                    }
                }
            }),
            content_type="application/json",
            HTTP_X_MOCK_SIGNATURE="bypass-sig"
        )
        if response.status_code == 200:
            parent_profile.refresh_from_db()
            assert parent_profile.is_premium is True
            assert parent_profile.stripe_customer_id == mock_customer
            assert parent_profile.stripe_subscription_id == mock_subscription
            assert parent_profile.subscription_status == "active"
            self.stdout.write(self.style.SUCCESS("  - B2C webhook processed successfully: Profile updated to Premium"))
        else:
            self.stdout.write(self.style.ERROR(f"  - B2C webhook failed: {response.content}"))
            return

        # ----------------------------------------------------
        # Test Case 4: Teacher Invite Code Generation & Reg
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 4] Testing Teacher Invitation System...")
        
        # Create mock campus
        campus = Campus.objects.create(name="SSO Verification High", students_active=0, seat_limit=5)
        
        # Create an admin user to make the invite
        admin_user_model = User.objects.create_user(username="district_admin_invite_tester", password="password123")
        UserProfile.objects.create(user=admin_user_model, role="admin")
        
        # Authenticate admin client
        client.force_login(admin_user_model)
        
        # Post invite creation
        response = client.post(
            "/api/admin/invites/create/",
            data=json.dumps({
                "email": "teacher_new_invite@school.org",
                "campus_id": str(campus.id)
            }),
            content_type="application/json"
        )
        if response.status_code == 201:
            res_data = response.json()
            invite_code = res_data["code"]
            self.stdout.write(self.style.SUCCESS(f"  - Generated invite code: {invite_code} for {res_data['email']} to {res_data['campus_name']}"))
        else:
            self.stdout.write(self.style.ERROR(f"  - Invite code generation failed: {response.content}"))
            return

        # Log out admin
        client.logout()

        # Register teacher using code
        response = client.post(
            "/api/auth/register-invite/",
            data=json.dumps({
                "username": "invited_teacher_bob",
                "password": "password123",
                "first_name": "Bob",
                "last_name": "Teacher",
                "invite_code": invite_code
            }),
            content_type="application/json"
        )
        if response.status_code == 201:
            res_data = response.json()
            invited_user = User.objects.get(username="invited_teacher_bob")
            assert invited_user.profile.role == "teacher"
            assert invited_user.profile.campus == campus
            # Check invite is used
            invite_obj = TeacherInvite.objects.get(code=invite_code)
            assert invite_obj.is_used is True
            self.stdout.write(self.style.SUCCESS(f"  - Registered teacher Bob successfully via invite: user campus linked to {invited_user.profile.campus.name}"))
        else:
            self.stdout.write(self.style.ERROR(f"  - Registration via invite failed: {response.content}"))
            return

        # ----------------------------------------------------
        # Test Case 5: B2B Stripe Webhook & Campus Seat limits
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 5] Testing B2B Stripe Webhook and Campus seat increases...")
        
        mock_customer_b2b = "cus_test_campus_123"
        mock_sub_b2b = "sub_test_campus_123"
        seats_purchased = 2
        
        response = client.post(
            "/api/billing/webhook/",
            data=json.dumps({
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "customer": mock_customer_b2b,
                        "subscription": mock_sub_b2b,
                        "metadata": {
                            "type": "b2b",
                            "campus_id": str(campus.id),
                            "seats": seats_purchased
                        }
                    }
                }
            }),
            content_type="application/json",
            HTTP_X_MOCK_SIGNATURE="bypass-sig"
        )
        if response.status_code == 200:
            campus.refresh_from_db()
            assert campus.seat_limit == 5 + seats_purchased  # 5 initial + 2 purchased = 7
            assert campus.stripe_customer_id == mock_customer_b2b
            assert campus.stripe_subscription_id == mock_sub_b2b
            assert campus.subscription_status == "active"
            self.stdout.write(self.style.SUCCESS(f"  - B2B Webhook processed: Campus seat limit increased from 5 to {campus.seat_limit}"))
        else:
            self.stdout.write(self.style.ERROR(f"  - B2B webhook failed: {response.content}"))
            return

        # ----------------------------------------------------
        # Test Case 6: Campus Seat Limit Enforcements on Joining
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 6] Testing seat limit enforcements when students join classrooms...")
        
        # Set campus seat limit to 2 manually to test quota enforcement
        campus.seat_limit = 2
        campus.students_active = 0
        campus.save()
        
        # Create a classroom belonging to this campus
        classroom = Classroom.objects.create(
            name="SSO Verif Class",
            teacher=invited_user,
            class_code="VER101",
            campus=campus
        )
        
        # Create 3 student users
        student_users = []
        for i in range(3):
            u = User.objects.create_user(username=f"verif_student_{i}", password="password123")
            UserProfile.objects.create(user=u, role="student")
            student_users.append(u)

        # Student 0 Joins: active seats 0 -> 1
        client.force_login(student_users[0])
        response = client.post(
            "/api/classroom/join/",
            data=json.dumps({"class_code": "VER101"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        campus.refresh_from_db()
        assert campus.students_active == 1
        self.stdout.write("  - Student 0 joined successfully. Active seats: 1/2")
        client.logout()

        # Student 1 Joins: active seats 1 -> 2
        client.force_login(student_users[1])
        response = client.post(
            "/api/classroom/join/",
            data=json.dumps({"class_code": "VER101"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        campus.refresh_from_db()
        assert campus.students_active == 2
        self.stdout.write("  - Student 1 joined successfully. Active seats: 2/2 (Limit reached)")
        client.logout()

        # Student 2 tries to Join: should FAIL
        client.force_login(student_users[2])
        response = client.post(
            "/api/classroom/join/",
            data=json.dumps({"class_code": "VER101"}),
            content_type="application/json"
        )
        assert response.status_code == 400
        campus.refresh_from_db()
        assert campus.students_active == 2
        res_err = response.json()
        assert "Seat limit reached" in res_err["error"]
        self.stdout.write(self.style.SUCCESS(f"  - Student 2 blocked from joining successfully. Error message: '{res_err['error']}'"))
        client.logout()

        # ----------------------------------------------------
        # Test Case 7: B2C Additional Household Children slots
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 7] Testing B2C Additional Household slots & multi-child premium limit...")
        
        # Link multiple students to parent
        student_a = Student.objects.create(name="Liam Smith")
        student_b = Student.objects.create(name="Sophia Smith")
        
        parent_profile.parent_students.add(student_a)
        parent_profile.parent_students.add(student_b)
        
        # Initially, slots = 1, parent is premium.
        # student_a is first (index 0 < 1) -> should be premium
        # student_b is second (index 1 >= 1) -> should not be premium
        
        client.force_login(parent_user)
        
        # Report for student_a
        response = client.get(f"/api/reports/parent/?student_id={student_a.id}")
        assert response.status_code == 200
        assert response.json()["is_premium"] is True
        self.stdout.write("  - Verified first student gets premium benefit (1/1 slots)")
        
        # Report for student_b
        response = client.get(f"/api/reports/parent/?student_id={student_b.id}")
        assert response.status_code == 200
        assert response.json()["is_premium"] is False
        self.stdout.write("  - Verified second student is basic/locked (1/1 slots)")
        
        # Purchase additional slot via webhook simulation
        response = client.post(
            "/api/billing/webhook/",
            data=json.dumps({
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "customer": mock_customer,
                        "subscription": "sub_test_parent_additional",
                        "metadata": {
                            "type": "b2c_additional",
                            "user_id": parent_user.id,
                            "slots": 1
                        }
                    }
                }
            }),
            content_type="application/json",
            HTTP_X_MOCK_SIGNATURE="bypass-sig"
        )
        assert response.status_code == 200
        parent_profile.refresh_from_db()
        assert parent_profile.premium_slots == 2
        
        # Report for student_b again
        response = client.get(f"/api/reports/parent/?student_id={student_b.id}")
        assert response.status_code == 200
        assert response.json()["is_premium"] is True
        self.stdout.write(self.style.SUCCESS("  - Verified additional B2C slot added via webhook and unlocks student_b!"))
        client.logout()

        # Clean up created verifications
        student_a.delete()
        student_b.delete()
        campus.delete()
        admin_user_model.delete()
        invited_user.delete()
        parent_user.delete()
        for u in student_users:
            u.delete()

        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 3 INTEGRATION VERIFICATION TESTS PASSED!"))
        self.stdout.write("==================================================")
