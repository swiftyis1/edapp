from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .models import Student, Session, TelemetryEvent
import uuid

@api_view(['POST'])
def telemetry_receive(request):
    """
    API endpoint to receive and store client telemetry events.
    Finds or creates Student/Session dynamically.
    """
    data = request.data
    
    event_id = data.get("event_id")
    student_id_str = data.get("student_id")
    session_id_str = data.get("session_id")
    timestamp_str = data.get("timestamp")
    event_type = data.get("event_type")
    level_id = data.get("level_id")
    construct_tag = data.get("construct_tag")
    payload = data.get("payload", {})

    if not student_id_str or not session_id_str or not event_type or not level_id:
        return Response(
            {"status": "error", "message": "Missing required fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Parse UUIDs
    try:
        student_id = uuid.UUID(student_id_str)
        session_id = uuid.UUID(session_id_str)
    except ValueError:
        return Response(
            {"status": "error", "message": "Invalid UUID format"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Parse timestamp
    timestamp = parse_datetime(timestamp_str) if timestamp_str else timezone.now()
    if not timestamp:
        timestamp = timezone.now()

    # Find or create Student
    student, created_student = Student.objects.get_or_create(
        id=student_id,
        defaults={"name": f"Student {str(student_id)[:8]}"}
    )

    # Find or create Session
    session, created_session = Session.objects.get_or_create(
        id=session_id,
        defaults={"student": student, "created_at": timestamp}
    )

    # Create Telemetry Event
    event = TelemetryEvent.objects.create(
        client_event_id=event_id,
        student=student,
        session=session,
        timestamp=timestamp,
        event_type=event_type,
        level_id=level_id,
        construct_tag=construct_tag,
        payload=payload
    )

    # If session is complete, update session completed_at
    if event_type == 'session_complete':
        session.completed_at = timestamp
        session.save()

    print(f"LOG: Saved event '{event_type}' for {student.name} in session {session.id}")

    return Response(
        {"status": "success", "message": "Telemetry event stored successfully"},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def teacher_report(request):
    """
    Endpoint to aggregate student telemetry events and run the rule-based performance classifier.
    """
    students = Student.objects.all().order_by('name')
    report_data = []

    for student in students:
        events = TelemetryEvent.objects.filter(student=student)
        
        # Calculate statistics
        pair_events = events.filter(event_type='pair_base')
        total_actions = pair_events.count()
        
        # Count errors
        errors = 0
        for ev in pair_events:
            is_correct = ev.payload.get('is_correct')
            if is_correct is False:
                errors += 1
                
        # Accuracy percentage
        if total_actions > 0:
            accuracy = round(((total_actions - errors) / total_actions) * 100, 1)
        else:
            accuracy = 100.0

        # Calculate speed (avg time per base pair)
        # We check session_complete events first
        complete_events = events.filter(event_type='session_complete')
        durations = []
        for ce in complete_events:
            dur = ce.payload.get('duration_seconds')
            if dur is not None:
                durations.append(float(dur))
                
        # If no complete event duration, compute using session timestamps
        if not durations:
            sessions = Session.objects.filter(student=student)
            for sess in sessions:
                sess_pairs = pair_events.filter(session=sess).order_by('timestamp')
                if sess_pairs.count() >= 2:
                    t_start = sess_pairs.first().timestamp
                    t_end = sess_pairs.last().timestamp
                    durations.append((t_end - t_start).total_seconds())

        if durations:
            avg_duration = sum(durations) / len(durations)
            avg_time_per_base = round(avg_duration / 9.0, 2) # DNA Template is 9 bases
        else:
            avg_time_per_base = 0.0

        # Rule-Based Heuristic Classifier
        # High accuracy/fast speed -> Advanced (327-399)
        # Normal accuracy/moderate speed -> Proficient (300-326)
        # Minor errors/high retries -> Basic (278-299)
        # High error rate (>30%)/low engagement -> Below Basic (200-277)
        
        if total_actions == 0:
            # Fresh state
            opi_score = 0
            performance_band = "N/A"
            status_flag = "No Data"
            color_class = "text-zinc-500 bg-zinc-800/40 border-zinc-700/30"
        else:
            # Performance bands are determined primarily by accuracy, with speed acting as a secondary modifier/gating constraint.
            is_advanced = accuracy >= 95.0 and 0 < avg_time_per_base <= 2.5
            
            is_proficient = (
                (accuracy >= 85.0 and 0 < avg_time_per_base <= 4.0 and not is_advanced) or
                (accuracy >= 95.0 and avg_time_per_base > 2.5)
            )
            
            is_basic = (
                (accuracy >= 70.0 and 0 < avg_time_per_base <= 5.0 and not is_advanced and not is_proficient) or
                (accuracy >= 85.0 and avg_time_per_base > 4.0)
            )

            if is_advanced:
                performance_band = "Advanced"
                status_flag = "On Track"
                color_class = "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
                # Map score between 327 and 399 based on speed
                speed_factor = max(0.0, min(1.0, (2.5 - avg_time_per_base) / 2.0))
                opi_score = int(327 + speed_factor * 72)
            elif is_proficient:
                performance_band = "Proficient"
                status_flag = "On Track"
                color_class = "text-indigo-400 bg-indigo-500/10 border-indigo-500/20"
                # Map score between 300 and 326 based on speed
                speed_factor = max(0.0, min(1.0, (4.0 - avg_time_per_base) / 4.0)) if avg_time_per_base > 0 else 0.5
                opi_score = int(300 + speed_factor * 26)
            elif is_basic:
                performance_band = "Basic"
                status_flag = "Needs Support"
                color_class = "text-amber-400 bg-amber-500/10 border-amber-500/20"
                # Map score between 278 and 299
                opi_score = int(278 + (accuracy - 70.0) * (299 - 278) / 25.0)
                opi_score = max(278, min(299, opi_score))
            else:
                performance_band = "Below Basic"
                status_flag = "Needs Support"
                color_class = "text-rose-400 bg-rose-500/10 border-rose-500/20"
                # Map score between 200 and 277
                opi_score = int(200 + (accuracy / 70.0) * 77)
                opi_score = max(200, min(277, opi_score))

        report_data.append({
            "id": str(student.id),
            "name": student.name,
            "accuracy": accuracy,
            "avg_time_per_base": avg_time_per_base,
            "total_actions": total_actions,
            "errors": errors,
            "opi_score": opi_score,
            "performance_band": performance_band,
            "status_flag": status_flag,
            "color_class": color_class
        })

    return Response(report_data, status=status.HTTP_200_OK)
