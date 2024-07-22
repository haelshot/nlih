# Generated by Django 5.0.7 on 2024-07-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_remove_doctor_free_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointments",
            name="status",
            field=models.CharField(
                choices=[
                    ("scheduled", "Scheduled"),
                    ("rejected", "Rejected"),
                    ("checked-in", "Checked-in"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                max_length=15,
            ),
        ),
    ]