import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from assignment.models import Assignment

def generate_short_uuid():
    return uuid.uuid4().hex[:24]

class Grade(models.Model):
    uuid = models.CharField(max_length=24, default=generate_short_uuid, editable=False, unique=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='grades')
    bot = models.ForeignKey('bot.Bot', on_delete=models.SET_NULL, null=True, related_name='grades')
    ai_status = models.CharField(max_length=255, default='pending')
    grade_feedback = models.TextField(blank=True, default='')
    grader_comments = models.TextField(blank=True, default='')
    grade_numeric = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)  # Cambiado a auto_now=True
    deleted_at = models.DateTimeField(null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    grade_questions = models.TextField(blank=True, default='')
    grade_student_response = models.TextField(blank=True, default='')
    grade_rubric = models.TextField(blank=True, default='')
    error_type = models.TextField(blank=True, default='')
    error_message = models.TextField(blank=True, default='')
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.name}"
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')
    student_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"