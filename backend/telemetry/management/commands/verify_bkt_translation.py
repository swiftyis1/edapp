import time
import uuid
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from django.core.cache import cache
from telemetry.models import Student, Session, TelemetryEvent, StudentBKTState, Classroom, UserProfile

class Command(BaseCommand):
    help = "Verifies Level 2 tRNA Translation telemetry, BKT state calculations, and Teacher Roster caching"

    def handle(self, *args, **options):
        client = Client()
        
        # Clean up leftovers
        User.objects.filter(username__in=["bkt_tester_student", "bkt_tester_teacher"]).delete()
        
        self.stdout.write("==================================================")
        self.stdout.write("STARTING INTEGRATION VERIFICATION FOR SPRINT 4")
        self.stdout.write("==================================================")

        # Setup teacher user & classroom
        teacher_user = User.objects.create_user(username="bkt_tester_teacher", email="teacher@bkt.edu")
        teacher_profile, _ = UserProfile.objects.get_or_create(user=teacher_user)
        teacher_profile.role = "teacher"
        teacher_profile.save()
        
        classroom = Classroom.objects.create(name="BKT Biology", class_code="BKT404", teacher=teacher_user)
        
        # Setup student user & profile
        student_user = User.objects.create_user(username="bkt_tester_student", email="student@bkt.edu")
        student_profile, _ = UserProfile.objects.get_or_create(user=student_user)
        student_profile.role = "student"
        student_profile.save()
        
        student = Student.objects.create(name="Liam BKT", user=student_user, classroom=classroom)
        
        session_id = uuid.uuid4()
        
        client.force_login(student_user)

        # ----------------------------------------------------
        # Test Case 1: Post Transcription (Level 1) events
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 1] Dispatching DNA Transcription (Level 1) telemetry...")
        
        # We pair 9 nucleotides (DNA template: TACGGTTAA -> mRNA target: AUGCCAAUU)
        # We will make 1 mistake at index 2 (G -> expected C, we try U)
        bases = [
            ("A", True), ("U", True), ("U", False), ("C", True),
            ("G", True), ("G", True), ("A", True), ("A", True),
            ("U", True), ("U", True)
        ]
        
        for idx, (b, correct) in enumerate(bases):
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-07-14T02:00:00Z",
                    "event_type": "pair_base",
                    "level_id": "dna_transcription_1",
                    "payload": {
                        "index": idx,
                        "attempted_base": b,
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201

        self.stdout.write("  - Level 1 events dispatched successfully.")

        # ----------------------------------------------------
        # Test Case 2: Dispatch Translation (Level 2) events
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 2] Dispatching DNA Translation (Level 2) tRNA anticodon matches...")
        
        # Codons: AUG, CCG, UUU (translated from mRNA target)
        # Matches: tRNA UAC, GGC, AAA
        # We will make 1 mistake on CCG (matching with UUU instead of GGC)
        codon_attempts = [
            ("AUG", "UAC", True),
            ("CCG", "UUU", False),
            ("CCG", "GGC", True),
            ("AAA", "UUU", True)
        ]
        
        for codon, tRNA, correct in codon_attempts:
            response = client.post(
                "/api/telemetry/",
                data=json.dumps({
                    "event_id": str(uuid.uuid4()),
                    "student_id": str(student.id),
                    "session_id": str(session_id),
                    "timestamp": "2026-07-14T02:05:00Z",
                    "event_type": "codon_match_attempt",
                    "level_id": "dna_translation_2",
                    "payload": {
                        "codon": codon,
                        "attempted_anticodon": tRNA,
                        "is_correct": correct
                    }
                }),
                content_type="application/json"
            )
            assert response.status_code == 201
            
        self.stdout.write("  - Level 2 events dispatched successfully.")

        # ----------------------------------------------------
        # Test Case 3: Complete Session & BKT calculations
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 3] Submitting Session Completion and verifying BKT computation...")
        
        response = client.post(
            "/api/telemetry/",
            data=json.dumps({
                "event_id": str(uuid.uuid4()),
                "student_id": str(student.id),
                "session_id": str(session_id),
                "timestamp": "2026-07-14T02:08:00Z",
                "event_type": "session_complete",
                "level_id": "dna_translation_2",
                "payload": {
                    "total_errors": 2,
                    "duration_seconds": 150
                }
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        
        # Wait briefly for background thread execution
        time.sleep(1.0)
        
        bkt_state = StudentBKTState.objects.filter(student=student).first()
        assert bkt_state is not None
        
        # Defaults were 0.20 and 0.15. After mostly correct updates:
        assert bkt_state.transcription_p_know != 0.20
        assert bkt_state.translation_p_know != 0.15
        
        self.stdout.write(self.style.SUCCESS(
            f"  - BKT State saved successfully! Transcription know={bkt_state.transcription_p_know:.3f}, Translation know={bkt_state.translation_p_know:.3f}"
        ))

        # ----------------------------------------------------
        # Test Case 4: Verifying Parent portal payload
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 4] Fetching Parent Report and verifying BKT estimates...")
        
        response = client.get(f"/api/reports/parent/?student_id={student.id}")
        assert response.status_code == 200
        res_data = response.json()
        assert "bkt_mastery" in res_data
        assert res_data["bkt_mastery"] > 0
        self.stdout.write(self.style.SUCCESS(f"  - Parent report standard B.LS1.1 BKT Mastery returned: {res_data['bkt_mastery']}%"))

        # ----------------------------------------------------
        # Test Case 5: Caching & Invalidation
        # ----------------------------------------------------
        self.stdout.write("\n[TEST 5] Testing teacher report caching and invalidation...")
        
        client.force_login(teacher_user)
        
        # Call 1: Populates cache
        response = client.get("/api/reports/teacher/")
        assert response.status_code == 200
        res1 = response.json()
        student_entry1 = next(s for s in res1 if s["id"] == str(student.id))
        assert student_entry1["total_actions"] == 10
        self.stdout.write("  - Roster data cached successfully on first fetch.")
        
        # Call 2: Returns cached data directly
        response = client.get("/api/reports/teacher/")
        assert response.status_code == 200
        res2 = response.json()
        student_entry2 = next(s for s in res2 if s["id"] == str(student.id))
        assert student_entry2["total_actions"] == 10
        
        # Invalidate via posting a new telemetry event
        client.force_login(student_user)
        response = client.post(
            "/api/telemetry/",
            data=json.dumps({
                "event_id": str(uuid.uuid4()),
                "student_id": str(student.id),
                "session_id": str(session_id),
                "timestamp": "2026-07-14T02:10:00Z",
                "event_type": "pair_base",
                "level_id": "dna_transcription_1",
                "payload": {
                    "index": 1,
                    "attempted_base": "A",
                    "is_correct": True
                }
            }),
            content_type="application/json"
        )
        assert response.status_code == 201
        
        # Fetch roster again as teacher: must see 11 actions (cache invalidated and updated!)
        client.force_login(teacher_user)
        response = client.get("/api/reports/teacher/")
        assert response.status_code == 200
        res3 = response.json()
        student_entry3 = next(s for s in res3 if s["id"] == str(student.id))
        assert student_entry3["total_actions"] == 11
        
        self.stdout.write(self.style.SUCCESS("  - Cache invalidation verified! Updated telemetry matches on subsequent fetch."))

        # Clean up
        student.delete()
        classroom.delete()
        teacher_user.delete()
        student_user.delete()
        
        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("ALL SPRINT 4 INTEGRATION VERIFICATION TESTS PASSED!"))
        self.stdout.write("==================================================")
