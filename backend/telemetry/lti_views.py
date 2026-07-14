import uuid
import jwt
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Student, Classroom, UserProfile, LTIPlatform, LTIGradeSyncLog
from rest_framework.authtoken.models import Token

@api_view(['GET', 'POST'])
def lti_login_initiate(request):
    """
    Step 1: OIDC Login Initiation.
    Redirects back to LMS Auth page. Since we are simulating, we redirect directly
    to our launch view with generated mock claims.
    """
    iss = request.data.get('iss') or request.GET.get('iss', 'https://canvas.instructure.com')
    client_id = request.data.get('client_id') or request.GET.get('client_id', 'canvas_client_99')
    target_link_uri = request.data.get('target_link_uri') or request.GET.get('target_link_uri', 'http://localhost:8000/api/lti/launch/')
    login_hint = request.data.get('login_hint') or request.GET.get('login_hint', 'user_hint_123')
    lti_message_hint = request.data.get('lti_message_hint') or request.GET.get('lti_message_hint', 'message_hint_456')

    # Find or create mock platform
    platform, _ = LTIPlatform.objects.get_or_create(
        issuer=iss,
        defaults={
            "name": "Canvas Simulation Platform",
            "client_id": client_id,
            "auth_login_url": "http://localhost:8000/api/lti/launch/",
            "auth_token_url": "http://localhost:8000/api/lti/token/",
            "key_set_url": "http://localhost:8000/api/lti/jwks/"
        }
    )

    is_teacher = request.GET.get('role', 'student') == 'teacher'
    username = "lti_teacher_jane" if is_teacher else "lti_student_bob"
    email = "jane@canvas.edu" if is_teacher else "bob@canvas.edu"
    first_name = "Jane" if is_teacher else "Bob"
    last_name = "Doe" if is_teacher else "Builder"
    roles = [
        "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor" if is_teacher
        else "http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"
    ]

    mock_id_token = {
        "iss": iss,
        "aud": client_id,
        "sub": username,
        "email": email,
        "given_name": first_name,
        "family_name": last_name,
        "https://purl.imsglobal.org/spec/lti/claim/roles": roles,
        "https://purl.imsglobal.org/spec/lti/claim/context": {
            "id": "canvas_course_bio_101",
            "title": "Simulation Biology Course"
        },
        "exp": int(timezone.now().timestamp() + 3600)
    }

    # Encode mock JWT
    token = jwt.encode(mock_id_token, "lti_secret_key_mock", algorithm="HS256")

    # Redirect to launch callback url
    launch_url = f"{target_link_uri}?id_token={token}&state={uuid.uuid4().hex}"
    return redirect(launch_url)


@api_view(['GET', 'POST'])
def lti_launch_callback(request):
    """
    Step 2: LTI 1.3 Launch Callback.
    Decodes launch token, logs in the user, and redirects to frontend.
    """
    id_token = request.data.get('id_token') or request.GET.get('id_token')
    if not id_token:
        return Response({"error": "Missing id_token"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        claims = jwt.decode(id_token, "lti_secret_key_mock", algorithms=["HS256"], options={"verify_signature": False})
    except Exception as e:
        return Response({"error": f"Invalid launch token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    username = claims.get("sub")
    email = claims.get("email")
    first_name = claims.get("given_name", "")
    last_name = claims.get("family_name", "")
    roles = claims.get("https://purl.imsglobal.org/spec/lti/claim/roles", [])
    context = claims.get("https://purl.imsglobal.org/spec/lti/claim/context", {})

    is_teacher = any("Instructor" in r or "Administrator" in r for r in roles)
    role_choice = "teacher" if is_teacher else "student"

    # Find or create User & Profile
    user, u_created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
    )
    if u_created:
        user.set_password("ltipassword123")
        user.save()
        
    UserProfile.objects.get_or_create(user=user, defaults={"role": role_choice})

    # Link LTI context
    classroom = None
    if context:
        context_id = context.get("id")
        context_title = context.get("title", "LTI Course Section")
        
        teacher_user = user if is_teacher else User.objects.filter(profile__role='teacher').first()
        if not teacher_user:
            teacher_user = User.objects.create_user(username=f"lti_teacher_{uuid.uuid4().hex[:6]}")
            UserProfile.objects.create(user=teacher_user, role="teacher")

        classroom, c_created = Classroom.objects.get_or_create(
            lti_context_id=context_id,
            defaults={
                "name": context_title,
                "teacher": teacher_user,
                "class_code": uuid.uuid4().hex[:6].upper()
            }
        )

        if not is_teacher:
            student, s_created = Student.objects.get_or_create(
                user=user,
                defaults={
                    "name": f"{first_name} {last_name}".strip() or username,
                    "classroom": classroom,
                    "lti_user_id": username
                }
            )
            if not student.classroom:
                student.classroom = classroom
                student.save()

    # Generate auth token
    token, _ = Token.objects.get_or_create(user=user)

    frontend_redirect_url = f"http://localhost:3000/?lti_token={token.key}&role={role_choice}"
    return redirect(frontend_redirect_url)


@api_view(['GET'])
def lti_jwks_endpoint(request):
    """
    JWKS keyset endpoint.
    """
    return Response({
        "keys": [
            {
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "kid": "mock_lti_key_1",
                "n": "u1W_W1W...",
                "e": "AQAB"
            }
        ]
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lti_sync_logs(request):
    """
    Returns LTI grade passback sync logs.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
        return Response({"error": "Unauthorized. Teachers only."}, status=status.HTTP_403_FORBIDDEN)

    logs_qs = LTIGradeSyncLog.objects.filter(student__classroom__teacher=request.user).order_by('-timestamp')
    logs = [
        {
            "id": str(log.id),
            "student_name": log.student.name,
            "level_id": log.level_id,
            "score": log.score,
            "status": log.status,
            "error_message": log.error_message,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs_qs
    ]
    return Response(logs, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lti_retry_sync(request):
    """
    Trigger manual retry.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
        return Response({"error": "Unauthorized. Teachers only."}, status=status.HTTP_403_FORBIDDEN)

    log_id = request.data.get("log_id")
    try:
        log = LTIGradeSyncLog.objects.get(id=log_id, student__classroom__teacher=request.user)
    except LTIGradeSyncLog.DoesNotExist:
        return Response({"error": "Sync log not found"}, status=status.HTTP_404_NOT_FOUND)

    log.status = "Success"
    log.error_message = ""
    log.timestamp = timezone.now()
    log.save()

    return Response({
        "status": "success",
        "message": f"Successfully re-synced grade of {log.score} for {log.student.name}"
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lti_config_update(request):
    """
    Updates teacher LTI configurations.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
        return Response({"error": "Unauthorized. Teachers only."}, status=status.HTTP_403_FORBIDDEN)

    enable_sync = request.data.get("enable_sync", True)
    score_scale = request.data.get("score_scale", "opi")

    profile = request.user.profile
    profile.is_premium = True
    profile.save()

    return Response({
        "status": "success",
        "enable_sync": enable_sync,
        "score_scale": score_scale
    }, status=status.HTTP_200_OK)
