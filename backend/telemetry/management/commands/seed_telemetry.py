import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from telemetry.models import Student, Session, TelemetryEvent

class Command(BaseCommand):
    help = "Seeds the database with mock student profiles and structured gameplay telemetry logs"

    def handle(self, *args, **options):
        self.stdout.write("Purging existing student and telemetry data...")
        TelemetryEvent.objects.all().delete()
        Session.objects.all().delete()
        Student.objects.all().delete()

        # Seed Students with fixed UUIDs to match the implementation plan
        students_data = [
            {"id": "da59114f-c0df-4d51-a957-cc3b23c92b23", "name": "Alex Rivera"},
            {"id": "e2d1d0c5-5a7c-47bc-8367-4f6c122bb33f", "name": "Blake Henderson"},
            {"id": "f04eb32d-2098-4b72-88ec-8f0a1c6a23b1", "name": "Charlie Smith"},
            {"id": "0e46be9f-b7a4-4df8-9226-eb52cbfb27d4", "name": "Daniela Garcia"},
            {"id": "1b131012-38d5-4ad9-bf9f-864a66a1cc92", "name": "Erik Johnson"},
        ]

        students = {}
        for sd in students_data:
            student = Student.objects.create(id=uuid.UUID(sd["id"]), name=sd["name"])
            students[sd["name"]] = student
            self.stdout.write(f"Created student: {student.name} ({student.id})")

        # Define template DNA (9 bases)
        template_dna = ["T", "A", "C", "G", "G", "C", "T", "T", "A"]
        complementary_map = {"T": "A", "A": "U", "C": "G", "G": "C"}

        base_time = timezone.now() - timezone.timedelta(days=1)

        # ----------------------------------------------------
        # 1. Alex Rivera (Advanced): 100% accuracy, fast speed (1.1s avg)
        # ----------------------------------------------------
        alex = students["Alex Rivera"]
        alex_session = Session.objects.create(
            id=uuid.UUID("a1111111-1111-1111-1111-111111111111"),
            student=alex,
            created_at=base_time
        )
        
        # 9 correct pair_base events
        curr_time = base_time
        for idx, dna_base in enumerate(template_dna):
            curr_time += timezone.timedelta(seconds=1.1)
            mrna_base = complementary_map[dna_base]
            TelemetryEvent.objects.create(
                student=alex,
                session=alex_session,
                timestamp=curr_time,
                event_type="pair_base",
                level_id="dna_transcription_1",
                construct_tag="OAS.B.LS1.1",
                payload={
                    "index": idx,
                    "template_base": dna_base,
                    "attempted_base": mrna_base,
                    "is_correct": True,
                    "cumulative_errors": 0
                }
            )

        # Session complete event
        curr_time += timezone.timedelta(seconds=1)
        TelemetryEvent.objects.create(
            student=alex,
            session=alex_session,
            timestamp=curr_time,
            event_type="session_complete",
            level_id="dna_transcription_1",
            construct_tag="OAS.B.LS1.1",
            payload={
                "total_errors": 0,
                "accuracy": 100.0,
                "duration_seconds": 9.9
            }
        )
        alex_session.completed_at = curr_time
        alex_session.save()
        self.stdout.write("Generated telemetry for Alex Rivera (Advanced)")

        # ----------------------------------------------------
        # 2. Blake Henderson (Proficient): 90% accuracy, moderate speed (2.0s avg)
        # ----------------------------------------------------
        blake = students["Blake Henderson"]
        blake_session = Session.objects.create(
            id=uuid.UUID("b2222222-2222-2222-2222-222222222222"),
            student=blake,
            created_at=base_time + timezone.timedelta(hours=1)
        )
        
        curr_time = base_time + timezone.timedelta(hours=1)
        errors = 0
        # Complete transcription with 1 error at index 3 (expected G, tries A, then corrects with G)
        actions = [
            (0, "T", "A", True),
            (1, "A", "U", True),
            (2, "C", "G", True),
            (3, "G", "A", False), # Error 1
            (3, "G", "C", True),
            (4, "G", "C", True),
            (5, "C", "G", True),
            (6, "T", "A", True),
            (7, "T", "A", True),
            (8, "A", "U", True),
        ]
        
        for idx, dna_base, attempted, is_correct in actions:
            curr_time += timezone.timedelta(seconds=2.0)
            if not is_correct:
                errors += 1
            TelemetryEvent.objects.create(
                student=blake,
                session=blake_session,
                timestamp=curr_time,
                event_type="pair_base",
                level_id="dna_transcription_1",
                construct_tag="OAS.B.LS1.1",
                payload={
                    "index": idx,
                    "template_base": dna_base,
                    "attempted_base": attempted,
                    "is_correct": is_correct,
                    "cumulative_errors": errors
                }
            )

        curr_time += timezone.timedelta(seconds=1)
        TelemetryEvent.objects.create(
            student=blake,
            session=blake_session,
            timestamp=curr_time,
            event_type="session_complete",
            level_id="dna_transcription_1",
            construct_tag="OAS.B.LS1.1",
            payload={
                "total_errors": 1,
                "accuracy": 90.0,
                "duration_seconds": 20.0
            }
        )
        blake_session.completed_at = curr_time
        blake_session.save()
        self.stdout.write("Generated telemetry for Blake Henderson (Proficient)")

        # ----------------------------------------------------
        # 3. Charlie Smith (Basic): 75% accuracy (3 errors), slow speed (3.5s avg)
        # ----------------------------------------------------
        charlie = students["Charlie Smith"]
        charlie_session = Session.objects.create(
            id=uuid.UUID("c3333333-3333-3333-3333-333333333333"),
            student=charlie,
            created_at=base_time + timezone.timedelta(hours=2)
        )
        
        curr_time = base_time + timezone.timedelta(hours=2)
        errors = 0
        actions = [
            (0, "T", "A", True),
            (1, "A", "G", False), # Error 1
            (1, "A", "U", True),
            (2, "C", "G", True),
            (3, "G", "C", True),
            (4, "G", "U", False), # Error 2
            (4, "G", "C", True),
            (5, "C", "G", True),
            (6, "T", "A", True),
            (7, "T", "C", False), # Error 3
            (7, "T", "A", True),
            (8, "A", "U", True),
        ]
        
        for idx, dna_base, attempted, is_correct in actions:
            curr_time += timezone.timedelta(seconds=3.5)
            if not is_correct:
                errors += 1
            TelemetryEvent.objects.create(
                student=charlie,
                session=charlie_session,
                timestamp=curr_time,
                event_type="pair_base",
                level_id="dna_transcription_1",
                construct_tag="OAS.B.LS1.1",
                payload={
                    "index": idx,
                    "template_base": dna_base,
                    "attempted_base": attempted,
                    "is_correct": is_correct,
                    "cumulative_errors": errors
                }
            )

        curr_time += timezone.timedelta(seconds=1)
        TelemetryEvent.objects.create(
            student=charlie,
            session=charlie_session,
            timestamp=curr_time,
            event_type="session_complete",
            level_id="dna_transcription_1",
            construct_tag="OAS.B.LS1.1",
            payload={
                "total_errors": 3,
                "accuracy": 75.0,
                "duration_seconds": 42.0
            }
        )
        charlie_session.completed_at = curr_time
        charlie_session.save()
        self.stdout.write("Generated telemetry for Charlie Smith (Basic)")

        # ----------------------------------------------------
        # 4. Daniela Garcia (Below Basic): 60% accuracy (6 errors), slow speed (4.2s avg)
        # ----------------------------------------------------
        daniela = students["Daniela Garcia"]
        daniela_session = Session.objects.create(
            id=uuid.UUID("d4444444-4444-4444-4444-444444444444"),
            student=daniela,
            created_at=base_time + timezone.timedelta(hours=3)
        )
        
        curr_time = base_time + timezone.timedelta(hours=3)
        errors = 0
        actions = [
            (0, "T", "U", False), # Error 1
            (0, "T", "A", True),
            (1, "A", "C", False), # Error 2
            (1, "A", "U", True),
            (2, "C", "A", False), # Error 3
            (2, "C", "G", True),
            (3, "G", "C", True),
            (4, "G", "C", True),
            (5, "C", "U", False), # Error 4
            (5, "C", "G", True),
            (6, "T", "G", False), # Error 5
            (6, "T", "A", True),
            (7, "T", "A", True),
            (8, "A", "G", False), # Error 6
            (8, "A", "U", True),
        ]
        
        for idx, dna_base, attempted, is_correct in actions:
            curr_time += timezone.timedelta(seconds=4.2)
            if not is_correct:
                errors += 1
            TelemetryEvent.objects.create(
                student=daniela,
                session=daniela_session,
                timestamp=curr_time,
                event_type="pair_base",
                level_id="dna_transcription_1",
                construct_tag="OAS.B.LS1.1",
                payload={
                    "index": idx,
                    "template_base": dna_base,
                    "attempted_base": attempted,
                    "is_correct": is_correct,
                    "cumulative_errors": errors
                }
            )

        curr_time += timezone.timedelta(seconds=1)
        TelemetryEvent.objects.create(
            student=daniela,
            session=daniela_session,
            timestamp=curr_time,
            event_type="session_complete",
            level_id="dna_transcription_1",
            construct_tag="OAS.B.LS1.1",
            payload={
                "total_errors": 6,
                "accuracy": 60.0,
                "duration_seconds": 63.0
            }
        )
        daniela_session.completed_at = curr_time
        daniela_session.save()
        self.stdout.write("Generated telemetry for Daniela Garcia (Below Basic)")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
