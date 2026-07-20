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
        ev_type = ev.event_type
        if ev.construct_tag == 'OAS.B.LS1.2':
            ev_type = 'hierarchy_check'
        elif ev.construct_tag == 'OAS.B.LS1.3':
            ev_type = 'homeostasis_check'
        elif ev.construct_tag == 'OAS.B.LS1.4':
            ev_type = 'division_check'
        elif ev.construct_tag == 'OAS.B.LS1.5':
            ev_type = 'photosynthesis_check'
        elif ev.construct_tag == 'OAS.B.LS1.6':
            ev_type = 'synthesis_check'
        elif ev.construct_tag == 'OAS.B.LS1.7':
            ev_type = 'respiration_check'
        elif ev.construct_tag == 'OAS.B.LS2.1':
            ev_type = 'capacity_check'
        elif ev.construct_tag == 'OAS.B.LS2.2':
            ev_type = 'biodiversity_check'
        elif ev_type in ['dok1_activity_check', 'dok2_activity_check', 'dok3_activity_check', 'dok4_activity_check']:
            activity_id = ev.payload.get('activity_id', '')
            if activity_id in [
                'bio_dok1_act1', 'bio_dok1_act3', 'bio_dok1_act4', 'bio_dok1_act3_workspace', 'bio_dok1_act4_workspace',
                'bio_dok2_act1', 'bio_dok2_act1_workspace',
                'bio_dok3_act2', 'bio_dok3_act2_workspace', 'bio_dok3_act4', 'bio_dok3_act4_workspace', 'bio_dok3_act5', 'bio_dok3_act5_workspace',
                'bio_dok4_act1', 'bio_dok4_act1_workspace', 'bio_dok4_act2', 'bio_dok4_act2_workspace'
            ]:
                ev_type = 'pair_base'
            elif activity_id in [
                'bio_dok1_act2', 'bio_dok1_act5', 'bio_dok1_act2_workspace', 'bio_dok1_act5_workspace',
                'bio_dok2_act2', 'bio_dok2_act2_workspace', 'bio_dok2_act5', 'bio_dok2_act5_workspace',
                'bio_dok3_act3', 'bio_dok3_act3_workspace',
                'bio_dok4_act4', 'bio_dok4_act4_workspace', 'bio_dok4_act5', 'bio_dok4_act5_workspace'
            ]:
                ev_type = 'codon_match_attempt'
            elif activity_id in [
                'bio_dok2_act3', 'bio_dok2_act3_workspace', 'bio_dok2_act4', 'bio_dok2_act4_workspace',
                'bio_dok3_act1', 'bio_dok3_act1_workspace',
                'bio_dok4_act3', 'bio_dok4_act3_workspace'
            ]:
                ev_type = 'mutation_check'

        if ev_type == 'pair_base':
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
            
        elif ev_type == 'codon_match_attempt':
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

        elif ev_type == 'mutation_check':
            # Skill: Mutation Analysis
            is_correct = ev.payload.get('is_correct', True)
            
            p_know = state.mutation_p_know
            p_guess = state.mutation_p_guess
            p_slip = state.mutation_p_slip
            p_transit = state.mutation_p_transit
            
            # Bayes update
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.mutation_p_slip = max(0.02, state.mutation_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.mutation_p_slip = min(0.30, state.mutation_p_slip + 0.01)
                
            state.mutation_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'hierarchy_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.hierarchy_p_know
            p_guess = state.hierarchy_p_guess
            p_slip = state.hierarchy_p_slip
            p_transit = state.hierarchy_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.hierarchy_p_slip = max(0.02, state.hierarchy_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.hierarchy_p_slip = min(0.30, state.hierarchy_p_slip + 0.01)
                
            state.hierarchy_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'homeostasis_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.homeostasis_p_know
            p_guess = state.homeostasis_p_guess
            p_slip = state.homeostasis_p_slip
            p_transit = state.homeostasis_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.homeostasis_p_slip = max(0.02, state.homeostasis_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.homeostasis_p_slip = min(0.30, state.homeostasis_p_slip + 0.01)
                
            state.homeostasis_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'division_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.division_p_know
            p_guess = state.division_p_guess
            p_slip = state.division_p_slip
            p_transit = state.division_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.division_p_slip = max(0.02, state.division_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.division_p_slip = min(0.30, state.division_p_slip + 0.01)
                
            state.division_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'photosynthesis_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.photosynthesis_p_know
            p_guess = state.photosynthesis_p_guess
            p_slip = state.photosynthesis_p_slip
            p_transit = state.photosynthesis_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.photosynthesis_p_slip = max(0.02, state.photosynthesis_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.photosynthesis_p_slip = min(0.30, state.photosynthesis_p_slip + 0.01)
                
            state.photosynthesis_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'synthesis_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.synthesis_p_know
            p_guess = state.synthesis_p_guess
            p_slip = state.synthesis_p_slip
            p_transit = state.synthesis_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.synthesis_p_slip = max(0.02, state.synthesis_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.synthesis_p_slip = min(0.30, state.synthesis_p_slip + 0.01)
                
            state.synthesis_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'respiration_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.respiration_p_know
            p_guess = state.respiration_p_guess
            p_slip = state.respiration_p_slip
            p_transit = state.respiration_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.respiration_p_slip = max(0.02, state.respiration_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.respiration_p_slip = min(0.30, state.respiration_p_slip + 0.01)
                
            state.respiration_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'capacity_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.capacity_p_know
            p_guess = state.capacity_p_guess
            p_slip = state.capacity_p_slip
            p_transit = state.capacity_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.capacity_p_slip = max(0.02, state.capacity_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.capacity_p_slip = min(0.30, state.capacity_p_slip + 0.01)
                
            state.capacity_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

        elif ev_type == 'biodiversity_check':
            is_correct = ev.payload.get('is_correct', True)
            p_know = state.biodiversity_p_know
            p_guess = state.biodiversity_p_guess
            p_slip = state.biodiversity_p_slip
            p_transit = state.biodiversity_p_transit
            
            if is_correct:
                p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
                state.biodiversity_p_slip = max(0.02, state.biodiversity_p_slip - 0.005)
            else:
                p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
                state.biodiversity_p_slip = min(0.30, state.biodiversity_p_slip + 0.01)
                
            state.biodiversity_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    state.save()

def trigger_bkt_update_async(student_id, session_id):
    """
    Spawns a thread to process BKT updates in the background.
    """
    thread = threading.Thread(target=run_student_bkt_updates, args=(student_id, session_id))
    thread.start()
