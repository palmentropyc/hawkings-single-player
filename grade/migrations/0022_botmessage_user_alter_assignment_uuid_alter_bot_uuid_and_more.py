# Generated by Django 4.2.9 on 2024-07-15 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("grade", "0021_alter_assignment_uuid_alter_bot_uuid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="botmessage",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="assignment",
            name="uuid",
            field=models.CharField(default="66957531dc4e8c17390e551c", max_length=24),
        ),
        migrations.AlterField(
            model_name="bot",
            name="uuid",
            field=models.CharField(default="66957531dc4e8c17390e551f", max_length=24),
        ),
        migrations.AlterField(
            model_name="botmessage",
            name="uuid",
            field=models.CharField(default="66957531dc4e8c17390e5520", max_length=24),
        ),
        migrations.AlterField(
            model_name="grade",
            name="uuid",
            field=models.CharField(default="66957531dc4e8c17390e551e", max_length=24),
        ),
        migrations.AlterField(
            model_name="student",
            name="uuid",
            field=models.CharField(default="66957531dc4e8c17390e551d", max_length=24),
        ),
    ]
