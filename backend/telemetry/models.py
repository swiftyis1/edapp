import uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'District Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    parent_student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='parents')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Campus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    students_active = models.IntegerField(default=0)
    seat_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
    class_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.class_code})"

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile')
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
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

class ScoringConfig(models.Model):
    key = models.CharField(max_length=50, unique=True, default='default')
    a = models.FloatField(default=23.08)
    b = models.FloatField(default=303.00)
    advanced_cutoff = models.IntegerField(default=327)
    proficient_cutoff = models.IntegerField(default=300)
    basic_cutoff = models.IntegerField(default=278)

    def __str__(self):
        return f"ScoringConfig({self.key}: A={self.a}, B={self.b})"
