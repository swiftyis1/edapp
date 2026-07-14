from .models import StudentBKTState

def update_bkt_state_for_event(student, event_type, is_correct):
    """
    Recursively updates the student's BKT state in real-time when an event is received.
    Supports:
      - 'pair_base': Transcription (OAS B.LS1.1)
      - 'codon_match_attempt': Translation (OAS B.LS1.1)
      - 'octet_rule_check': Chemical Bonding (OAS B.PS1.1)
    """
    state, created = StudentBKTState.objects.get_or_create(student=student)
    
    if event_type == 'pair_base':
        p_know = state.transcription_p_know
        p_guess = state.transcription_p_guess
        p_slip = state.transcription_p_slip
        p_transit = state.transcription_p_transit
        
        # Bayes calculation
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            # Adaptive slip adjustment
            state.transcription_p_slip = max(0.02, state.transcription_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.transcription_p_slip = min(0.30, state.transcription_p_slip + 0.01)
            
        state.transcription_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))
        
    elif event_type == 'codon_match_attempt':
        p_know = state.translation_p_know
        p_guess = state.translation_p_guess
        p_slip = state.translation_p_slip
        p_transit = state.translation_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.translation_p_slip = max(0.02, state.translation_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.translation_p_slip = min(0.30, state.translation_p_slip + 0.01)
            
        state.translation_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))
        
    elif event_type == 'octet_rule_check':
        p_know = state.bonding_p_know
        p_guess = state.bonding_p_guess
        p_slip = state.bonding_p_slip
        p_transit = state.bonding_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.bonding_p_slip = max(0.02, state.bonding_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.bonding_p_slip = min(0.30, state.bonding_p_slip + 0.01)
            
        state.bonding_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    state.save()

    # Append to BKT History for temporal growth charting
    from .models import StudentBKTHistory
    if event_type in ['pair_base', 'codon_match_attempt']:
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.1',
            p_know=(state.transcription_p_know + state.translation_p_know) / 2
        )
    elif event_type == 'octet_rule_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.PS1.1',
            p_know=state.bonding_p_know
        )

    return state
