from django import forms
from django.contrib.auth.models import User
from .models import Assignment, Student, Grade


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'assignment_questions', 'assignment_rubric', 'assignment_full_text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'evaluated_at', 'language', 'assignment', 'local_path']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['student'].queryset = Student.objects.filter(user=self.user)
            self.fields['assignment'].queryset = Assignment.objects.filter(user=self.user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance