from .models import ScoringConfig

def calculate_student_theta(accuracy, avg_time_per_base):
    """
    Calculates the student's latent science ability theta.
    Baseline: 85% accuracy and 3.0s speed yields theta = 0.0.
    Accuracy component: (accuracy - 85.0) / 10.0
    Speed component: (3.0 - avg_time_per_base) / 2.0 (if avg_time_per_base > 0)
    """
    acc_component = (accuracy - 85.0) / 10.0
    speed_component = 0.0
    if avg_time_per_base > 0:
        speed_component = (3.0 - avg_time_per_base) / 2.0
    return acc_component + speed_component

def calculate_opi_score(accuracy, avg_time_per_base):
    """
    Computes predicted OPI scaled score (200-399) and performance band
    based on database scoring configuration parameters.
    """
    try:
        config = ScoringConfig.objects.get(key='default')
        a = config.a
        b = config.b
        adv = config.advanced_cutoff
        prof = config.proficient_cutoff
        bas = config.basic_cutoff
    except ScoringConfig.DoesNotExist:
        a = 23.08
        b = 303.00
        adv = 327
        prof = 300
        bas = 278

    theta = calculate_student_theta(accuracy, avg_time_per_base)
    
    # Calculate OPI score: S = A * theta + B
    score = int(round(a * theta + b))
    # Cap between 200 and 399
    score = max(200, min(399, score))

    if score >= adv:
        band = "Advanced"
        status = "On Track"
        color = "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
    elif score >= prof:
        band = "Proficient"
        status = "On Track"
        color = "text-indigo-400 bg-indigo-500/10 border-indigo-500/20"
    elif score >= bas:
        band = "Basic"
        status = "Needs Support"
        color = "text-amber-400 bg-amber-500/10 border-amber-500/20"
    else:
        band = "Below Basic"
        status = "Needs Support"
        color = "text-rose-400 bg-rose-500/10 border-rose-500/20"

    return {
        "opi_score": score,
        "performance_band": band,
        "status_flag": status,
        "color_class": color,
        "theta": theta
    }
