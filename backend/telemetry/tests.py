from django.test import TestCase
from telemetry.bkt import get_or_create_bkt_state, run_student_bkt_updates
from telemetry.models import Student, StudentBKTState, TelemetryEvent, Session
from django.contrib.auth.models import User
from django.utils import timezone

class BktNewStandardsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teststudent", password="password")
        self.student = Student.objects.create(user=self.user, name="Test Student")
        self.session = Session.objects.create(student=self.student)

    def test_init_student_bkt_for_new_standards(self):
        state = get_or_create_bkt_state(self.student)
        self.assertIsNotNone(state)
        self.assertEqual(state.rates_p_know, 0.15)
        self.assertEqual(state.conservation_p_know, 0.15)
        self.assertEqual(state.induction_p_know, 0.15)
        self.assertEqual(state.energyflows_p_know, 0.15)
        self.assertEqual(state.storage_p_know, 0.15)
        self.assertEqual(state.devices_p_know, 0.15)
        self.assertEqual(state.thermal_p_know, 0.15)
        self.assertEqual(state.wavekinematics_p_know, 0.15)
        self.assertEqual(state.radiation_p_know, 0.15)

    def test_run_student_bkt_updates_for_new_standards(self):
        TelemetryEvent.objects.create(
            student=self.student,
            session=self.session,
            event_type="rates_check",
            level_id="1",
            construct_tag="OAS.PS.PS1.5",
            payload={"is_correct": True},
            timestamp=timezone.now()
        )
        
        state_before = get_or_create_bkt_state(self.student)
        self.assertEqual(state_before.rates_p_know, 0.15)

        run_student_bkt_updates(str(self.student.id), str(self.session.id))

        state_after = StudentBKTState.objects.get(student=self.student)
        self.assertGreater(state_after.rates_p_know, 0.15)
