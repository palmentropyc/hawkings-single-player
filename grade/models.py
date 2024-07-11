from django.db import models
from django.contrib.auth.models import User
from bson import ObjectId

class Language(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(primary_key=True)
    rtl = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    iso = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    id = models.BigAutoField(primary_key=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    uuid = models.CharField(max_length=24, default=str(ObjectId()))
    name = models.CharField(max_length=255)
    assignment_questions = models.CharField(max_length=255)
    assignment_rubric = models.CharField(max_length=255)
    assignment_full_text = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(ObjectId())
        super().save(*args, **kwargs)

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    uuid = models.CharField(max_length=24, default=str(ObjectId()))
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(ObjectId())
        super().save(*args, **kwargs)

class Grade(models.Model):
    id = models.BigAutoField(primary_key=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    grade_numeric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    error_message = models.TextField(default='')
    uuid = models.CharField(max_length=24, default=str(ObjectId()))
    ai_behaviour = models.TextField(default='')
    ai_status = models.TextField(default='pending')
    grade_feedback = models.TextField(default='')
    grader_comments = models.TextField(default='')
    local_path = models.FileField(upload_to='uploads/grades/')
    grade_questions = models.TextField(default='')
    grade_student_response = models.TextField(default='')
    grade_rubric = models.TextField(default='')
    error_type = models.TextField(default='')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Grade {self.id} for Assignment {self.assignment_id} by Student {self.student_id}"

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(ObjectId())
        super().save(*args, **kwargs)

class Bot(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=24, default=str(ObjectId()))
    type = models.CharField(max_length=255)
    stack = models.CharField(max_length=255)
    prompt_icebr = models.TextField(default='')
    payload = models.JSONField()
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    prompt_default = models.TextField(default='')
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bot {self.id} - {self.type}"

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(ObjectId())
        super().save(*args, **kwargs)