# Generated by Django 4.2.9 on 2024-07-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studio", "0006_course_subject"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="uuid",
            field=models.CharField(default="669519f9dc4e8cc376dbc395", max_length=24),
        ),
    ]
