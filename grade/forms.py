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
        fields = ['student', 'evaluated_at', 'language', 'assignment', 'local_path']