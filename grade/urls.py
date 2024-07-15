from django.urls import path
from .views import (
    AssignmentListView, AssignmentCreateView, AssignmentDetailView, AssignmentUpdateView,
    StudentDetailView, StudentListView, StudentCreateView,
    GradeDetailView, GradeListView, GradeCreateView, BotListView, BotCreateView
)

print("URLs are being loaded")
urlpatterns = [
path('assignment/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignment/new/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignment/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignment/<int:pk>/edit/', AssignmentUpdateView.as_view(), name='assignment-edit'),
    path('student/', StudentListView.as_view(), name='student-list'),
    path('student/new/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('grade/', GradeListView.as_view(), name='grade-list'),
    path('grade/new/', GradeCreateView.as_view(), name='grade_create'),
    path('grade/<int:pk>/', GradeDetailView.as_view(), name='grade_detail'),
    path('bots/', BotListView.as_view(), name='bot-list'),
    path('bots/new/', BotCreateView.as_view(), name='bot-create'),
    path('bot/create/', BotCreateView.as_view(), name='bot-create'),

    
]

