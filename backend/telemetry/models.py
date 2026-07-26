import uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'District Admin'),
        ('school_admin', 'School Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    parent_student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='parents_legacy')
    parent_students = models.ManyToManyField('Student', blank=True, related_name='parents')
    campus = models.ForeignKey('Campus', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    # B2C Premium Subscription fields
    is_premium = models.BooleanField(default=False)
    premium_slots = models.IntegerField(default=1)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    subscription_status = models.CharField(max_length=50, default='inactive')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Campus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    students_active = models.IntegerField(default=0)
    seat_limit = models.IntegerField(default=0)
    
    # B2B License Subscription fields
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    subscription_status = models.CharField(max_length=50, default='inactive')

    def __str__(self):
        return self.name

class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
    class_code = models.CharField(max_length=6, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    lti_context_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.class_code})"

class TeacherInvite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='invites')
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite for {self.email} to {self.campus.name}"

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile')
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    lti_user_id = models.CharField(max_length=255, blank=True, null=True)

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

    class Meta:
        indexes = [
            models.Index(fields=['student', 'event_type']),
            models.Index(fields=['session', 'event_type']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['construct_tag']),
            models.Index(fields=['student', 'construct_tag', 'timestamp']),
        ]

class ScoringConfig(models.Model):
    key = models.CharField(max_length=50, unique=True, default='default')
    a = models.FloatField(default=23.08)
    b = models.FloatField(default=303.00)
    advanced_cutoff = models.IntegerField(default=327)
    proficient_cutoff = models.IntegerField(default=300)
    basic_cutoff = models.IntegerField(default=278)

    def __str__(self):
        return f"ScoringConfig({self.key}: A={self.a}, B={self.b})"


