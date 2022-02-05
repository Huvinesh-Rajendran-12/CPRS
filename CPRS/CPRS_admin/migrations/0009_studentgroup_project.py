# Generated by Django 4.0.1 on 2022-02-04 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("CPRS_admin", "0008_alter_project_requirements"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentgroup",
            name="project",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="CPRS_admin.project",
            ),
        ),
    ]
