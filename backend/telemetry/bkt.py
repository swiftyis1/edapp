import threading
from .models import Student, StudentBKTState, TelemetryEvent

def get_or_create_bkt_state(student):
    state, created = StudentBKTState.objects.get_or_create(student=student)
    return state

def run_student_bkt_updates(student_id, session_id):
    """
    Computes BKT probability updates on student's telemetry events inside a session.
    """
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return

    state = get_or_create_bkt_state(student)
    
    # Process events in order
    events = TelemetryEvent.objects.filter(student=student, session_id=session_id).order_by('timestamp')
    
    for ev in events:
        if ev.event_type == 'pair_base':
            # Skill: Transcription
            is_correct = ev.payload.get('is_correct', True)
            
            p_know = state.transcription_p_know
            p_guess = state.transcription_p_guess
            p_slip = state.transcription_p_slip
            p_transit = state.transcription_p_transit
            
            # Bayes update
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                # Adaptive parameter tuning
                state.transcription_p_slip = max(0.02, state.transcription_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                # Adaptive parameter tuning
                state.transcription_p_slip = min(0.30, state.transcription_p_slip + 0.01)
                
            state.transcription_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))
            
        elif ev.event_type == 'codon_match_attempt':
            # Skill: Translation
            is_correct = ev.payload.get('is_correct', True)
            
            p_know = state.translation_p_know
            p_guess = state.translation_p_guess
            p_slip = state.translation_p_slip
            p_transit = state.translation_p_transit
            
            # Bayes update
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.translation_p_slip = max(0.02, state.translation_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.translation_p_slip = min(0.30, state.translation_p_slip + 0.01)
                
            state.translation_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    state.save()

def trigger_bkt_update_async(student_id, session_id):
    """
    Spawns a thread to process BKT updates in the background.
    """
    thread = threading.Thread(target=run_student_bkt_updates, args=(student_id, session_id))
    thread.start()
