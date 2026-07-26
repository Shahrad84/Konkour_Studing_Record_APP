from django.urls import path
from . import views

app_name = 'study_log'

urlpatterns = [
    path('', views.my_reports, name='my_reports'),
    
    path('create/', views.create_report, name='create_report'),
    
    path('daily/<int:daily_report_id>/', views.daily_detail, name='daily_detail'),
    path('daily/<int:daily_report_id>/add/', views.add_session, name='add_session'),
    path('session/<int:session_id>/edit/', views.edit_session, name='edit_session'),
    path('session/<int:session_id>/delete/', views.delete_session, name='delete_session'),

    path('consultant/dashboard/', views.consultant_dashboard, name='consultant_dashboard'),
    path('consultant/student/<int:student_id>/', views.consultant_student_detail, name='consultant_student_detail'),
]