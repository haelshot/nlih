# Generated by Django 5.0.7 on 2024-07-21 15:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_doctor_patient_appointments_delete_userprofile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctor",
            name="free_time",
        ),
    ]
