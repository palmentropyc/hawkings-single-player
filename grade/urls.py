from django.urls import path
from .views import (
    AssignmentListView, AssignmentCreateView, AssignmentDetailView,
    StudentDetailView, StudentListView, StudentCreateView,
    GradeDetailView, GradeListView, GradeCreateView
)

urlpatterns = [
    path('assignment/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignment/new/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignment/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('student/', StudentListView.as_view(), name='student-list'),
    path('student/new/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('grade/', GradeListView.as_view(), name='grade-list'),
    path('grade/new/', GradeCreateView.as_view(), name='grade_create'),
    path('grade/<int:pk>/', GradeDetailView.as_view(), name='grade_detail'),
    

]
