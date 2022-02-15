# Generated by Django 4.0.1 on 2022-02-09 13:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("CPRS_admin", "0003_studentgroup_has_project"),
    ]

    operations = [
        migrations.CreateModel(
            name="Supevisor_Profile",
            fields=[
                (
                    "supervisor",
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="profile",
                        serialize=False,
                        to="CPRS_admin.supervisor",
                    ),
                ),
                ("school", models.CharField(max_length=50, null=True)),
                ("email", models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="student_feedback",
            name="feedbackid",
        ),
        migrations.RemoveField(
            model_name="student_feedback",
            name="studentid",
        ),
        migrations.RemoveField(
            model_name="student_task",
            name="student_id",
        ),
        migrations.RemoveField(
            model_name="student_task",
            name="taskid",
        ),
        migrations.RemoveField(
            model_name="task",
            name="name",
        ),
        migrations.RemoveField(
            model_name="task",
            name="progress",
        ),
        migrations.AddField(
            model_name="client",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="mleclient",
            name="contact",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region=None, unique=True
            ),
        ),
        migrations.AddField(
            model_name="mleclient",
            name="school",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="supervisor",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="assigned_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="task_assigned_to",
                to="CPRS_admin.student",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="task_created_by",
                to="CPRS_admin.student",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="created_date",
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("New", "New"),
                    ("Started", "Started"),
                    ("Ongoing", "Ongoing"),
                    ("In QA", "In QA"),
                    ("Completed", "Completed"),
                ],
                default="New",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="title",
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AddField(
            model_name="universityclient",
            name="contact",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="universityclient",
            name="faculty",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="CPRS_admin.project",
                verbose_name="Project",
            ),
        ),
        migrations.DeleteModel(
            name="Feedback",
        ),
        migrations.DeleteModel(
            name="Student_Feedback",
        ),
        migrations.DeleteModel(
            name="Student_Task",
        ),
    ]