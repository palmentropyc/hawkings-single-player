from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    name = models.CharField(max_length=200)
    description = models.TextField()
    rubric = models.TextField()
    answers = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.teacher.username}"

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name