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
    





from studio.models import Course, Subject
from django_countries.fields import CountryField



from django import forms
from .models import Bot
from studio.models import Course, Subject
from django_countries.fields import CountryField
from django_countries import countries


class BotForm(forms.ModelForm):
    country = forms.ChoiceField(choices=[])
    course = forms.ModelChoiceField(queryset=Course.objects.none(), required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False)

    class Meta:
        model = Bot
        fields = ['name', 'description', 'country', 'course', 'subject']

    def __init__(self, *args, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)
        available_countries = Course.objects.values_list('country', flat=True).distinct()
        country_choices = [(code, name) for code, name in countries if code in available_countries]
        self.fields['country'].choices = country_choices

        if 'country' in self.data:
            try:
                country = self.data.get('country')
                self.fields['course'].queryset = Course.objects.filter(country=country).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['subject'].queryset = Subject.objects.filter(course_id=course_id).order_by('name')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.country.course_set.order_by('name')
            self.fields['subject'].queryset = self.instance.course.subject_set.order_by('name')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.country = self.cleaned_data['country']
        instance.course = self.cleaned_data['course']
        instance.subject = self.cleaned_data['subject']

        # Set fixed values for type and stack
        instance.type = 'content-bot'
        instance.stack = 'openai-streamlit'

        # Set fixed values for prompt_icebr and payload
        instance.prompt_icebr = 'en qué me puedes ayudar?'
        instance.payload = {
            "api_key": os.environ.get('OPENAI_API_KEY_SINGLE_PLAYER_BOTS'),
            "assistant_id": "asst_XXXXX"
        }

        # Set other required fields
        instance.uuid = str(ObjectId())
        instance.enabled = True
        instance.prompt_default = f"Eres un tutor académico que trabajas en {instance.country}, en la asignatura {instance.subject.name} del curso {instance.course.name}. Ayuda al alumno a lo que te pregunte adaptándote al temario de esa asignatura"
        instance.grade = None
        instance.name = f'Tutor de {instance.subject.name}'
        instance.description = f'Tutor de {instance.subject.name} del curso {instance.course.name}, {instance.country}'
         # Get or create Language and Student instances
        instance.language, _ = Language.objects.get_or_create(id=1)
        instance.student = None

        if commit:
            instance.save()

        return instance

