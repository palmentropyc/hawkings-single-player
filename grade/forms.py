import json
import os
from django import forms
from django.contrib.auth.models import User
from .models import Assignment, Language, Student, Grade
from django import forms
from .models import Bot
from bson import ObjectId
from django import forms
from .models import Bot

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
    





class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BotForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.user:
            instance.user = self.user
        else:
            raise ValueError("User is required to create a Bot instance")

        # Set fixed values for type and stack
        instance.type = 'content-bot'
        instance.stack = 'openai-streamlit'

        # Set fixed values for prompt_icebr and payload
        instance.prompt_icebr = 'inicia la conversación'
        instance.payload = {
            "api_key": os.environ.get('OPENAI_API_KEY_SINGLE_PLAYER_BOTS'),
            "assistant_id": "asst_XXXXX"
        }

        # Set other required fields
        instance.uuid = str(ObjectId())
        instance.enabled = True
        instance.prompt_default = 'Default prompt'
        instance.grade = None
        
        # Get or create Language and Student instances
        instance.language, _ = Language.objects.get_or_create(id=1)
        instance.student, _ = Student.objects.get_or_create(id=1, user=self.user)

        if commit:
            instance.save()
        
        return instance
