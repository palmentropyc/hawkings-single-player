from django import forms
from .models import Assignment, Student, Grade

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'assignment_questions', 'assignment_rubric', 'assignment_full_text', 'language']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'email']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['enabled', 'evaluated_at', 'is_archived', 'grade_numeric', 'error_message', 'ai_behaviour', 'ai_status', 'grade_feedback', 'grader_comments', 'local_path', 'grade_questions', 'grade_student_response', 'grade_rubric', 'error_type', 'language', 'assignment', 'student']
