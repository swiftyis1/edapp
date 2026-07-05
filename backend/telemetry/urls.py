from django.urls import path
from . import views

urlpatterns = [
    path('telemetry/', views.telemetry_receive, name='telemetry_receive'),
    path('reports/teacher/', views.teacher_report, name='teacher_report'),
]