class StudentBKTState(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='bkt_state')
    
    # Skill: Transcription (base pairing)
    transcription_p_know = models.FloatField(default=0.20)
    transcription_p_guess = models.FloatField(default=0.25)
    transcription_p_slip = models.FloatField(default=0.10)
    transcription_p_transit = models.FloatField(default=0.15)
    
    # Skill: Translation (codon matching)
    translation_p_know = models.FloatField(default=0.15)
    translation_p_guess = models.FloatField(default=0.20)
    translation_p_slip = models.FloatField(default=0.12)
    translation_p_transit = models.FloatField(default=0.18)
    
    # Skill: Chemical Bonding (OAS B.PS1.1)
    bonding_p_know = models.FloatField(default=0.15)
    bonding_p_guess = models.FloatField(default=0.20)
    bonding_p_slip = models.FloatField(default=0.10)
    bonding_p_transit = models.FloatField(default=0.15)
    
    # Skill: Mutation Analysis (OAS B.LS1.1)
    mutation_p_know = models.FloatField(default=0.10)
    mutation_p_guess = models.FloatField(default=0.25)
    mutation_p_slip = models.FloatField(default=0.10)
    mutation_p_transit = models.FloatField(default=0.15)
    
    # Skill: Multicellular Hierarchical Systems (OAS B.LS1.2)
    hierarchy_p_know = models.FloatField(default=0.15)
    hierarchy_p_guess = models.FloatField(default=0.20)
    hierarchy_p_slip = models.FloatField(default=0.10)
    hierarchy_p_transit = models.FloatField(default=0.15)
    
    # Skill: Maintaining Homeostasis (OAS B.LS1.3)
    homeostasis_p_know = models.FloatField(default=0.15)
    homeostasis_p_guess = models.FloatField(default=0.20)
    homeostasis_p_slip = models.FloatField(default=0.10)
    homeostasis_p_transit = models.FloatField(default=0.15)
    
    # Skill: Cellular Division & Differentiation (OAS B.LS1.4)
    division_p_know = models.FloatField(default=0.15)
    division_p_guess = models.FloatField(default=0.20)
    division_p_slip = models.FloatField(default=0.10)
    division_p_transit = models.FloatField(default=0.15)
    
    # Skill: Photosynthesis Energy Transformation (OAS B.LS1.5)
    photosynthesis_p_know = models.FloatField(default=0.15)
    photosynthesis_p_guess = models.FloatField(default=0.20)
    photosynthesis_p_slip = models.FloatField(default=0.10)
    photosynthesis_p_transit = models.FloatField(default=0.15)
    
    # Skill: Macromolecule Synthesis (OAS B.LS1.6)
    synthesis_p_know = models.FloatField(default=0.15)
    synthesis_p_guess = models.FloatField(default=0.20)
    synthesis_p_slip = models.FloatField(default=0.10)
    synthesis_p_transit = models.FloatField(default=0.15)
    
    # Skill: Cellular Respiration Energy Transfer (OAS B.LS1.7)
    respiration_p_know = models.FloatField(default=0.15)
    respiration_p_guess = models.FloatField(default=0.20)
    respiration_p_slip = models.FloatField(default=0.10)
    respiration_p_transit = models.FloatField(default=0.15)
    
    # Skill: Carrying Capacity Factors (OAS B.LS2.1)
    capacity_p_know = models.FloatField(default=0.15)
    capacity_p_guess = models.FloatField(default=0.20)
    capacity_p_slip = models.FloatField(default=0.10)
    capacity_p_transit = models.FloatField(default=0.15)
    
    # Skill: Biodiversity Factors (OAS B.LS2.2)
    biodiversity_p_know = models.FloatField(default=0.15)
    biodiversity_p_guess = models.FloatField(default=0.20)
    biodiversity_p_slip = models.FloatField(default=0.10)
    biodiversity_p_transit = models.FloatField(default=0.15)
    
    # Skill: Cycling of Matter (OAS B.LS2.3)
    matter_p_know = models.FloatField(default=0.15)
    matter_p_guess = models.FloatField(default=0.20)
    matter_p_slip = models.FloatField(default=0.10)
    matter_p_transit = models.FloatField(default=0.15)
    
    # Skill: Ecosystem Energy Flow (OAS B.LS2.4)
    energy_p_know = models.FloatField(default=0.15)
    energy_p_guess = models.FloatField(default=0.20)
    energy_p_slip = models.FloatField(default=0.10)
    energy_p_transit = models.FloatField(default=0.15)
    
    # Skill: Carbon Cycling Spheres (OAS B.LS2.5)
    carbon_p_know = models.FloatField(default=0.15)
    carbon_p_guess = models.FloatField(default=0.20)
    carbon_p_slip = models.FloatField(default=0.10)
    carbon_p_transit = models.FloatField(default=0.15)
    
    # Skill: Ecosystem Stability Evaluation (OAS B.LS2.6)
    stability_p_know = models.FloatField(default=0.15)
    stability_p_guess = models.FloatField(default=0.20)
    stability_p_slip = models.FloatField(default=0.10)
    stability_p_transit = models.FloatField(default=0.15)

    # Skill: Group Behavior Evidence (OAS B.LS2.8)
    behavior_p_know = models.FloatField(default=0.15)
    behavior_p_guess = models.FloatField(default=0.20)
    behavior_p_slip = models.FloatField(default=0.10)
    behavior_p_transit = models.FloatField(default=0.15)

    # Skill: Genetics Inheritable Traits (OAS B.LS3.1)
    inheritance_p_know = models.FloatField(default=0.15)
    inheritance_p_guess = models.FloatField(default=0.20)
    inheritance_p_slip = models.FloatField(default=0.10)
    inheritance_p_transit = models.FloatField(default=0.15)

    # Skill: Genetic Variation Viable Errors (OAS B.LS3.2)
    variation_p_know = models.FloatField(default=0.15)
    variation_p_guess = models.FloatField(default=0.20)
    variation_p_slip = models.FloatField(default=0.10)
    variation_p_transit = models.FloatField(default=0.15)

    # Skill: Statistics of Trait Distribution (OAS B.LS3.3)
    statistics_p_know = models.FloatField(default=0.15)
    statistics_p_guess = models.FloatField(default=0.20)
    statistics_p_slip = models.FloatField(default=0.10)
    statistics_p_transit = models.FloatField(default=0.15)
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BKT State for {self.student.name}"


class StudentBKTHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bkt_history')
    timestamp = models.DateTimeField(auto_now_add=True)
    construct_tag = models.CharField(max_length=100) # 'OAS.B.LS1.1' or 'OAS.B.PS1.1'
    p_know = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.construct_tag}: {self.p_know:.3f} ({self.timestamp})"


class InvoiceReceipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='invoices')
    stripe_invoice_id = models.CharField(max_length=200)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    seats_purchased = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_pdf_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.stripe_invoice_id} - {self.campus.name} (${self.amount_paid})"


class LTIPlatform(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100) # e.g. "Canvas LMS"
    issuer = models.CharField(max_length=255, unique=True) # e.g. "https://canvas.instructure.com"
    client_id = models.CharField(max_length=255)
    auth_login_url = models.URLField()
    auth_token_url = models.URLField()
    key_set_url = models.URLField()

    def __str__(self):
        return self.name


class LTIGradeSyncLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lti_grade_logs')
    level_id = models.CharField(max_length=100)
    score = models.IntegerField()
    status = models.CharField(max_length=20, default='Success') # 'Success' or 'Failed'
    error_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.level_id}: {self.score} ({self.status})"


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action_name = models.CharField(max_length=100) # e.g. "adjust_quota", "import_data", "schedule_report", "purge_data"
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_name} by {self.action_by.username if self.action_by else 'System'} ({self.timestamp})"


class ReportSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    frequency = models.CharField(max_length=20, default='weekly') # 'weekly', 'monthly'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.email} ({self.frequency})"
