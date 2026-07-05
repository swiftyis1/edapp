from django.urls import path
from . import views

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
]
