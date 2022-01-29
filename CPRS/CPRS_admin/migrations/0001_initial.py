# Generated by Django 4.0.1 on 2022-01-28 09:50

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client_Type',
            fields=[
                ('id', models.IntegerField(max_length=5, primary_key=True, serialize=False)),
                ('categoryname', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('projecttitle', models.CharField(max_length=100, null=True)),
                ('projectoverview', models.CharField(max_length=255, null=True)),
                ('is_assigned', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.client')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_group', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_supervisor', models.BooleanField(default=False)),
                ('is_client', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('progress', models.IntegerField(max_length=3, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.project')),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.student')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.student')),
                ('taskid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.task')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_taken', models.CharField(max_length=50, null=True)),
                ('specialization', models.CharField(max_length=255, null=True)),
                ('area_of_interest', models.CharField(max_length=255, null=True)),
                ('skills', models.CharField(max_length=255, null=True)),
                ('cgpa', models.FloatField()),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.student')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedbackid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.feedback')),
                ('studentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255, null=True)),
                ('approval', models.CharField(max_length=1, null=True)),
                ('clientid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.client')),
            ],
        ),
        migrations.CreateModel(
            name='Recommended_Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=255)),
                ('similarity_score', models.FloatField()),
                ('is_approved', models.IntegerField(default=0)),
                ('client', models.ManyToManyField(to='CPRS_admin.Client')),
                ('group', models.ManyToManyField(to='CPRS_admin.StudentGroup')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.project')),
            ],
        ),
        migrations.CreateModel(
            name='File_Attachment',
            fields=[
                ('id', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('file_path', models.CharField(max_length=255, null=True)),
                ('faprojectid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.project')),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='feedbacksupervisorid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.supervisor'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='feedbacktaskid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CPRS_admin.task'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
