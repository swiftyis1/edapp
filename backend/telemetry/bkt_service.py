from .models import StudentBKTState

def update_bkt_state_for_event(student, event_type, is_correct):
    """
    Recursively updates the student's BKT state in real-time when an event is received.
    Supports:
      - 'pair_base': Transcription (OAS B.LS1.1)
      - 'codon_match_attempt': Translation (OAS B.LS1.1)
      - 'octet_rule_check': Chemical Bonding (OAS B.PS1.1)
      - 'mutation_check': Mutation Analysis (OAS B.LS1.1)
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

    elif event_type == 'mutation_check':
        p_know = state.mutation_p_know
        p_guess = state.mutation_p_guess
        p_slip = state.mutation_p_slip
        p_transit = state.mutation_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.mutation_p_slip = max(0.02, state.mutation_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.mutation_p_slip = min(0.30, state.mutation_p_slip + 0.01)
            
        state.mutation_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'hierarchy_check':
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

    elif event_type == 'homeostasis_check':
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

    elif event_type == 'division_check':
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

    elif event_type == 'photosynthesis_check':
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

    elif event_type == 'synthesis_check':
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

    elif event_type == 'respiration_check':
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

    elif event_type == 'capacity_check':
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

    elif event_type == 'biodiversity_check':
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

    elif event_type == 'matter_check':
        p_know = state.matter_p_know
        p_guess = state.matter_p_guess
        p_slip = state.matter_p_slip
        p_transit = state.matter_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.matter_p_slip = max(0.02, state.matter_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.matter_p_slip = min(0.30, state.matter_p_slip + 0.01)
            
        state.matter_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'energy_check':
        p_know = state.energy_p_know
        p_guess = state.energy_p_guess
        p_slip = state.energy_p_slip
        p_transit = state.energy_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.energy_p_slip = max(0.02, state.energy_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.energy_p_slip = min(0.30, state.energy_p_slip + 0.01)
            
        state.energy_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'carbon_check':
        p_know = state.carbon_p_know
        p_guess = state.carbon_p_guess
        p_slip = state.carbon_p_slip
        p_transit = state.carbon_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.carbon_p_slip = max(0.02, state.carbon_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.carbon_p_slip = min(0.30, state.carbon_p_slip + 0.01)
            
        state.carbon_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'stability_check':
        p_know = state.stability_p_know
        p_guess = state.stability_p_guess
        p_slip = state.stability_p_slip
        p_transit = state.stability_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.stability_p_slip = max(0.02, state.stability_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.stability_p_slip = min(0.30, state.stability_p_slip + 0.01)
            
        state.stability_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'behavior_check':
        p_know = state.behavior_p_know
        p_guess = state.behavior_p_guess
        p_slip = state.behavior_p_slip
        p_transit = state.behavior_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.behavior_p_slip = max(0.02, state.behavior_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.behavior_p_slip = min(0.30, state.behavior_p_slip + 0.01)
            
        state.behavior_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'inheritance_check':
        p_know = state.inheritance_p_know
        p_guess = state.inheritance_p_guess
        p_slip = state.inheritance_p_slip
        p_transit = state.inheritance_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.inheritance_p_slip = max(0.02, state.inheritance_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.inheritance_p_slip = min(0.30, state.inheritance_p_slip + 0.01)
            
        state.inheritance_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'variation_check':
        p_know = state.variation_p_know
        p_guess = state.variation_p_guess
        p_slip = state.variation_p_slip
        p_transit = state.variation_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.variation_p_slip = max(0.02, state.variation_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.variation_p_slip = min(0.30, state.variation_p_slip + 0.01)
            
        state.variation_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    elif event_type == 'statistics_check':
        p_know = state.statistics_p_know
        p_guess = state.statistics_p_guess
        p_slip = state.statistics_p_slip
        p_transit = state.statistics_p_transit
        
        if is_correct:
            p_know_given_obs = (p_know * (1.0 - p_slip)) / ((p_know * (1.0 - p_slip)) + ((1.0 - p_know) * p_guess))
            state.statistics_p_slip = max(0.02, state.statistics_p_slip - 0.005)
        else:
            p_know_given_obs = (p_know * p_slip) / ((p_know * p_slip) + ((1.0 - p_know) * (1.0 - p_guess)))
            state.statistics_p_slip = min(0.30, state.statistics_p_slip + 0.01)
            
        state.statistics_p_know = min(0.999, max(0.001, p_know_given_obs + (1.0 - p_know_given_obs) * p_transit))

    state.save()

    # Append to BKT History for temporal growth charting
    from .models import StudentBKTHistory
    if event_type in ['pair_base', 'codon_match_attempt', 'mutation_check']:
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.1',
            p_know=(state.transcription_p_know + state.translation_p_know + state.mutation_p_know) / 3
        )
    elif event_type == 'octet_rule_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.PS1.1',
            p_know=state.bonding_p_know
        )
    elif event_type == 'hierarchy_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.2',
            p_know=state.hierarchy_p_know
        )
    elif event_type == 'homeostasis_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.3',
            p_know=state.homeostasis_p_know
        )
    elif event_type == 'division_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.4',
            p_know=state.division_p_know
        )
    elif event_type == 'photosynthesis_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.5',
            p_know=state.photosynthesis_p_know
        )
    elif event_type == 'synthesis_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.6',
            p_know=state.synthesis_p_know
        )
    elif event_type == 'respiration_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS1.7',
            p_know=state.respiration_p_know
        )
    elif event_type == 'capacity_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS2.1',
            p_know=state.capacity_p_know
        )
    elif event_type == 'biodiversity_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS2.2',
            p_know=state.biodiversity_p_know
        )
    elif event_type == 'matter_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS2.3',
            p_know=state.matter_p_know
        )
    elif event_type == 'energy_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS2.4',
            p_know=state.energy_p_know
        )
    elif event_type == 'carbon_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS2.5',
            p_know=state.carbon_p_know
        )
    elif event_type == 'stability_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS2.6',
            p_know=state.stability_p_know
        )
    elif event_type == 'behavior_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS2.8',
            p_know=state.behavior_p_know
        )
    elif event_type == 'inheritance_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS3.1',
            p_know=state.inheritance_p_know
        )
    elif event_type == 'variation_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS3.2',
            p_know=state.variation_p_know
        )
    elif event_type == 'statistics_check':
        StudentBKTHistory.objects.create(
            student=student,
            construct_tag='OAS.B.LS3.3',
            p_know=state.statistics_p_know
        )

    return state
