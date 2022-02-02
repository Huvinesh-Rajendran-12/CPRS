# Generated by Django 4.0.1 on 2022-02-01 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CPRS_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Request',
            fields=[
                ('id', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255, null=True)),
                ('approval_status', models.IntegerField(default=0)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.client')),
            ],
        ),
        migrations.AddField(
            model_name='studentgroup',
            name='can_view',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentgroup',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.client'),
        ),
        migrations.DeleteModel(
            name='Request',
        ),
        migrations.AddField(
            model_name='client_request',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.studentgroup'),
        ),
    ]
