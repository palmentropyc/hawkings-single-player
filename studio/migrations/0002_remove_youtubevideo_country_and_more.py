# Generated by Django 4.2.9 on 2024-07-14 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studio", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="youtubevideo",
            name="country",
        ),
        migrations.AlterField(
            model_name="youtubevideo",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("es", "Spanish")],
                default="en",
                max_length=2,
            ),
        ),
    ]