# Generated by Django 4.2.9 on 2024-07-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grade", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="uuid",
            field=models.CharField(default="668ea354dc4e8c5c624bdf2e", max_length=24),
        ),
        migrations.AlterField(
            model_name="bot",
            name="uuid",
            field=models.CharField(default="668ea354dc4e8c5c624bdf31", max_length=24),
        ),
        migrations.AlterField(
            model_name="grade",
            name="uuid",
            field=models.CharField(default="668ea354dc4e8c5c624bdf30", max_length=24),
        ),
        migrations.AlterField(
            model_name="student",
            name="uuid",
            field=models.CharField(default="668ea354dc4e8c5c624bdf2f", max_length=24),
        ),
    ]
