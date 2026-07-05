import uuid
from django.db import models

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.id} for {self.student.name}"

class TelemetryEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_event_id = models.CharField(max_length=100, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='telemetry_events')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='telemetry_events')
    timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=50) # e.g. 'level_start', 'pair_base', 'reset', 'session_complete'
    level_id = models.CharField(max_length=50)
    construct_tag = models.CharField(max_length=100, null=True, blank=True)
    payload = models.JSONField()

    def __str__(self):
        return f"{self.event_type} - {self.student.name} ({self.timestamp})"
