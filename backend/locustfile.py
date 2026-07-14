import uuid
import random
from locust import HttpUser, task, between

class StudentTelemetryUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Initialize a mock student and session
        self.student_id = str(uuid.uuid4())
        self.session_id = str(uuid.uuid4())
        self.level_progress = 0

    @task(3)
    def post_base_pairing_event(self):
        # Simulate pairing a base
        self.client.post("/api/telemetry/", json={
            "event_id": str(uuid.uuid4()),
            "student_id": self.student_id,
            "session_id": self.session_id,
            "timestamp": "2026-07-14T04:00:00Z",
            "event_type": "pair_base",
            "level_id": f"dna_transcription_level_{random.choice([1, 2, 3])}",
            "construct_tag": "OAS.B.LS1.1",
            "payload": {
                "index": self.level_progress,
                "template_base": "T",
                "attempted_base": "A",
                "is_correct": random.choice([True, True, True, False]) # 75% correct
            }
        })
        self.level_progress += 1

    @task(1)
    def post_codon_match_event(self):
        # Simulate codon matching
        self.client.post("/api/telemetry/", json={
            "event_id": str(uuid.uuid4()),
            "student_id": self.student_id,
            "session_id": self.session_id,
            "timestamp": "2026-07-14T04:00:00Z",
            "event_type": "codon_match_attempt",
            "level_id": "dna_translation_level_2",
            "construct_tag": "OAS.B.LS1.1",
            "payload": {
                "codon_index": random.choice([0, 1, 2]),
                "mRNA_codon": "AUG",
                "attempted_anticodon": "UAC",
                "is_correct": random.choice([True, True, False])
            }
        })

    @task(1)
    def post_octet_rule_event(self):
        # Simulate chemical bonding checks
        self.client.post("/api/telemetry/", json={
            "event_id": str(uuid.uuid4()),
            "student_id": self.student_id,
            "session_id": self.session_id,
            "timestamp": "2026-07-14T04:00:00Z",
            "event_type": "octet_rule_check",
            "level_id": "chemical_bonding_level_3",
            "construct_tag": "OAS.B.PS1.1",
            "payload": {
                "element": "Oxygen",
                "electrons": 8,
                "is_correct": random.choice([True, False])
            }
        })
