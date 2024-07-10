from django.db import models
from django.contrib.auth.models import User
from assignment.models import Assignment, Language

class Bot(models.Model):
    uuid = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bots')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='bots')
    type = models.CharField(max_length=255)
    stack = models.CharField(max_length=255)
    prompt_icebreaker = models.TextField()
    prompt_default = models.TextField()
    payload = models.JSONField()
    enabled = models.BooleanField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='bots')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.teacher.username} - {self.assignment.name}"