from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student_name', 'date', 'assignment', 'file']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }