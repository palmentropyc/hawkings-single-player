# Generated by Django 4.2.9 on 2024-07-15 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("grade", "0020_bot_slug_alter_assignment_uuid_alter_bot_uuid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="uuid",
            field=models.CharField(default="66956f9fdc4e8c0d8b4860dd", max_length=24),
        ),
        migrations.AlterField(
            model_name="bot",
            name="uuid",
            field=models.CharField(default="66956f9fdc4e8c0d8b4860e0", max_length=24),
        ),
        migrations.AlterField(
            model_name="grade",
            name="uuid",
            field=models.CharField(default="66956f9fdc4e8c0d8b4860df", max_length=24),
        ),
        migrations.AlterField(
            model_name="student",
            name="uuid",
            field=models.CharField(default="66956f9fdc4e8c0d8b4860de", max_length=24),
        ),
        migrations.CreateModel(
            name="BotMessage",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "uuid",
                    models.CharField(default="66956f9fdc4e8c0d8b4860e1", max_length=24),
                ),
                ("message", models.TextField()),
                ("from_role", models.CharField(max_length=255)),
                ("tokens", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "bot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="grade.bot"
                    ),
                ),
            ],
        ),
    ]
