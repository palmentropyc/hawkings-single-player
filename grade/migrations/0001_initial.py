# Generated by Django 4.2.9 on 2024-07-10 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignment",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("enabled", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "uuid",
                    models.CharField(default="668ea307dc4e8c5b8f93e3d2", max_length=24),
                ),
                ("name", models.CharField(max_length=255)),
                ("assignment_questions", models.CharField(max_length=255)),
                ("assignment_rubric", models.CharField(max_length=255)),
                ("assignment_full_text", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("enabled", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("rtl", models.BooleanField(default=False)),
                ("default", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=255)),
                ("iso", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "uuid",
                    models.CharField(default="668ea307dc4e8c5b8f93e3d3", max_length=24),
                ),
                ("name", models.CharField(max_length=255)),
                ("surname", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("enabled", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("evaluated_at", models.DateTimeField(blank=True, null=True)),
                ("is_archived", models.BooleanField(default=False)),
                (
                    "grade_numeric",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("error_message", models.TextField(default="")),
                (
                    "uuid",
                    models.CharField(default="668ea307dc4e8c5b8f93e3d4", max_length=24),
                ),
                ("ai_behaviour", models.TextField(default="")),
                ("ai_status", models.TextField(default="pending")),
                ("grade_feedback", models.TextField(default="")),
                ("grader_comments", models.TextField(default="")),
                ("local_path", models.TextField(default="")),
                ("grade_questions", models.TextField(default="")),
                ("grade_student_response", models.TextField(default="")),
                ("grade_rubric", models.TextField(default="")),
                ("error_type", models.TextField(default="")),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="grade.assignment",
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="grade.language"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="grade.student"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bot",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "uuid",
                    models.CharField(default="668ea307dc4e8c5b8f93e3d5", max_length=24),
                ),
                ("type", models.CharField(max_length=255)),
                ("stack", models.CharField(max_length=255)),
                ("prompt_icebr", models.TextField(default="")),
                ("payload", models.JSONField()),
                ("enabled", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("prompt_default", models.TextField(default="")),
                (
                    "grade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="grade.grade"
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="grade.language"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="grade.student"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="assignment",
            name="language",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="grade.language"
            ),
        ),
        migrations.AddField(
            model_name="assignment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]