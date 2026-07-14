from django.urls import path
from . import views
from . import lti_views

urlpatterns = [
    path('telemetry/', views.telemetry_receive, name='telemetry_receive'),
    path('reports/teacher/', views.teacher_report, name='teacher_report'),
    path('reports/admin/kpis/', views.admin_kpis, name='admin_kpis'),
    path('auth/register/', views.auth_register, name='auth_register'),
    path('auth/login/', views.auth_login, name='auth_login'),
    path('classroom/create/', views.classroom_create, name='classroom_create'),
    path('classroom/join/', views.classroom_join, name='classroom_join'),
    path('admin/import-eoy/', views.import_eoy_csv, name='import_eoy_csv'),
    path('reports/parent/', views.parent_report, name='parent_report'),
    
    # Billing
    path('billing/checkout/', views.create_checkout_session, name='create_checkout_session'),
    path('billing/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('admin/campuses/adjust-quota/', views.adjust_campus_quota, name='adjust_campus_quota'),
    
    # SSO
    path('auth/sso/google/login/', views.sso_google_login, name='sso_google_login'),
    path('auth/sso/google/callback/', views.sso_google_callback, name='sso_google_callback'),
    path('auth/sso/clever/login/', views.sso_clever_login, name='sso_clever_login'),
    path('auth/sso/clever/callback/', views.sso_clever_callback, name='sso_clever_callback'),
    
    # Teacher Invites
    path('admin/invites/create/', views.invite_create, name='invite_create'),
    path('auth/register-invite/', views.auth_register_invite, name='auth_register_invite'),
    path('parent/add-child/', views.parent_add_child, name='parent_add_child'),
    path('sync/google-classroom/', views.sync_google_classroom, name='sync_google_classroom'),
    path('sync/clever/', views.sync_clever, name='sync_clever'),
    path('reports/school-admin/', views.school_admin_dashboard, name='school_admin_dashboard'),

    # LTI 1.3
    path('lti/login/', lti_views.lti_login_initiate, name='lti_login_initiate'),
    path('lti/launch/', lti_views.lti_launch_callback, name='lti_launch_callback'),
    path('lti/jwks/', lti_views.lti_jwks_endpoint, name='lti_jwks_endpoint'),
    path('lti/config/', lti_views.lti_config_update, name='lti_config_update'),
    path('lti/sync-logs/', lti_views.lti_sync_logs, name='lti_sync_logs'),
    path('lti/retry-sync/', lti_views.lti_retry_sync, name='lti_retry_sync'),
]
