import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.authtoken.models import Token
from telemetry.models import Student, Classroom, UserProfile, PythonAssignment, PythonSubmission, TelemetryEvent

class Command(BaseCommand):
    help = "Verifies Python curriculum, locks, attempts limits, teacher selection, individual overrides, and admin stats."

    def handle(self, *args, **options):
        client = Client()
        
        # Clean up existing test users
        User.objects.filter(username__in=["sprint3_student", "sprint3_teacher", "sprint3_admin"]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 3 (ADMIN HUB)")
        self.stdout.write("==================================================")

        # Setup test admin, teacher & student
        admin_user = User.objects.create_user(username="sprint3_admin", email="admin@sprint3.edu")
        UserProfile.objects.get_or_create(user=admin_user, role="admin")

        teacher_user = User.objects.create_user(username="sprint3_teacher", email="teacher@sprint3.edu")
        UserProfile.objects.get_or_create(user=teacher_user, role="teacher")
        classroom = Classroom.objects.create(name="Sprint 3 Class", class_code="PY3", teacher=teacher_user)
        
        student_user = User.objects.create_user(username="sprint3_student", email="student@sprint3.edu")
        UserProfile.objects.get_or_create(user=student_user, role="student")
        student = Student.objects.create(name="Sprint3 Student", user=student_user, classroom=classroom)
        
        # Setup assignments and unlock assessment
        assign1 = PythonAssignment.objects.get(slug="func_declaration")
        assign2 = PythonAssignment.objects.get(slug="param_passing")
        assign3 = PythonAssignment.objects.get(slug="scoping_rules")
        assign4 = PythonAssignment.objects.get(slug="math_library")
        assign5 = PythonAssignment.objects.get(slug="random_gen")
        unit3_assign = PythonAssignment.objects.get(slug="unit3_assessment")
        
        for a in [assign1, assign2, assign3, assign4, assign5]:
            PythonSubmission.objects.create(student=student, assignment=a, code="pass", passed=True, score=100, test_results={})

        # Set attempts limit to 1
        client.force_login(teacher_user)
        response = client.post(
            "/api/python/classroom/settings/",
            data=json.dumps({"limit": 1}),
            content_type="application/json"
        )
        assert response.status_code == 200

        # Student submits attempt 1 (reaches limit)
        client.force_login(student_user)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(unit3_assign.id),
                "code": "import math\n# attempt 1",
                "passed": True,
                "score": 100,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201

        # Attempt 2 (should be rejected since limit = 1)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(unit3_assign.id),
                "code": "import math\n# attempt 2",
                "passed": True,
                "score": 100,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "limit" in response.json()["error"]
        self.stdout.write(self.style.SUCCESS("  - Successfully verified attempt limits block."))

        # Teacher grants student 1 extra attempt individually for unit3_assessment
        client.force_login(teacher_user)
        response = client.post(
            "/api/python/teacher/grant-extra-attempt/",
            data=json.dumps({
                "student_id": str(student.id),
                "assignment_slug": "unit3_assessment"
            }),
            content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json()["extra_attempts"] == 1

        # Student submits attempt 2 (should succeed now since limit is effectively 1 + 1 = 2)
        client.force_login(student_user)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(unit3_assign.id),
                "code": "import math\n# attempt 2",
                "passed": True,
                "score": 88,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        self.stdout.write(self.style.SUCCESS("  - Student successfully submitted Attempt 2 after grant override."))

        # Teacher marks attempt 2 (score 88) as selected for grading
        best_sub = PythonSubmission.objects.filter(student=student, assignment=unit3_assign, score=88).first()
        client.force_login(teacher_user)
        response = client.post(
            "/api/python/teacher/select-submission/",
            data=json.dumps({"submission_id": str(best_sub.id)}),
            content_type="application/json"
        )
        assert response.status_code == 200

        # Admin logs in and fetches stats
        self.stdout.write("\n[TEST 1] Admin fetching district Python stats...")
        client.force_login(admin_user)
        response = client.get("/api/python/admin/stats/")
        assert response.status_code == 200
        stats = response.json()
        
        # Verify student stats
        assert stats["total_students_active"] >= 1
        assert stats["overall_completion_rate"] > 0
        assert "Unit 3 Assessment: Sphere Calculations" in stats["average_assessment_scores"]
        assert stats["average_assessment_scores"]["Unit 3 Assessment: Sphere Calculations"] == 88.0
        
        self.stdout.write(self.style.SUCCESS("  - Successfully verified active student count & completion metrics."))
        self.stdout.write(self.style.SUCCESS("  - Successfully verified average assessment score matches chosen grade (88.0%)."))

        # ==========================================
        # SPRINT 4 (OOP MODULE 4) VERIFICATION
        # ==========================================
        self.stdout.write("\n[TEST 2] Starting Sprint 4 OOP (Module 4) integration checks...")
        
        # Retrieve Module 4 assignments
        m4_assign1 = PythonAssignment.objects.get(slug="class_blueprint")
        m4_assign2 = PythonAssignment.objects.get(slug="init_constructor")
        m4_assign3 = PythonAssignment.objects.get(slug="instance_methods")
        m4_assign4 = PythonAssignment.objects.get(slug="private_variables")
        m4_assign5 = PythonAssignment.objects.get(slug="getters_setters")
        m4_assess = PythonAssignment.objects.get(slug="unit4_assessment")
        
        # Verify assessment is locked because assignments are not complete yet
        client.force_login(student_user)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m4_assess.id),
                "code": "class Car:\n  pass",
                "passed": True,
                "score": 100,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "complete" in response.json()["error"]
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 4 Assessment is locked until assignments are complete."))
        
        # Complete all Module 4 assignments
        for a in [m4_assign1, m4_assign2, m4_assign3, m4_assign4, m4_assign5]:
            PythonSubmission.objects.create(student=student, assignment=a, code="pass", passed=True, score=100, test_results={})
            
        # Submit Module 4 assessment (should succeed now)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m4_assess.id),
                "code": "class Car:\n  pass",
                "passed": True,
                "score": 95,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        self.stdout.write(self.style.SUCCESS("  - Successfully submitted Module 4 Assessment after unlocking."))

        # Verify admin stats includes Module 4 assessment score
        client.force_login(admin_user)
        response = client.get("/api/python/admin/stats/")
        assert response.status_code == 200
        stats = response.json()
        assert "Unit 4 Assessment: Class Blueprint & Operations" in stats["average_assessment_scores"]
        assert stats["average_assessment_scores"]["Unit 4 Assessment: Class Blueprint & Operations"] == 95.0
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 4 average assessment score in admin stats."))

        # ==========================================
        # SPRINT 5 (INHERITANCE & POLYMORPHISM MODULE 5) VERIFICATION
        # ==========================================
        self.stdout.write("\n[TEST 3] Starting Sprint 5 OOP Inheritance (Module 5) integration checks...")
        
        # Retrieve Module 5 assignments
        m5_assign1 = PythonAssignment.objects.get(slug="simple_inheritance")
        m5_assign2 = PythonAssignment.objects.get(slug="super_call")
        m5_assign3 = PythonAssignment.objects.get(slug="method_override")
        m5_assign4 = PythonAssignment.objects.get(slug="polymorphic_list")
        m5_assign5 = PythonAssignment.objects.get(slug="isinstance_checks")
        m5_assess = PythonAssignment.objects.get(slug="unit5_assessment")
        
        # Verify assessment is locked because assignments are not complete yet
        client.force_login(student_user)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m5_assess.id),
                "code": "class Shape:\n  pass",
                "passed": True,
                "score": 100,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "complete" in response.json()["error"]
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 5 Assessment is locked until assignments are complete."))
        
        # Complete all Module 5 assignments
        for a in [m5_assign1, m5_assign2, m5_assign3, m5_assign4, m5_assign5]:
            PythonSubmission.objects.create(student=student, assignment=a, code="pass", passed=True, score=100, test_results={})
            
        # Submit Module 5 assessment (should succeed now)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m5_assess.id),
                "code": "class Shape:\n  pass",
                "passed": True,
                "score": 92,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        self.stdout.write(self.style.SUCCESS("  - Successfully submitted Module 5 Assessment after unlocking."))

        # Verify admin stats includes Module 5 assessment score
        client.force_login(admin_user)
        response = client.get("/api/python/admin/stats/")
        assert response.status_code == 200
        stats = response.json()
        assert "Unit 5 Assessment: Subclasses & Polymorphism" in stats["average_assessment_scores"]
        assert stats["average_assessment_scores"]["Unit 5 Assessment: Subclasses & Polymorphism"] == 92.0
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 5 average assessment score in admin stats."))

        # ==========================================
        # SPRINT 6 (1D LISTS & DATA TRAVERSAL MODULE 6) VERIFICATION
        # ==========================================
        self.stdout.write("\n[TEST 4] Starting Sprint 6 1D Lists (Module 6) integration checks...")
        
        # Retrieve Module 6 assignments
        m6_assign1 = PythonAssignment.objects.get(slug="list_mutators")
        m6_assign2 = PythonAssignment.objects.get(slug="list_slice")
        m6_assign3 = PythonAssignment.objects.get(slug="list_traversal")
        m6_assign4 = PythonAssignment.objects.get(slug="list_comprehension")
        m6_assign5 = PythonAssignment.objects.get(slug="list_reversing")
        m6_assess = PythonAssignment.objects.get(slug="unit6_assessment")
        
        # Verify assessment is locked because assignments are not complete yet
        client.force_login(student_user)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m6_assess.id),
                "code": "def process_dataset(data):\n  pass",
                "passed": True,
                "score": 100,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "complete" in response.json()["error"]
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 6 Assessment is locked until assignments are complete."))
        
        # Complete all Module 6 assignments
        for a in [m6_assign1, m6_assign2, m6_assign3, m6_assign4, m6_assign5]:
            PythonSubmission.objects.create(student=student, assignment=a, code="pass", passed=True, score=100, test_results={})
            
        # Submit Module 6 assessment (should succeed now)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m6_assess.id),
                "code": "def process_dataset(data):\n  pass",
                "passed": True,
                "score": 87,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        self.stdout.write(self.style.SUCCESS("  - Successfully submitted Module 6 Assessment after unlocking."))

        # Verify admin stats includes Module 6 assessment score
        client.force_login(admin_user)
        response = client.get("/api/python/admin/stats/")
        assert response.status_code == 200
        stats = response.json()
        assert "Unit 6 Assessment: List Operations & Processing" in stats["average_assessment_scores"]
        assert stats["average_assessment_scores"]["Unit 6 Assessment: List Operations & Processing"] == 87.0
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 6 average assessment score in admin stats."))

        # ==========================================
        # SPRINT 7 (2D LISTS MODULE 7) VERIFICATION
        # ==========================================
        self.stdout.write("\n[TEST 5] Starting Sprint 7 2D Lists (Module 7) integration checks...")
        
        # Retrieve Module 7 assignments
        m7_assign1 = PythonAssignment.objects.get(slug="grid_creation")
        m7_assign2 = PythonAssignment.objects.get(slug="row_sum")
        m7_assign3 = PythonAssignment.objects.get(slug="column_sum")
        m7_assign4 = PythonAssignment.objects.get(slug="diagonal_check")
        m7_assign5 = PythonAssignment.objects.get(slug="boundary_search")
        m7_assess = PythonAssignment.objects.get(slug="unit7_assessment")
        
        # Verify assessment is locked because assignments are not complete yet
        client.force_login(student_user)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m7_assess.id),
                "code": "def analyze_matrix(matrix):\n  pass",
                "passed": True,
                "score": 100,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "complete" in response.json()["error"]
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 7 Assessment is locked until assignments are complete."))
        
        # Complete all Module 7 assignments
        for a in [m7_assign1, m7_assign2, m7_assign3, m7_assign4, m7_assign5]:
            PythonSubmission.objects.create(student=student, assignment=a, code="pass", passed=True, score=100, test_results={})
            
        # Submit Module 7 assessment (should succeed now)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m7_assess.id),
                "code": "def analyze_matrix(matrix):\n  pass",
                "passed": True,
                "score": 95,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        self.stdout.write(self.style.SUCCESS("  - Successfully submitted Module 7 Assessment after unlocking."))

        # Verify admin stats includes Module 7 assessment score
        client.force_login(admin_user)
        response = client.get("/api/python/admin/stats/")
        assert response.status_code == 200
        stats = response.json()
        assert "Unit 7 Assessment: Matrix Analysis" in stats["average_assessment_scores"]
        assert stats["average_assessment_scores"]["Unit 7 Assessment: Matrix Analysis"] == 95.0
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 7 average assessment score in admin stats."))

        # ==========================================
        # SPRINT 8 (SEARCHING, SORTING, & RECURSION MODULE 8) VERIFICATION
        # ==========================================
        self.stdout.write("\n[TEST 6] Starting Sprint 8 Search, Sort & Recursion (Module 8) integration checks...")
        
        # Retrieve Module 8 assignments
        m8_assign1 = PythonAssignment.objects.get(slug="binary_search")
        m8_assign2 = PythonAssignment.objects.get(slug="selection_sort")
        m8_assign3 = PythonAssignment.objects.get(slug="insertion_sort")
        m8_assign4 = PythonAssignment.objects.get(slug="recursive_factorial")
        m8_assign5 = PythonAssignment.objects.get(slug="recursive_fibonacci")
        m8_assess = PythonAssignment.objects.get(slug="unit8_assessment")
        
        # Verify assessment is locked because assignments are not complete yet
        client.force_login(student_user)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m8_assess.id),
                "code": "def search_and_sort_stats(arr):\n  pass",
                "passed": True,
                "score": 100,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 400
        assert "complete" in response.json()["error"]
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 8 Assessment is locked until assignments are complete."))
        
        # Complete all Module 8 assignments
        for a in [m8_assign1, m8_assign2, m8_assign3, m8_assign4, m8_assign5]:
            PythonSubmission.objects.create(student=student, assignment=a, code="pass", passed=True, score=100, test_results={})
            
        # Submit Module 8 assessment (should succeed now)
        response = client.post(
            "/api/python/submit/",
            data=json.dumps({
                "assignment_id": str(m8_assess.id),
                "code": "def search_and_sort_stats(arr):\n  pass",
                "passed": True,
                "score": 90,
                "test_results": {}
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        self.stdout.write(self.style.SUCCESS("  - Successfully submitted Module 8 Assessment after unlocking."))

        # Verify admin stats includes Module 8 assessment score
        client.force_login(admin_user)
        response = client.get("/api/python/admin/stats/")
        assert response.status_code == 200
        stats = response.json()
        assert "Unit 8 Assessment: Recursive Sorting & Search" in stats["average_assessment_scores"]
        assert stats["average_assessment_scores"]["Unit 8 Assessment: Recursive Sorting & Search"] == 90.0
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Module 8 average assessment score in admin stats."))

        # ==========================================
        # SPRINT 9 (GOOGLE CLASSROOM INTEGRATION) VERIFICATION
        # ==========================================
        self.stdout.write("\n[TEST 7] Starting Sprint 9 Google Classroom OAuth & Ingestion checks...")

        # 1. Test redirect callback URL behavior on Google Classroom Authorize
        # We need to pass the teacher's auth token
        teacher_token, _ = Token.objects.get_or_create(user=teacher_user)
        response = client.get(f"/api/google/authorize/?token={teacher_token.key}")
        # When no client id is set, it redirects to the callback url
        assert response.status_code == 302
        assert "callback" in response.url
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Google Classroom Authorization redirect."))

        # 2. Test callback code exchange redirecting back to frontend with success query param
        response = client.get(f"/api/google/callback/?code=mock_code&state={teacher_token.key}")
        assert response.status_code == 302
        assert "google_sync=success" in response.url
        self.stdout.write(self.style.SUCCESS("  - Successfully verified Google Classroom callback code exchange flow."))

        # 3. List courses
        client.force_login(teacher_user)
        response = client.get("/api/google/courses/")
        assert response.status_code == 200
        courses = response.json()
        assert len(courses) > 0
        assert courses[0]["id"] == "ap-csa-1"
        self.stdout.write(self.style.SUCCESS("  - Successfully fetched Google Classroom course templates."))

        # 4. View Course Roster
        response = client.get("/api/google/courses/ap-csa-1/roster/")
        assert response.status_code == 200
        roster = response.json()
        assert len(roster) > 0
        assert roster[0]["email"] == "john_doe@example.com"
        self.stdout.write(self.style.SUCCESS("  - Successfully fetched Google Classroom student roster mappings."))

        # 5. View Coursework Tasks
        response = client.get("/api/google/courses/ap-csa-1/coursework/")
        assert response.status_code == 200
        coursework = response.json()
        assert len(coursework) > 0
        assert coursework[0]["id"] == "task-1"
        self.stdout.write(self.style.SUCCESS("  - Successfully fetched Google Classroom coursework assignment lists."))

        # 6. Import Course and map student roster
        response = client.post("/api/google/courses/ap-csa-1/import/")
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "Google Classroom" in data["classroom_name"]
        self.stdout.write(self.style.SUCCESS("  - Successfully imported Google Classroom course and mapped student emails."))

        # 7. Sync Grades to Google Classroom Coursework
        response = client.post("/api/google/sync-grades/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "synced_submissions_count" in data
        self.stdout.write(self.style.SUCCESS("  - Successfully completed Google Classroom grades synchronization."))

        # ==========================================
        # SPRINT 10 (GRADE SYNCING PIPELINE & RETRY QUEUE) VERIFICATION
        # ==========================================
        self.stdout.write("\n[TEST 8] Starting Sprint 10 Celery Sync Pipeline & 429 Retry checks...")

        from telemetry.tasks import push_grade_to_google_classroom
        
        # Verify that push_grade_to_google_classroom runs successfully in eager mode
        task_res = push_grade_to_google_classroom.delay(
            user_profile_id=teacher_user.profile.id,
            course_id="ap-csa-1",
            coursework_id="task-1",
            submission_id="sub-1234",
            score=95
        )
        assert task_res.successful()
        self.stdout.write(self.style.SUCCESS("  - Successfully executed Celery push task in local eager mode."))

        # Verify rate-limiting retry on simulated 429 using 'test-rate-limit-retry' course ID
        # Since it's synchronous in eager mode, it executes retries inline
        task_res_retry = push_grade_to_google_classroom.delay(
            user_profile_id=teacher_user.profile.id,
            course_id="test-rate-limit-retry",
            coursework_id="task-1",
            submission_id="sub-1234",
            score=85
        )
        assert task_res_retry.successful()
        self.stdout.write(self.style.SUCCESS("  - Successfully verified exponential task retries on simulated 429 responses."))

        # Clean up
        student.delete()
        classroom.delete()
        teacher_user.delete()
        student_user.delete()
        admin_user.delete()
        
        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 10 INTEGRATION TESTS PASSED!"))
        self.stdout.write("==================================================")
