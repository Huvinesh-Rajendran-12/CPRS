# Generated by Django 4.0.1 on 2022-02-07 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("CPRS_admin", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="student_profile",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="CPRS_admin.studentgroup",
            ),
        ),
    ]