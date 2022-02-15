# Generated by Django 4.0.1 on 2022-02-11 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("CPRS_admin", "0010_alter_client_request_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentgroup",
            name="has_requested",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="client_request",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="client_request",
                to="CPRS_admin.studentgroup",
            ),
        ),
    ]