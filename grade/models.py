from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from assignment.models import Assignment

class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    date = models.DateField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='grades/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])])

    def str(self):
        return f"{self.student_name} - {self.assignment.name}"