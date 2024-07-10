from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        exclude = ['updated_at', 'created_at', 'uuid']  # Excluimos estos campos
        fields = [
            'student',
            'assignment',
            'grade_numeric',
            'grade_feedback',
            'grader_comments',
            'grade_numeric',
            'enabled',
            'created_at',
            'updated_at',
            'deleted_at',
            'evaluated_at',
            'assignment',
            'grade_questions',
            'grade_student_response',
            'grade_rubric',
            'error_type',
            'error_message',
            'is_archived',
            'student'
        ]
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }