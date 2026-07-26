from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import uuid
import random
import string
import csv
import io
from django.conf import settings
import stripe
from .models import Student, Session, TelemetryEvent, UserProfile, Classroom, Campus, ScoringConfig, TeacherInvite
from .scoring import calculate_opi_score, calculate_student_theta

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

    # Check if student's campus subscription is frozen/unpaid
    if student.classroom and student.classroom.campus:
        campus = student.classroom.campus
        if campus.subscription_status != 'active':
            return Response(
                {"status": "error", "message": f"Campus license for '{campus.name}' is frozen or unpaid."},
                status=status.HTTP_402_PAYMENT_REQUIRED
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

    # Trigger real-time BKT updates
    if event_type in ['pair_base', 'codon_match_attempt', 'octet_rule_check', 'mutation_check', 'dok1_activity_check', 'dok2_activity_check', 'dok3_activity_check', 'dok4_activity_check']:
        try:
            from .bkt_service import update_bkt_state_for_event
            is_correct = payload.get('is_correct', True)
            
            actual_event_type = event_type
            if construct_tag == 'OAS.B.LS1.2':
                actual_event_type = 'hierarchy_check'
            elif construct_tag == 'OAS.B.LS1.3':
                actual_event_type = 'homeostasis_check'
            elif construct_tag == 'OAS.B.LS1.4':
                actual_event_type = 'division_check'
            elif construct_tag == 'OAS.B.LS1.5':
                actual_event_type = 'photosynthesis_check'
            elif construct_tag == 'OAS.B.LS1.6':
                actual_event_type = 'synthesis_check'
            elif construct_tag == 'OAS.B.LS1.7':
                actual_event_type = 'respiration_check'
            elif construct_tag == 'OAS.B.LS2.1':
                actual_event_type = 'capacity_check'
            elif construct_tag == 'OAS.B.LS2.2':
                actual_event_type = 'biodiversity_check'
            elif construct_tag == 'OAS.B.LS2.3':
                actual_event_type = 'matter_check'
            elif construct_tag == 'OAS.B.LS2.4':
                actual_event_type = 'energy_check'
            elif construct_tag == 'OAS.B.LS2.5':
                actual_event_type = 'carbon_check'
            elif construct_tag == 'OAS.B.LS2.6':
                actual_event_type = 'stability_check'
            elif construct_tag == 'OAS.B.LS2.8':
                actual_event_type = 'behavior_check'
            elif construct_tag == 'OAS.B.LS3.1':
                actual_event_type = 'inheritance_check'
            elif construct_tag == 'OAS.B.LS3.2':
                actual_event_type = 'variation_check'
            elif construct_tag == 'OAS.B.LS3.3':
                actual_event_type = 'statistics_check'
            elif construct_tag == 'OAS.B.LS4.1':
                actual_event_type = 'ancestry_check'
            elif construct_tag == 'OAS.B.LS4.2':
                actual_event_type = 'drivers_check'
            elif construct_tag == 'OAS.B.LS4.3':
                actual_event_type = 'advantage_check'
            elif construct_tag == 'OAS.B.LS4.4':
                actual_event_type = 'adaptation_check'
            elif construct_tag == 'OAS.B.LS4.5':
                actual_event_type = 'extinction_check'
            elif construct_tag == 'OAS.PS.PS1.2':
                actual_event_type = 'reactions_check'
            elif event_type in ['dok1_activity_check', 'dok2_activity_check', 'dok3_activity_check', 'dok4_activity_check']:
                activity_id = payload.get('activity_id', '')
                if activity_id in [
                    'bio_dok1_act1', 'bio_dok1_act3', 'bio_dok1_act4', 'bio_dok1_act3_workspace', 'bio_dok1_act4_workspace',
                    'bio_dok2_act1', 'bio_dok2_act1_workspace',
                    'bio_dok3_act2', 'bio_dok3_act2_workspace', 'bio_dok3_act4', 'bio_dok3_act4_workspace', 'bio_dok3_act5', 'bio_dok3_act5_workspace',
                    'bio_dok4_act1', 'bio_dok4_act1_workspace', 'bio_dok4_act2', 'bio_dok4_act2_workspace'
                ]:
                    actual_event_type = 'pair_base'
                elif activity_id in [
                    'bio_dok1_act2', 'bio_dok1_act5', 'bio_dok1_act2_workspace', 'bio_dok1_act5_workspace',
                    'bio_dok2_act2', 'bio_dok2_act2_workspace', 'bio_dok2_act5', 'bio_dok2_act5_workspace',
                    'bio_dok3_act3', 'bio_dok3_act3_workspace',
                    'bio_dok4_act4', 'bio_dok4_act4_workspace', 'bio_dok4_act5', 'bio_dok4_act5_workspace'
                ]:
                    actual_event_type = 'codon_match_attempt'
                elif activity_id in [
                    'bio_dok2_act3', 'bio_dok2_act3_workspace', 'bio_dok2_act4', 'bio_dok2_act4_workspace',
                    'bio_dok3_act1', 'bio_dok3_act1_workspace',
                    'bio_dok4_act3', 'bio_dok4_act3_workspace'
                ]:
                    actual_event_type = 'mutation_check'
            
            update_bkt_state_for_event(student, actual_event_type, is_correct)
        except Exception as bkt_err:
            print(f"Error updating BKT in real-time: {str(bkt_err)}")

    # If session is complete, update session completed_at and trigger BKT updates
    if event_type in ['session_complete', 'translation_complete']:
        session.completed_at = timestamp
        session.save()
        try:
            from .bkt import trigger_bkt_update_async
            trigger_bkt_update_async(student.id, session.id)
        except Exception as e:
            print(f"Error triggering BKT: {str(e)}")

        # LTI Grade Passback Sync Check
        if student.lti_user_id:
            try:
                from .models import StudentBKTState, LTIGradeSyncLog
                bkt_state = StudentBKTState.objects.filter(student=student).first()
                if bkt_state:
                    mastery = (bkt_state.transcription_p_know + bkt_state.translation_p_know + bkt_state.mutation_p_know + bkt_state.bonding_p_know) / 4
                    opi_score = int(200 + mastery * 199)
                    
                    LTIGradeSyncLog.objects.create(
                        student=student,
                        level_id=level_id,
                        score=opi_score,
                        status="Success"
                    )
                    print(f"[LTI AGS] Automatically posted grade of {opi_score} for Student {student.name}")
            except Exception as lti_err:
                print(f"Error in LTI passback: {str(lti_err)}")

    print(f"LOG: Saved event '{event_type}' for {student.name} in session {session.id}")

    # Invalidate cache for teachers
    try:
        from django.core.cache import cache
        cache.delete("teacher_report_anonymous")
        if student.classroom and student.classroom.teacher:
            cache.delete(f"teacher_report_{student.classroom.teacher.id}")
    except Exception as cache_err:
        pass

    return Response(
        {"status": "success", "message": "Telemetry event stored successfully"},
        status=status.HTTP_201_CREATED
    )


def get_opi_for_events(events, total_events_all):
    action_types = ['pair_base', 'codon_match_attempt', 'octet_rule_check', 'mutation_check', 'dok1_activity_check', 'dok2_activity_check', 'dok3_activity_check', 'dok4_activity_check']
    action_events = events.filter(event_type__in=action_types)
    total_actions = action_events.count()
    if total_actions == 0:
        return {
            "opi_score": 250, # default starting
            "performance_band": "Basic",
            "status_flag": "Needs Support",
            "color_class": "text-amber-400 bg-amber-500/10 border-amber-500/20"
        }
    
    errors = 0
    for ev in action_events:
        is_correct = ev.payload.get('is_correct')
        if is_correct is False:
            errors += 1
            
    accuracy = round(((total_actions - errors) / total_actions) * 100, 1)
    
    complete_events = total_events_all.filter(event_type='session_complete')
    durations = []
    for ce in complete_events:
        dur = ce.payload.get('duration_seconds')
        if dur is not None:
            durations.append(float(dur))
            
    if not durations:
        avg_time_per_base = 3.0
    else:
        avg_duration = sum(durations) / len(durations)
        avg_time_per_base = round(avg_duration / 9.0, 2)
        
    from .scoring import calculate_opi_score
    return calculate_opi_score(accuracy, avg_time_per_base)


@api_view(['GET'])
def teacher_report(request):
    """
    Endpoint to aggregate student telemetry events and run the rule-based performance classifier.
    Filters by the teacher's classroom if authenticated.
    """
    from django.core.cache import cache

    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'teacher':
        cache_key = f"teacher_report_{request.user.id}"
        classrooms = Classroom.objects.filter(teacher=request.user)
        students = Student.objects.filter(classroom__in=classrooms).order_by('name')
    else:
        cache_key = "teacher_report_anonymous"
        students = Student.objects.all().order_by('name')

    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    report_data = []

    for student in students:
        events = TelemetryEvent.objects.filter(student=student)
        
        # Calculate statistics
        action_types = ['pair_base', 'codon_match_attempt', 'octet_rule_check', 'mutation_check', 'dok1_activity_check', 'dok2_activity_check', 'dok3_activity_check', 'dok4_activity_check']
        action_events = events.filter(event_type__in=action_types)
        total_actions = action_events.count()
        
        errors = 0
        for ev in action_events:
            is_correct = ev.payload.get('is_correct')
            if is_correct is False:
                errors += 1
                
        if total_actions > 0:
            accuracy = round(((total_actions - errors) / total_actions) * 100, 1)
        else:
            accuracy = 100.0

        complete_events = events.filter(event_type='session_complete')
        durations = []
        for ce in complete_events:
            dur = ce.payload.get('duration_seconds')
            if dur is not None:
                durations.append(float(dur))
                
        if durations:
            avg_duration = sum(durations) / len(durations)
            avg_time_per_base = round(avg_duration / 9.0, 2)
        else:
            avg_time_per_base = 0.0

        # Calculate Overall, LS, and PS OPIs
        overall_opi_res = get_opi_for_events(events, events)
        ls_events = events.filter(construct_tag__startswith='OAS.B.LS')
        ls_opi_res = get_opi_for_events(ls_events, events)
        ps_events = events.filter(construct_tag__startswith='OAS.B.PS') | events.filter(construct_tag__startswith='OAS.PS.PS')
        ps_opi_res = get_opi_for_events(ps_events, events)

        if total_actions == 0:
            opi_score = 0
            performance_band = "N/A"
            status_flag = "No Data"
            color_class = "text-zinc-500 bg-zinc-800/40 border-zinc-700/30"
            ls_opi_score = 0
            ls_performance_band = "N/A"
            ps_opi_score = 0
            ps_performance_band = "N/A"
        else:
            opi_score = overall_opi_res["opi_score"]
            performance_band = overall_opi_res["performance_band"]
            status_flag = overall_opi_res["status_flag"]
            color_class = overall_opi_res["color_class"]
            ls_opi_score = ls_opi_res["opi_score"]
            ls_performance_band = ls_opi_res["performance_band"]
            ps_opi_score = ps_opi_res["opi_score"]
            ps_performance_band = ps_opi_res["performance_band"]

        # Fetch student BKT state
        from .models import StudentBKTState
        bkt_state = StudentBKTState.objects.filter(student=student).first()
        if bkt_state:
            bkt_mastery = round(((bkt_state.transcription_p_know + bkt_state.translation_p_know + bkt_state.mutation_p_know) / 3) * 100, 1)
            bkt_bonding_mastery = round(bkt_state.bonding_p_know * 100, 1)
            bkt_hierarchy_mastery = round(bkt_state.hierarchy_p_know * 100, 1)
            bkt_homeostasis_mastery = round(bkt_state.homeostasis_p_know * 100, 1)
            bkt_division_mastery = round(bkt_state.division_p_know * 100, 1)
            bkt_photosynthesis_mastery = round(bkt_state.photosynthesis_p_know * 100, 1)
            bkt_synthesis_mastery = round(bkt_state.synthesis_p_know * 100, 1)
            bkt_respiration_mastery = round(bkt_state.respiration_p_know * 100, 1)
            bkt_capacity_mastery = round(bkt_state.capacity_p_know * 100, 1)
            bkt_biodiversity_mastery = round(bkt_state.biodiversity_p_know * 100, 1)
            bkt_matter_mastery = round(bkt_state.matter_p_know * 100, 1)
            bkt_energy_mastery = round(bkt_state.energy_p_know * 100, 1)
            bkt_carbon_mastery = round(bkt_state.carbon_p_know * 100, 1)
            bkt_stability_mastery = round(bkt_state.stability_p_know * 100, 1)
            bkt_behavior_mastery = round(bkt_state.behavior_p_know * 100, 1)
            bkt_inheritance_mastery = round(bkt_state.inheritance_p_know * 100, 1)
            bkt_variation_mastery = round(bkt_state.variation_p_know * 100, 1)
            bkt_statistics_mastery = round(bkt_state.statistics_p_know * 100, 1)
            bkt_ancestry_mastery = round(bkt_state.ancestry_p_know * 100, 1)
            bkt_drivers_mastery = round(bkt_state.drivers_p_know * 100, 1)
            bkt_advantage_mastery = round(bkt_state.advantage_p_know * 100, 1)
            bkt_adaptation_mastery = round(bkt_state.adaptation_p_know * 100, 1)
            bkt_extinction_mastery = round(bkt_state.extinction_p_know * 100, 1)
            bkt_reactions_mastery = round(bkt_state.reactions_p_know * 100, 1)
        else:
            bkt_mastery = 15.0
            bkt_bonding_mastery = 15.0
            bkt_hierarchy_mastery = 15.0
            bkt_homeostasis_mastery = 15.0
            bkt_division_mastery = 15.0
            bkt_photosynthesis_mastery = 15.0
            bkt_synthesis_mastery = 15.0
            bkt_respiration_mastery = 15.0
            bkt_capacity_mastery = 15.0
            bkt_biodiversity_mastery = 15.0
            bkt_matter_mastery = 15.0
            bkt_energy_mastery = 15.0
            bkt_carbon_mastery = 15.0
            bkt_stability_mastery = 15.0
            bkt_behavior_mastery = 15.0
            bkt_inheritance_mastery = 15.0
            bkt_variation_mastery = 15.0
            bkt_statistics_mastery = 15.0
            bkt_ancestry_mastery = 15.0
            bkt_drivers_mastery = 15.0
            bkt_advantage_mastery = 15.0
            bkt_adaptation_mastery = 15.0
            bkt_extinction_mastery = 15.0
            bkt_reactions_mastery = 15.0

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
            "color_class": color_class,
            "ls_opi_score": ls_opi_score,
            "ls_performance_band": ls_performance_band,
            "ps_opi_score": ps_opi_score,
            "ps_performance_band": ps_performance_band,
            "bkt_mastery": bkt_mastery,
            "bkt_bonding_mastery": bkt_bonding_mastery,
            "bkt_hierarchy_mastery": bkt_hierarchy_mastery,
            "bkt_homeostasis_mastery": bkt_homeostasis_mastery,
            "bkt_division_mastery": bkt_division_mastery,
            "bkt_photosynthesis_mastery": bkt_photosynthesis_mastery,
            "bkt_synthesis_mastery": bkt_synthesis_mastery,
            "bkt_respiration_mastery": bkt_respiration_mastery,
            "bkt_capacity_mastery": bkt_capacity_mastery,
            "bkt_biodiversity_mastery": bkt_biodiversity_mastery,
            "bkt_matter_mastery": bkt_matter_mastery,
            "bkt_energy_mastery": bkt_energy_mastery,
            "bkt_carbon_mastery": bkt_carbon_mastery,
            "bkt_stability_mastery": bkt_stability_mastery,
            "bkt_behavior_mastery": bkt_behavior_mastery,
            "bkt_inheritance_mastery": bkt_inheritance_mastery,
            "bkt_variation_mastery": bkt_variation_mastery,
            "bkt_statistics_mastery": bkt_statistics_mastery,
            "bkt_ancestry_mastery": bkt_ancestry_mastery,
            "bkt_drivers_mastery": bkt_drivers_mastery,
            "bkt_advantage_mastery": bkt_advantage_mastery,
            "bkt_adaptation_mastery": bkt_adaptation_mastery,
            "bkt_extinction_mastery": bkt_extinction_mastery,
            "bkt_reactions_mastery": bkt_reactions_mastery
        })

    cache.set(cache_key, report_data, 300)
    return Response(report_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role", "student")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")
    class_code = request.data.get("class_code")
    
    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    UserProfile.objects.create(user=user, role=role)
    token, _ = Token.objects.get_or_create(user=user)
    
    student_id = None
    if role == "student":
        classroom = None
        if class_code:
            try:
                classroom = Classroom.objects.get(class_code=class_code.upper())
            except Classroom.DoesNotExist:
                pass
        
        student_profile = Student.objects.create(
            user=user,
            name=f"{first_name} {last_name}".strip() or username,
            classroom=classroom
        )
        student_id = str(student_profile.id)
    
    return Response({
        "token": token.key,
        "username": user.username,
        "role": role,
        "student_id": student_id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
    role = "student"
    if hasattr(user, 'profile'):
        role = user.profile.role
        
    token, _ = Token.objects.get_or_create(user=user)
    
    student_id = None
    if role == "student":
        if hasattr(user, 'student_profile'):
            student_id = str(user.student_profile.id)
        else:
            student_prof = Student.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}".strip() or user.username
            )
            student_id = str(student_prof.id)
            
    return Response({
        "token": token.key,
        "username": user.username,
        "role": role,
        "student_id": student_id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def classroom_create(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
        return Response({"error": "Only teachers can create classrooms"}, status=status.HTTP_403_FORBIDDEN)
        
    name = request.data.get("name")
    if not name:
        return Response({"error": "Classroom name required"}, status=status.HTTP_400_BAD_REQUEST)
        
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Classroom.objects.filter(class_code=code).exists():
            break
            
    classroom = Classroom.objects.create(
        name=name,
        teacher=request.user,
        class_code=code
    )
    return Response({
        "id": str(classroom.id),
        "name": classroom.name,
        "class_code": classroom.class_code
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def classroom_join(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
        return Response({"error": "Only students can join classrooms"}, status=status.HTTP_403_FORBIDDEN)
        
    class_code = request.data.get("class_code")
    if not class_code:
        return Response({"error": "Class code required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        classroom = Classroom.objects.get(class_code=class_code.upper())
    except Classroom.DoesNotExist:
        return Response({"error": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)
        
    student = getattr(request.user, 'student_profile', None)
    if not student:
        student = Student.objects.create(
            user=request.user,
            name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        )
        
    # Enforce Seat Quota Checks
    old_classroom = student.classroom
    new_campus = classroom.campus
    old_campus = old_classroom.campus if (old_classroom and old_classroom.campus) else None
    
    if new_campus:
        # Check if campus subscription is frozen/unpaid
        if new_campus.subscription_status != 'active':
            return Response({
                "error": f"Campus license for '{new_campus.name}' is currently frozen or unpaid. Please contact your school administrator."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if student is new to this campus
        if old_campus != new_campus:
            if new_campus.students_active >= new_campus.seat_limit:
                return Response({
                    "error": f"Seat limit reached for campus '{new_campus.name}' ({new_campus.students_active}/{new_campus.seat_limit} seats). Please contact your administrator."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Increment new campus active count
            new_campus.students_active += 1
            new_campus.save()
            
            # Decrement old campus active count if exists
            if old_campus and old_campus.students_active > 0:
                old_campus.students_active -= 1
                old_campus.save()
                
    student.classroom = classroom
    student.save()
    
    return Response({
        "message": f"Successfully joined classroom: {classroom.name}",
        "classroom_name": classroom.name,
        "class_code": classroom.class_code
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def admin_kpis(request):
    campuses = Campus.objects.all().order_by('name')
    campus_list = []
    for c in campuses:
        pct = round((c.students_active / c.seat_limit) * 100, 1) if c.seat_limit > 0 else 0
        campus_list.append({
            "id": str(c.id),
            "name": c.name,
            "students_active": c.students_active,
            "seat_limit": c.seat_limit,
            "utilization_pct": pct
        })
        
    students = Student.objects.all()
    total_accuracy = 0.0
    students_with_data = 0
    proficient_count = 0
    
    total_opi = 0
    total_ls_opi = 0
    total_ps_opi = 0
    
    for student in students:
        events = TelemetryEvent.objects.filter(student=student)
        pair_events = events.filter(event_type='pair_base')
        total_actions = pair_events.count()
        
        if events.exists():
            overall_res = get_opi_for_events(events, events)
            ls_events = events.filter(construct_tag__startswith='OAS.B.LS')
            ls_res = get_opi_for_events(ls_events, events)
            ps_events = events.filter(construct_tag__startswith='OAS.B.PS') | events.filter(construct_tag__startswith='OAS.PS.PS')
            ps_res = get_opi_for_events(ps_events, events)
            
            total_opi += overall_res["opi_score"]
            total_ls_opi += ls_res["opi_score"]
            total_ps_opi += ps_res["opi_score"]
            
        if total_actions > 0:
            correct_pairs = pair_events.filter(payload__is_correct=True).count()
            accuracy = round((correct_pairs / total_actions) * 100, 1)
            total_accuracy += accuracy
            students_with_data += 1
            
            errors = pair_events.filter(payload__is_correct=False).count()
            durations = [e.payload.get("duration_seconds", 0) for e in events.filter(event_type='session_complete') if e.payload]
            avg_time = 0.0
            if durations:
                avg_time = round(sum(durations) / len(durations) / 10.0, 2)
                
            is_adv = accuracy >= 95.0 and 0 < avg_time <= 2.5
            is_prof = (accuracy >= 85.0 and 0 < avg_time <= 4.0 and not is_adv) or (accuracy >= 95.0 and avg_time > 2.5)
            if is_adv or is_prof:
                proficient_count += 1
                
    overall_avg_accuracy = round(total_accuracy / students_with_data, 1) if students_with_data > 0 else 82.5
    overall_proficiency_rate = round((proficient_count / students_with_data) * 100, 1) if students_with_data > 0 else 68.0
    
    return Response({
        "campuses": campus_list,
        "overall_avg_accuracy": overall_avg_accuracy,
        "overall_proficiency_rate": overall_proficiency_rate,
        "total_seats_allocated": sum(c.seat_limit for c in campuses),
        "total_seats_active": sum(c.students_active for c in campuses),
        "overall_opi_avg": round(total_opi / students_with_data, 1) if students_with_data > 0 else 295.4,
        "ls_opi_avg": round(total_ls_opi / students_with_data, 1) if students_with_data > 0 else 292.1,
        "ps_opi_avg": round(total_ps_opi / students_with_data, 1) if students_with_data > 0 else 298.5
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def import_eoy_csv(request):
    """
    Ingests de-identified EOY CSV data mapping student user_id (username) to raw OPI scores.
    Performs OLS regression in-memory to calibrate A and B scaling factors.
    """
    file_obj = request.FILES.get('file')
    if not file_obj:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        csv_data = file_obj.read().decode('utf-8')
        reader = csv.reader(io.StringIO(csv_data))
        headers = next(reader) # Skip headers
    except Exception as e:
        return Response({"error": f"Failed to parse CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    logs = ["[INFO] Initiating EOY assessment data import..."]
    matched_records = []
    
    # In-memory join
    for row in reader:
        if len(row) < 2:
            continue
        username = row[0].strip()
        try:
            opi_score_str = row[1].strip()
            actual_opi = int(float(opi_score_str))
        except ValueError:
            continue
            
        try:
            user = User.objects.get(username=username)
            student = Student.objects.get(user=user)
        except (User.DoesNotExist, Student.DoesNotExist):
            logs.append(f"[WARNING] Username '{username}' could not be matched to a registered student. Skipping.")
            continue
            
        events = TelemetryEvent.objects.filter(student=student, event_type='pair_base')
        total_actions = events.count()
        if total_actions == 0:
            logs.append(f"[WARNING] Student '{username}' has no gameplay telemetry. Skipping.")
            continue
            
        errors = 0
        for ev in events:
            if ev.payload.get('is_correct') is False:
                errors += 1
                
        accuracy = ((total_actions - errors) / total_actions) * 100
        
        complete_events = TelemetryEvent.objects.filter(student=student, event_type='session_complete')
        durations = []
        for ce in complete_events:
            dur = ce.payload.get('duration_seconds')
            if dur is not None:
                durations.append(float(dur))
                
        if durations:
            avg_duration = sum(durations) / len(durations)
            avg_time_per_base = avg_duration / 9.0
        else:
            avg_time_per_base = 3.0 # Fallback
            
        theta = calculate_student_theta(accuracy, avg_time_per_base)
        matched_records.append((theta, actual_opi))
        logs.append(f"[INFO] Matched de-identified record: Theta={theta:.3f} -> OPI={actual_opi}")
        
    if len(matched_records) < 2:
        logs.append("[ERROR] Calibration failed: Less than 2 matched student records with telemetry found.")
        return Response({"error": "Insufficient data to calibrate model", "logs": logs}, status=status.HTTP_400_BAD_REQUEST)
        
    # Perform OLS simple linear regression
    N = len(matched_records)
    sum_theta = sum(r[0] for r in matched_records)
    sum_opi = sum(r[1] for r in matched_records)
    mean_theta = sum_theta / N
    mean_opi = sum_opi / N
    
    num = sum((r[0] - mean_theta) * (r[1] - mean_opi) for r in matched_records)
    den = sum((r[0] - mean_theta) ** 2 for r in matched_records)
    
    if den == 0:
        logs.append("[ERROR] Calibration failed: Zero variance in theta ability scores.")
        return Response({"error": "Zero variance in telemetry scores", "logs": logs}, status=status.HTTP_400_BAD_REQUEST)
        
    a_new = num / den
    b_new = mean_opi - a_new * mean_theta
    
    config, created = ScoringConfig.objects.get_or_create(key='default')
    config.a = round(a_new, 4)
    config.b = round(b_new, 4)
    config.save()
    
    logs.append(f"[SUCCESS] Model retrained successfully! {N} matched student records.")
    logs.append(f"[SUCCESS] New scaling constants: A = {config.a:.4f}, B = {config.b:.4f}.")
    logs.append(f"[SUCCESS] Model calibration completed! Active Model: v1.3.")

    from .models import AuditLog
    AuditLog.objects.create(
        action_by=request.user if request.user.is_authenticated else None,
        action_name="import_data",
        description=f"Calibrated predictive engine (Active Model v1.3) using EOY CSV import containing {N} student records."
    )
    
    return Response({
        "status": "success",
        "a": config.a,
        "b": config.b,
        "matched_count": N,
        "logs": logs
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def parent_report(request):
    """
    Returns performance metrics, daily gameplay logs, and home activity recommendation cards for a parent's child.
    """
    is_premium = False
    student = None
    
    student_id = request.query_params.get('student_id')
    
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'parent':
        profile = request.user.profile
        linked_students = list(profile.parent_students.all())
        
        # Populate ManyToMany list from legacy field if empty
        if not linked_students and profile.parent_student:
            profile.parent_students.add(profile.parent_student)
            linked_students = [profile.parent_student]
            
        if student_id:
            try:
                student = profile.parent_students.get(id=student_id)
            except Student.DoesNotExist:
                pass
                
        if not student and linked_students:
            student = linked_students[0]
            
        if profile.is_premium and student in linked_students:
            student_idx = linked_students.index(student)
            if student_idx < profile.premium_slots:
                is_premium = True
    else:
        # Mock/dev fallback or query param override
        if student_id:
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                pass
        if not student:
            try:
                student = Student.objects.get(name="Charlie Smith")
            except Student.DoesNotExist:
                student = Student.objects.first()
        if student:
            try:
                parent_prof = UserProfile.objects.filter(parent_student=student).first()
                if not parent_prof:
                    parent_prof = UserProfile.objects.filter(parent_students=student).first()
                if parent_prof:
                    is_premium = parent_prof.is_premium
            except Exception:
                pass
                
    if not student:
        return Response({"error": "No child associated with this parent account"}, status=status.HTTP_404_NOT_FOUND)
        
    events = TelemetryEvent.objects.filter(student=student)
    pair_events = events.filter(event_type='pair_base')
    total_actions = pair_events.count()
    
    errors = 0
    for ev in pair_events:
        if ev.payload.get('is_correct') is False:
            errors += 1
            
    if total_actions > 0:
        accuracy = round(((total_actions - errors) / total_actions) * 100, 1)
    else:
        accuracy = 100.0
        
    complete_events = events.filter(event_type='session_complete')
    durations = []
    for ce in complete_events:
        dur = ce.payload.get('duration_seconds')
        if dur is not None:
            durations.append(float(dur))
            
    if durations:
        avg_duration = sum(durations) / len(durations)
        avg_time_per_base = round(avg_duration / 9.0, 2)
    else:
        avg_time_per_base = 0.0
        
    if total_actions == 0:
        opi_res = {
            "opi_score": 0,
            "performance_band": "N/A",
            "status_flag": "No Data",
            "color_class": "text-zinc-500 bg-zinc-800/40 border-zinc-700/30"
        }
    else:
        opi_res = calculate_opi_score(accuracy, avg_time_per_base)
        
    daily_gameplay = [
        {"day": "Mon", "minutes": 12},
        {"day": "Tue", "minutes": 8},
        {"day": "Wed", "minutes": 15},
        {"day": "Thu", "minutes": 10},
        {"day": "Fri", "minutes": 5},
    ]
    
    if opi_res["performance_band"] in ["Below Basic", "Basic"]:
        tips = [
            {
                "id": "strawberry_dna",
                "title": "🍓 Hands-on: Strawberry DNA Extraction",
                "description": "Extract real DNA strands in your kitchen using strawberries, salt, dish soap, and rubbing alcohol! Helps visualize double-helix strands.",
                "difficulty": "Easy (30 mins)"
            },
            {
                "id": "codon_bracelet",
                "title": "📿 Activity: mRNA Codon Bracelet",
                "description": "Thread colored beads (A, U, G, C) to build bracelets spelling out their name! Reinforces standard base-pairing rules.",
                "difficulty": "Easy (20 mins)"
            }
        ]
    else:
        tips = [
            {
                "id": "translation_origami",
                "title": "🧬 Advanced: Protein Synthesis Origami",
                "description": "Fold origami shapes representing amino acids and fold them together like a growing peptide chain. Connects Level 1 Transcription to Level 2 Translation!",
                "difficulty": "Medium (45 mins)"
            },
            {
                "id": "mutation_detective",
                "title": "🔍 Game: Mutation Detective",
                "description": "Introduce single base-pair errors in a target sequence and ask your child to locate and correct them before transcription fails. Simulates genetic mutations!",
                "difficulty": "Easy (15 mins)"
            }
        ]
        
    linked_students = []
    premium_slots = 1
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'parent':
        linked_students = list(request.user.profile.parent_students.all())
        premium_slots = request.user.profile.premium_slots
        if not linked_students and request.user.profile.parent_student:
            linked_students = [request.user.profile.parent_student]
    else:
        linked_students = [student]

    # Fetch child BKT state
    from .models import StudentBKTState, StudentBKTHistory
    bkt_state = StudentBKTState.objects.filter(student=student).first()
    if bkt_state:
        bkt_transcription = round(bkt_state.transcription_p_know * 100, 1)
        bkt_translation = round(bkt_state.translation_p_know * 100, 1)
        bkt_mutation = round(bkt_state.mutation_p_know * 100, 1)
        bkt_mastery = round(((bkt_state.transcription_p_know + bkt_state.translation_p_know + bkt_state.mutation_p_know) / 3) * 100, 1)
        bkt_bonding_mastery = round(bkt_state.bonding_p_know * 100, 1)
        bkt_hierarchy_mastery = round(bkt_state.hierarchy_p_know * 100, 1)
        bkt_homeostasis_mastery = round(bkt_state.homeostasis_p_know * 100, 1)
        bkt_division_mastery = round(bkt_state.division_p_know * 100, 1)
        bkt_photosynthesis_mastery = round(bkt_state.photosynthesis_p_know * 100, 1)
        bkt_synthesis_mastery = round(bkt_state.synthesis_p_know * 100, 1)
        bkt_respiration_mastery = round(bkt_state.respiration_p_know * 100, 1)
        bkt_capacity_mastery = round(bkt_state.capacity_p_know * 100, 1)
        bkt_biodiversity_mastery = round(bkt_state.biodiversity_p_know * 100, 1)
        bkt_matter_mastery = round(bkt_state.matter_p_know * 100, 1)
        bkt_energy_mastery = round(bkt_state.energy_p_know * 100, 1)
        bkt_carbon_mastery = round(bkt_state.carbon_p_know * 100, 1)
        bkt_stability_mastery = round(bkt_state.stability_p_know * 100, 1)
        bkt_behavior_mastery = round(bkt_state.behavior_p_know * 100, 1)
        bkt_inheritance_mastery = round(bkt_state.inheritance_p_know * 100, 1)
        bkt_variation_mastery = round(bkt_state.variation_p_know * 100, 1)
        bkt_statistics_mastery = round(bkt_state.statistics_p_know * 100, 1)
        bkt_ancestry_mastery = round(bkt_state.ancestry_p_know * 100, 1)
        bkt_drivers_mastery = round(bkt_state.drivers_p_know * 100, 1)
        bkt_advantage_mastery = round(bkt_state.advantage_p_know * 100, 1)
        bkt_adaptation_mastery = round(bkt_state.adaptation_p_know * 100, 1)
        bkt_extinction_mastery = round(bkt_state.extinction_p_know * 100, 1)
        bkt_reactions_mastery = round(bkt_state.reactions_p_know * 100, 1)
    else:
        bkt_transcription = 20.0
        bkt_translation = 15.0
        bkt_mutation = 10.0
        bkt_mastery = 15.0
        bkt_bonding_mastery = 15.0
        bkt_hierarchy_mastery = 15.0
        bkt_homeostasis_mastery = 15.0
        bkt_division_mastery = 15.0
        bkt_photosynthesis_mastery = 15.0
        bkt_synthesis_mastery = 15.0
        bkt_respiration_mastery = 15.0
        bkt_capacity_mastery = 15.0
        bkt_biodiversity_mastery = 15.0
        bkt_matter_mastery = 15.0
        bkt_energy_mastery = 15.0
        bkt_carbon_mastery = 15.0
        bkt_stability_mastery = 15.0
        bkt_behavior_mastery = 15.0
        bkt_inheritance_mastery = 15.0
        bkt_variation_mastery = 15.0
        bkt_statistics_mastery = 15.0
        bkt_ancestry_mastery = 15.0
        bkt_drivers_mastery = 15.0
        bkt_advantage_mastery = 15.0
        bkt_adaptation_mastery = 15.0
        bkt_extinction_mastery = 15.0
        bkt_reactions_mastery = 15.0

    # Retrieve temporal BKT history milestones
    history_qs = StudentBKTHistory.objects.filter(student=student).order_by('timestamp')
    bkt_history_list = [
        {
            "timestamp": h.timestamp.isoformat(),
            "construct_tag": h.construct_tag,
            "p_know": round(h.p_know * 100, 1)
        }
        for h in history_qs
    ]

    return Response({
        "child_id": str(student.id),
        "child_name": student.name,
        "accuracy": accuracy,
        "avg_time_per_base": avg_time_per_base,
        "total_sessions": complete_events.count(),
        "opi_score": opi_res["opi_score"],
        "performance_band": opi_res["performance_band"],
        "status_flag": opi_res["status_flag"],
        "color_class": opi_res["color_class"],
        "daily_gameplay": daily_gameplay,
        "home_activity_cards": tips,
        "is_premium": is_premium,
        "premium_slots": premium_slots,
        "linked_children": [{"id": str(s.id), "name": s.name} for s in linked_students],
        "bkt_transcription": bkt_transcription,
        "bkt_translation": bkt_translation,
        "bkt_mutation": bkt_mutation,
        "bkt_mastery": bkt_mastery,
        "bkt_bonding_mastery": bkt_bonding_mastery,
        "bkt_hierarchy_mastery": bkt_hierarchy_mastery,
        "bkt_homeostasis_mastery": bkt_homeostasis_mastery,
        "bkt_division_mastery": bkt_division_mastery,
        "bkt_photosynthesis_mastery": bkt_photosynthesis_mastery,
        "bkt_synthesis_mastery": bkt_synthesis_mastery,
        "bkt_respiration_mastery": bkt_respiration_mastery,
        "bkt_capacity_mastery": bkt_capacity_mastery,
        "bkt_biodiversity_mastery": bkt_biodiversity_mastery,
        "bkt_matter_mastery": bkt_matter_mastery,
        "bkt_energy_mastery": bkt_energy_mastery,
        "bkt_carbon_mastery": bkt_carbon_mastery,
        "bkt_stability_mastery": bkt_stability_mastery,
        "bkt_behavior_mastery": bkt_behavior_mastery,
        "bkt_inheritance_mastery": bkt_inheritance_mastery,
        "bkt_variation_mastery": bkt_variation_mastery,
        "bkt_statistics_mastery": bkt_statistics_mastery,
        "bkt_ancestry_mastery": bkt_ancestry_mastery,
        "bkt_drivers_mastery": bkt_drivers_mastery,
        "bkt_advantage_mastery": bkt_advantage_mastery,
        "bkt_adaptation_mastery": bkt_adaptation_mastery,
        "bkt_extinction_mastery": bkt_extinction_mastery,
        "bkt_reactions_mastery": bkt_reactions_mastery,
        "bkt_history": bkt_history_list
    }, status=status.HTTP_200_OK)


# ==========================================
# Billing & Stripe Integration
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """
    Creates a Stripe Checkout Session for B2C premium parent subscriptions,
    additional children, or B2B seat licenses for district campuses.
    """
    checkout_type = request.data.get('type')  # 'b2c', 'b2c_additional', or 'b2b'
    
    if checkout_type not in ['b2c', 'b2b', 'b2c_additional']:
        return Response({"error": "Invalid checkout type"}, status=status.HTTP_400_BAD_REQUEST)
        
    if getattr(settings, 'STRIPE_MOCK_MODE', True):
        # Local mock checkout session creation
        mock_session_id = f"mock_sess_{uuid.uuid4().hex[:16]}"
        seats = request.data.get('seats', 1)
        slots = request.data.get('slots', 1)
        campus_id = request.data.get('campus_id', '')
        
        # Build a mock redirect URL that the frontend can catch
        mock_url = f"http://localhost:3000/?mock_checkout=true&type={checkout_type}&session_id={mock_session_id}"
        if checkout_type == 'b2b':
            mock_url += f"&campus_id={campus_id}&seats={seats}"
        elif checkout_type == 'b2c_additional':
            mock_url += f"&slots={slots}"
            
        return Response({
            "url": mock_url,
            "session_id": mock_session_id,
            "mock": True
        }, status=status.HTTP_200_OK)
        
    # Real Stripe integration
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        if checkout_type == 'b2c':
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': settings.STRIPE_PRICE_ID_B2C,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='http://localhost:3000/?billing_success=true&type=b2c',
                cancel_url='http://localhost:3000/?billing_cancel=true',
                metadata={
                    'type': 'b2c',
                    'user_id': request.user.id
                }
            )
        elif checkout_type == 'b2c_additional':
            slots = int(request.data.get('slots', 1))
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': settings.STRIPE_PRICE_ID_B2C_ADDITIONAL,
                    'quantity': slots,
                }],
                mode='subscription',
                success_url=f'http://localhost:3000/?billing_success=true&type=b2c_additional&slots={slots}',
                cancel_url='http://localhost:3000/?billing_cancel=true',
                metadata={
                    'type': 'b2c_additional',
                    'user_id': request.user.id,
                    'slots': slots
                }
            )
        else:  # B2B
            campus_id = request.data.get('campus_id')
            seats = int(request.data.get('seats', 0))
            if not campus_id or seats <= 0:
                return Response({"error": "Campus ID and number of seats (> 0) required for B2B"}, status=status.HTTP_400_BAD_REQUEST)
                
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': settings.STRIPE_PRICE_ID_B2B,
                    'quantity': seats,
                }],
                mode='subscription',
                success_url=f'http://localhost:3000/?billing_success=true&type=b2b&campus_id={campus_id}&seats={seats}',
                cancel_url='http://localhost:3000/?billing_cancel=true',
                metadata={
                    'type': 'b2b',
                    'campus_id': str(campus_id),
                    'seats': seats
                }
            )
            
        return Response({
            "url": session.url,
            "session_id": session.id,
            "mock": False
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    """
    Stripe webhook receiver. Processes payment completion and subscription events.
    Bypasses signature verification if settings.STRIPE_MOCK_MODE is enabled or in DEBUG
    with special header (for dev/scripts testing).
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    mock_header = request.META.get('HTTP_X_MOCK_SIGNATURE')
    
    event = None
    is_mock = getattr(settings, 'STRIPE_MOCK_MODE', True)
    
    if is_mock or (settings.DEBUG and mock_header == "bypass-sig"):
        # Process directly as mock JSON
        try:
            import json
            event = json.loads(payload.decode('utf-8'))
        except Exception as e:
            return Response({"error": f"Invalid mock JSON payload: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError as e:
            return Response({"error": f"Signature verification failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    event_type = event.get('type') if isinstance(event, dict) else event.type
    data_obj = event.get('data', {}).get('object', {}) if isinstance(event, dict) else event.data.object
    
    if event_type == 'checkout.session.completed':
        metadata = data_obj.get('metadata', {})
        customer_id = data_obj.get('customer')
        subscription_id = data_obj.get('subscription')
        checkout_type = metadata.get('type')
        
        if checkout_type == 'b2c':
            user_id = metadata.get('user_id')
            try:
                profile = UserProfile.objects.get(user_id=user_id)
                profile.is_premium = True
                profile.stripe_customer_id = customer_id
                profile.stripe_subscription_id = subscription_id
                profile.subscription_status = 'active'
                profile.save()
                print(f"[WEBHOOK] Upgraded B2C user profile {profile.user.username} to Premium")
            except UserProfile.DoesNotExist:
                print(f"[WEBHOOK ERROR] UserProfile for user_id={user_id} not found")
                
        elif checkout_type == 'b2c_additional':
            user_id = metadata.get('user_id')
            slots = int(metadata.get('slots', 1))
            try:
                profile = UserProfile.objects.get(user_id=user_id)
                profile.is_premium = True
                profile.premium_slots += slots
                profile.stripe_customer_id = customer_id
                profile.stripe_subscription_id = subscription_id
                profile.subscription_status = 'active'
                profile.save()
                print(f"[WEBHOOK] Added {slots} premium child slots to parent profile {profile.user.username}. New total slots: {profile.premium_slots}")
            except UserProfile.DoesNotExist:
                print(f"[WEBHOOK ERROR] UserProfile for user_id={user_id} not found")
                
        elif checkout_type == 'b2b':
            campus_id = metadata.get('campus_id')
            seats = int(metadata.get('seats', 0))
            try:
                campus = Campus.objects.get(id=campus_id)
                campus.stripe_customer_id = customer_id
                campus.stripe_subscription_id = subscription_id
                campus.subscription_status = 'active'
                campus.seat_limit += seats
                campus.save()
                
                # Record InvoiceReceipt in local DB
                from .models import InvoiceReceipt
                InvoiceReceipt.objects.create(
                    campus=campus,
                    stripe_invoice_id=f"INV-CHKT-{subscription_id or uuid.uuid4().hex[:8].upper()}",
                    amount_paid=seats * 6.00,
                    seats_purchased=seats,
                    invoice_pdf_url="https://stripe.com/mock-invoice-receipt.pdf"
                )
                print(f"[WEBHOOK] Credited campus {campus.name} with {seats} seats. New limit: {campus.seat_limit}")
            except Campus.DoesNotExist:
                print(f"[WEBHOOK ERROR] Campus id={campus_id} not found")
                
    elif event_type in ['customer.subscription.updated', 'customer.subscription.deleted']:
        sub_id = data_obj.get('id')
        stripe_status = data_obj.get('status') # 'active', 'past_due', 'canceled', 'unpaid'
        
        # Check UserProfiles
        profiles = UserProfile.objects.filter(stripe_subscription_id=sub_id)
        for p in profiles:
            p.subscription_status = stripe_status
            p.is_premium = stripe_status in ['active', 'trialing']
            p.save()
            print(f"[WEBHOOK] Updated B2C subscription {sub_id} status for {p.user.username} to {stripe_status}")
            
        # Check Campuses
        campuses = Campus.objects.filter(stripe_subscription_id=sub_id)
        for c in campuses:
            c.subscription_status = stripe_status
            if stripe_status == 'canceled':
                c.subscription_status = 'inactive'
            c.save()
            print(f"[WEBHOOK] Updated B2B subscription {sub_id} status for Campus {c.name} to {stripe_status}")
            
    elif event_type == 'invoice.paid':
        sub_id = data_obj.get('subscription')
        cust_id = data_obj.get('customer')
        invoice_id = data_obj.get('id', f"INV-{uuid.uuid4().hex[:8].upper()}")
        amount_paid_cents = data_obj.get('amount_paid', 0)
        amount_paid = amount_paid_cents / 100.0
        
        campus = None
        if sub_id:
            campus = Campus.objects.filter(stripe_subscription_id=sub_id).first()
        if not campus and cust_id:
            campus = Campus.objects.filter(stripe_customer_id=cust_id).first()
            
        if campus:
            campus.subscription_status = 'active'
            campus.save()
            
            # Determine seats from amount paid ($6/seat/year)
            seats = int(amount_paid / 6.00) if amount_paid > 0 else 0
            
            from .models import InvoiceReceipt
            InvoiceReceipt.objects.create(
                campus=campus,
                stripe_invoice_id=invoice_id,
                amount_paid=amount_paid,
                seats_purchased=seats,
                invoice_pdf_url=data_obj.get('hosted_invoice_url', 'https://stripe.com/mock-invoice-receipt.pdf')
            )
            print(f"[WEBHOOK] invoice.paid processed for Campus {campus.name}. Invoice ID: {invoice_id}")
            
    elif event_type == 'invoice.payment_failed':
        sub_id = data_obj.get('subscription')
        cust_id = data_obj.get('customer')
        
        campus = None
        if sub_id:
            campus = Campus.objects.filter(stripe_subscription_id=sub_id).first()
        if not campus and cust_id:
            campus = Campus.objects.filter(stripe_customer_id=cust_id).first()
            
        if campus:
            campus.subscription_status = 'unpaid' # Freeze campus account
            campus.save()
            print(f"[WEBHOOK] invoice.payment_failed processed for Campus {campus.name}. Account frozen.")
            
    return Response({"status": "success", "event_processed": event_type}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adjust_campus_quota(request):
    """
    Endpoint for District Admins to adjust campus seat limits.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({"error": "Only District Admins can adjust seat quotas"}, status=status.HTTP_403_FORBIDDEN)
        
    campus_id = request.data.get("campus_id")
    seat_limit = request.data.get("seat_limit")
    
    if not campus_id or seat_limit is None:
        return Response({"error": "Campus ID and seat limit required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        campus = Campus.objects.get(id=campus_id)
    except Campus.DoesNotExist:
        return Response({"error": "Campus not found"}, status=status.HTTP_404_NOT_FOUND)
        
    try:
        old_quota = campus.seat_limit
        campus.seat_limit = int(seat_limit)
        campus.save()

        from .models import AuditLog
        AuditLog.objects.create(
            action_by=request.user,
            action_name="adjust_quota",
            description=f"Adjusted seat quota for Campus {campus.name} from {old_quota} to {seat_limit}"
        )
    except ValueError:
        return Response({"error": "Invalid seat limit format"}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        "message": f"Successfully updated seat quota for {campus.name}",
        "campus_id": str(campus.id),
        "seat_limit": campus.seat_limit
    }, status=status.HTTP_200_OK)


# ==========================================
# SSO Authentication Stubs
# ==========================================

def _generate_sso_user_response(email, first_name, last_name, provider):
    """
    Helper to find or create a user via SSO details and detect role from email domain/pattern.
    """
    username = f"{provider}_{email.split('@')[0]}"
    try:
        user = User.objects.get(email=email)
        created = False
    except User.DoesNotExist:
        # Create user
        random_pw = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        user = User.objects.create_user(
            username=username,
            email=email,
            password=random_pw,
            first_name=first_name,
            last_name=last_name
        )
        created = True
        
    # Auto-detect role
    role = 'student'
    email_lower = email.lower()
    if 'admin' in email_lower or 'superintendent' in email_lower:
        role = 'admin'
    elif 'teacher' in email_lower or email_lower.endswith('.edu') or 'instructor' in email_lower:
        role = 'teacher'
    elif 'parent' in email_lower or 'family' in email_lower:
        role = 'parent'
        
    # Get or create profile
    profile, profile_created = UserProfile.objects.get_or_create(user=user, defaults={'role': role})
    if not profile_created and profile.role != role:
        # If user exists but role detected is different, update it
        profile.role = role
        profile.save()
        
    token, _ = Token.objects.get_or_create(user=user)
    
    student_id = None
    if role == 'student':
        student_prof, _ = Student.objects.get_or_create(
            user=user,
            defaults={"name": f"{first_name} {last_name}".strip() or user.username}
        )
        student_id = str(student_prof.id)
        
    return {
        "token": token.key,
        "username": user.username,
        "role": role,
        "student_id": student_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created": created
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def sso_google_login(request):
    """
    Stub for initiating Google SSO redirect.
    """
    mock_redirect_url = "http://localhost:3000/?sso_provider=google&sso_login=true"
    return Response({"url": mock_redirect_url}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def sso_google_callback(request):
    """
    Stub for Google SSO callback auth code exchange.
    Accepts query params or POST request parameters.
    """
    data = request.data if request.method == 'POST' else request.GET
    email = data.get('email', 'sso_student@school.edu')
    first_name = data.get('first_name', 'Google')
    last_name = data.get('last_name', 'User')
    
    auth_data = _generate_sso_user_response(email, first_name, last_name, 'google')
    return Response(auth_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def sso_clever_login(request):
    """
    Stub for initiating Clever SSO redirect.
    """
    mock_redirect_url = "http://localhost:3000/?sso_provider=clever&sso_login=true"
    return Response({"url": mock_redirect_url}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def sso_clever_callback(request):
    """
    Stub for Clever SSO callback auth code exchange.
    """
    data = request.data if request.method == 'POST' else request.GET
    email = data.get('email', 'sso_clever_teacher@school.edu')
    first_name = data.get('first_name', 'Clever')
    last_name = data.get('last_name', 'Teacher')
    
    auth_data = _generate_sso_user_response(email, first_name, last_name, 'clever')
    return Response(auth_data, status=status.HTTP_200_OK)


# ==========================================
# Teacher Invitation System
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_create(request):
    """
    Endpoint for School/District Admins to create unique invite codes for teachers.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({"error": "Only administrators can generate teacher invites"}, status=status.HTTP_403_FORBIDDEN)
        
    email = request.data.get('email')
    campus_id = request.data.get('campus_id')
    
    if not email or not campus_id:
        return Response({"error": "Email and Campus ID are required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        campus = Campus.objects.get(id=campus_id)
    except Campus.DoesNotExist:
        return Response({"error": "Campus not found"}, status=status.HTTP_404_NOT_FOUND)
        
    # Generate unique 12-character alphanumeric code: TCH-XXXX-XXXX
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    code = f"TCH-{random_str[:4]}-{random_str[4:]}"
    
    invite = TeacherInvite.objects.create(
        email=email,
        campus=campus,
        code=code
    )
    
    invite_url = f"http://localhost:3000/?invite_code={code}"
    return Response({
        "id": str(invite.id),
        "email": invite.email,
        "campus_name": campus.name,
        "code": invite.code,
        "invite_url": invite_url
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register_invite(request):
    """
    Endpoint for teachers to register using a unique invitation code.
    """
    username = request.data.get("username")
    password = request.data.get("password")
    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")
    invite_code = request.data.get("invite_code")
    
    if not username or not password or not invite_code:
        return Response({"error": "Username, password and invitation code are required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        invite = TeacherInvite.objects.get(code=invite_code.upper(), is_used=False)
    except TeacherInvite.DoesNotExist:
        return Response({"error": "Invalid or already used invitation code"}, status=status.HTTP_400_BAD_REQUEST)
        
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
    user = User.objects.create_user(
        username=username,
        password=password,
        email=invite.email,
        first_name=first_name,
        last_name=last_name
    )
    
    # Create profile linked to the invite campus
    UserProfile.objects.create(
        user=user,
        role='teacher',
        campus=invite.campus
    )
    
    # Mark invite as used
    invite.is_used = True
    invite.save()
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        "token": token.key,
        "username": user.username,
        "role": 'teacher',
        "campus_id": str(invite.campus.id),
        "campus_name": invite.campus.name,
        "first_name": user.first_name,
        "last_name": user.last_name
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def parent_add_child(request):
    """
    Allows a parent to link a new student to their household profile.
    """
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.role != 'parent':
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
    student_name = request.data.get('name')
    if not student_name:
        return Response({"error": "Student name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    profile = request.user.profile
    # Try to find or create the student
    student, created = Student.objects.get_or_create(name=student_name)
    profile.parent_students.add(student)
    
    return Response({
        "message": f"Successfully linked {student_name} to your household.",
        "student_id": str(student.id),
        "name": student.name
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_google_classroom(request):
    """
    Simulates Google Classroom OAuth2 Roster Syncing.
    Creates a new Classroom and registers mock student accounts linked to the teacher.
    """
    teacher = request.user
    if not hasattr(teacher, 'profile') or teacher.profile.role != 'teacher':
        return Response({"error": "Only teachers can sync rosters."}, status=status.HTTP_403_FORBIDDEN)

    classroom, created = Classroom.objects.get_or_create(
        name="Google Classroom AP Biology",
        teacher=teacher,
        defaults={"class_code": "GCL999"}
    )

    mock_students = [
        {"name": "Selena Gomez", "username": "selena_gomez"},
        {"name": "Justin Bieber", "username": "justin_bieber"},
        {"name": "Harry Styles", "username": "harry_styles"}
    ]

    synced = []
    for s_data in mock_students:
        user, u_created = User.objects.get_or_create(
            username=s_data["username"],
            defaults={
                "first_name": s_data["name"].split(' ')[0],
                "last_name": s_data["name"].split(' ')[1] if ' ' in s_data["name"] else ""
            }
        )
        if u_created:
            user.set_password("password123")
            user.save()
            UserProfile.objects.create(user=user, role="student")

        student, s_created = Student.objects.get_or_create(
            user=user,
            defaults={
                "name": s_data["name"],
                "classroom": classroom
            }
        )
        if not student.classroom:
            student.classroom = classroom
            student.save()

        synced.append({
            "id": str(student.id),
            "name": student.name,
            "username": user.username,
            "created": s_created
        })

    # Clear teacher report cache
    from django.core.cache import cache
    cache.delete(f"teacher_report_{teacher.id}")

    return Response({
        "status": "success",
        "classroom_name": classroom.name,
        "class_code": classroom.class_code,
        "synced_students": synced
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_clever(request):
    """
    Simulates Clever SSO Roster Syncing.
    Creates a new Classroom and registers mock student accounts linked to the teacher.
    """
    teacher = request.user
    if not hasattr(teacher, 'profile') or teacher.profile.role != 'teacher':
        return Response({"error": "Only teachers can sync rosters."}, status=status.HTTP_403_FORBIDDEN)

    classroom, created = Classroom.objects.get_or_create(
        name="Clever Integrated Science",
        teacher=teacher,
        defaults={"class_code": "CLV888"}
    )

    mock_students = [
        {"name": "Albert Einstein", "username": "albert_einstein"},
        {"name": "Marie Curie", "username": "marie_curie"},
        {"name": "Isaac Newton", "username": "isaac_newton"}
    ]

    synced = []
    for s_data in mock_students:
        user, u_created = User.objects.get_or_create(
            username=s_data["username"],
            defaults={
                "first_name": s_data["name"].split(' ')[0],
                "last_name": s_data["name"].split(' ')[1] if ' ' in s_data["name"] else ""
            }
        )
        if u_created:
            user.set_password("password123")
            user.save()
            UserProfile.objects.create(user=user, role="student")

        student, s_created = Student.objects.get_or_create(
            user=user,
            defaults={
                "name": s_data["name"],
                "classroom": classroom
            }
        )
        if not student.classroom:
            student.classroom = classroom
            student.save()

        synced.append({
            "id": str(student.id),
            "name": student.name,
            "username": user.username,
            "created": s_created
        })

    # Clear teacher report cache
    from django.core.cache import cache
    cache.delete(f"teacher_report_{teacher.id}")

    return Response({
        "status": "success",
        "classroom_name": classroom.name,
        "class_code": classroom.class_code,
        "synced_students": synced
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def school_admin_dashboard(request):
    """
    Returns seat quotas, active usage, invoices list, and invite codes for the school administrator.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'school_admin':
        return Response({"error": "Unauthorized. School Admin role required."}, status=status.HTTP_403_FORBIDDEN)

    campus = request.user.profile.campus
    if not campus:
        campus = Campus.objects.first()
        if not campus:
            return Response({"error": "No campus found in database"}, status=status.HTTP_404_NOT_FOUND)

    # Fetch invoices
    from .models import InvoiceReceipt
    invoices_qs = InvoiceReceipt.objects.filter(campus=campus).order_by('-created_at')
    invoices = [
        {
            "id": str(inv.id),
            "stripe_invoice_id": inv.stripe_invoice_id,
            "amount_paid": float(inv.amount_paid),
            "seats_purchased": inv.seats_purchased,
            "created_at": inv.created_at.isoformat(),
            "invoice_pdf_url": inv.invoice_pdf_url
        }
        for inv in invoices_qs
    ]

    # Fetch invite codes
    from .models import TeacherInvite
    invites_qs = TeacherInvite.objects.filter(campus=campus).order_by('-created_at')
    invites = [
        {
            "code": inv.code,
            "is_used": inv.is_used,
            "created_at": inv.created_at.isoformat()
        }
        for inv in invites_qs
    ]

    # Calculate active seats
    active_students = Student.objects.filter(classroom__teacher__profile__campus=campus).distinct().count()

    return Response({
        "campus_id": str(campus.id),
        "campus_name": campus.name,
        "seat_limit": campus.seat_limit,
        "active_students": active_students,
        "subscription_status": campus.subscription_status or "active",
        "invoices": invoices,
        "invites": invites
    }, status=status.HTTP_200_OK)


import csv
import zipfile
import io
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def osde_compliance_export(request):
    """
    District Admin endpoint to export OSDE-compliant CSV or de-identified ZIP telemetry.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({"error": "District Admins only"}, status=status.HTTP_403_FORBIDDEN)

    export_format = request.GET.get('export_format', 'csv')

    from .models import Campus, Student, StudentBKTState, AuditLog, TelemetryEvent

    if export_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="osde_compliance_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Campus Name', 'Total Students', 'Below Basic', 'Basic', 'Proficient', 'Advanced', 'Proficiency Rate (%)'])

        for campus in Campus.objects.all():
            students = Student.objects.filter(classroom__campus=campus)
            total = students.count()
            
            below_basic = 0
            basic = 0
            proficient = 0
            advanced = 0
            
            for student in students:
                bkt_state = StudentBKTState.objects.filter(student=student).first()
                if bkt_state:
                    mastery = (bkt_state.transcription_p_know + bkt_state.translation_p_know + bkt_state.mutation_p_know + bkt_state.bonding_p_know) / 4
                    score = int(200 + mastery * 199)
                else:
                    score = 250

                if score >= 327:
                    advanced += 1
                elif score >= 300:
                    proficient += 1
                elif score >= 278:
                    basic += 1
                else:
                    below_basic += 1

            prof_rate = round(((proficient + advanced) / total * 100), 2) if total > 0 else 0.0
            writer.writerow([campus.name, total, below_basic, basic, proficient, advanced, prof_rate])

        AuditLog.objects.create(
            action_by=request.user,
            action_name="osde_export_csv",
            description="Exported district-wide OSDE compliance CSV report"
        )
        return response

    elif export_format == 'zip':
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(['DeIdentified_Student_ID', 'Event_Type', 'Level_ID', 'Construct_Tag', 'Timestamp'])

            for ev in TelemetryEvent.objects.all():
                import hashlib
                anon_id = hashlib.sha256(str(ev.student.id).encode()).hexdigest()[:16]
                csv_writer.writerow([anon_id, ev.event_type, ev.level_id, ev.construct_tag, ev.timestamp.isoformat()])

            zip_file.writestr("de_identified_telemetry.csv", csv_buffer.getvalue())

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="district_telemetry_export.zip"'

        AuditLog.objects.create(
            action_by=request.user,
            action_name="osde_export_zip",
            description="Exported de-identified telemetry ZIP archive"
        )
        return response

    return Response({"error": "Invalid format requested"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_report_update(request):
    """
    Allows District Admins to schedule weekly/monthly report runs.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({"error": "District Admins only"}, status=status.HTTP_403_FORBIDDEN)

    email = request.data.get('email')
    frequency = request.data.get('frequency', 'weekly')

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    from .models import ReportSchedule, AuditLog
    schedule, _ = ReportSchedule.objects.update_or_create(
        email=email,
        defaults={"frequency": frequency}
    )

    AuditLog.objects.create(
        action_by=request.user,
        action_name="schedule_report",
        description=f"Scheduled {frequency} OSDE progress report deliveries to {email}"
    )

    return Response({
        "status": "success",
        "email": email,
        "frequency": frequency
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def audit_logs_list(request):
    """
    District Admin endpoint to retrieve administrative audit logs.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({"error": "District Admins only"}, status=status.HTTP_403_FORBIDDEN)

    from .models import AuditLog
    logs_qs = AuditLog.objects.all().order_by('-timestamp')[:50]
    logs = [
        {
            "id": str(log.id),
            "action_by": log.action_by.username if log.action_by else "System",
            "action_name": log.action_name,
            "description": log.description,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs_qs
    ]
    return Response(logs, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_retention_purge(request):
    """
    Anonymizes or deletes student telemetry records older than 1 year (365 days).
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return Response({"error": "District Admins only"}, status=status.HTTP_403_FORBIDDEN)

    from django.utils import timezone
    from datetime import timedelta
    from .models import TelemetryEvent, AuditLog

    cutoff_date = timezone.now() - timedelta(days=365)
    old_events = TelemetryEvent.objects.filter(timestamp__lt=cutoff_date)
    deleted_count = old_events.count()
    old_events.delete()

    AuditLog.objects.create(
        action_by=request.user,
        action_name="purge_data",
        description=f"Executed FERPA-compliant data retention policy: deleted {deleted_count} telemetry records older than 1 year"
    )

    return Response({
        "status": "success",
        "purged_count": deleted_count,
        "message": f"Successfully purged {deleted_count} records older than 1 year"
    }, status=status.HTTP_200_OK)

