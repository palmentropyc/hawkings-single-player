import os
from django import forms
from .models import Assignment, Language, Student, Grade
from django import forms
from .models import Bot
from bson import ObjectId
from studio.models import Course, Subject
from django_countries import countries
import random
import string

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'assignment_questions', 'assignment_rubric', 'language']

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
            self.fields['assignment'].queryset = Assignment.objects.filter(user=self.user).order_by('-created_at')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
    

class BotForm(forms.ModelForm):
    country = forms.ChoiceField(choices=[])
    course = forms.ModelChoiceField(queryset=Course.objects.none(), required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False)
    custom_prompt = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Bot
        fields = ['country', 'course', 'subject', 'custom_prompt']

    def __init__(self, *args, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)
        self.initialize_country_choices()
        self.initialize_course_and_subject_choices()

    def initialize_country_choices(self):
        available_countries = Course.objects.values_list('country', flat=True).distinct()
        country_choices = [(code, name) for code, name in countries if code in available_countries]
        self.fields['country'].choices = country_choices

    def initialize_course_and_subject_choices(self):
        if 'country' in self.data:
            self.set_course_queryset()
        if 'course' in self.data:
            self.set_subject_queryset()
        elif self.instance.pk:
            self.set_instance_course_and_subject_queryset()

    def set_course_queryset(self):
        try:
            country = self.data.get('country')
            self.fields['course'].queryset = Course.objects.filter(country=country).order_by('name')
        except (ValueError, TypeError):
            pass

    def set_subject_queryset(self):
        try:
            course_id = int(self.data.get('course'))
            self.fields['subject'].queryset = Subject.objects.filter(course_id=course_id).order_by('name')
        except (ValueError, TypeError):
            pass

    def set_instance_course_and_subject_queryset(self):
        self.fields['course'].queryset = self.instance.country.course_set.order_by('name')
        self.fields['subject'].queryset = self.instance.course.subject_set.order_by('name')

    def save(self, commit=True):
        instance = super().save(commit=False)
        self.set_instance_fields(instance)
        self.set_instance_prompt_fields(instance)
        if commit:
            instance.save()
        return instance
    



    
    def set_instance_fields(self, instance):

        def create_slug(name):
            if hasattr(name, 'name'):  # Check if the name has a 'name' attribute
                name = name.name
            trimmed_name = name[:16].replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').lower()
            random_hex = ''.join(random.choices(string.hexdigits.lower(), k=5))
            return f"{trimmed_name}-{random_hex}"
        
        instance.country = self.cleaned_data['country']
        instance.course = self.cleaned_data['course']
        instance.subject = self.cleaned_data['subject']
        instance.custom_prompt = self.cleaned_data['custom_prompt']
        instance.type = 'content-bot'
        instance.stack = 'openai-streamlit'
        instance.prompt_icebr = 'en qué me puedes ayudar?'
        instance.uuid = str(ObjectId())
        instance.enabled = True
        instance.grade = None
        instance.language, _ = Language.objects.get_or_create(id=1)
        instance.student = None
        instance.slug = create_slug(instance.subject)

    def set_instance_prompt_fields(self, instance):
        instance.prompt_default = f"Eres un tutor académico que trabajas en {instance.country}, en la asignatura {instance.subject.name} del curso {instance.course.name}. Ayuda al alumno a lo que te pregunte adaptándote al temario de esa asignatura."
        instance.name = f'Tutor de {instance.subject.name}'
        instance.description = f'Tutor de {instance.subject.name} del curso {instance.course.name}, {instance.country}'
        final_prompt = f"{instance.prompt_default} \n Además, el profesor ha dado estas instrucciones: \n {self.cleaned_data['custom_prompt'] }"
        instance.final_prompt = final_prompt

    def get_final_prompt(self):
        instance = self.instance
        return f"{instance.prompt_default} \n Además, el profesor ha dado estas instrucciones: \n {self.cleaned_data['custom_prompt'] }"