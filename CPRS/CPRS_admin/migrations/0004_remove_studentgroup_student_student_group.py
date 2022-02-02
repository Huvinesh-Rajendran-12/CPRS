# Generated by Django 4.0.1 on 2022-02-02 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CPRS_admin', '0003_student_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentgroup',
            name='student',
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.studentgroup'),
        ),
    ]
