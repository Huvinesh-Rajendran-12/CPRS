# Generated by Django 4.0.1 on 2022-02-02 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CPRS_admin', '0002_client_request_studentgroup_can_view_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
