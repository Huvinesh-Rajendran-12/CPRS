from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        full_name = self.first_name + " " + self.last_name
        return full_name


class Client(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    is_active = models.IntegerField(default=1)
    client_type = models.CharField(null=True, max_length=50)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            full_name = self.user.first_name + " " + self.user.last_name
        return full_name


class IndustryClient(models.Model):
    client = models.OneToOneField(
        Client,
        primary_key=True,
        default=None,
        related_name="industry",
        on_delete=models.CASCADE,
    )
    company = models.CharField(max_length=50, null=True)
    address = models.TextField(null=True)
    contact = PhoneNumberField(null=True, unique=True)


class MLEClient(models.Model):
    client = models.OneToOneField(
        User,
        primary_key=True,
        default=None,
        related_name="mle",
        on_delete=models.CASCADE,
    )


class UniversityClient(models.Model):
    client = models.OneToOneField(
        User,
        primary_key=True,
        default=None,
        related_name="university",
        on_delete=models.CASCADE,
    )


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    overview = models.TextField(null=True)
    requirements = models.TextField(null=True)
    is_assigned = models.BooleanField(default=False)
    file = models.FileField(upload_to="documents/", null=True)

    def __str__(self):
        return self.projecttitle + "," + self.projectoverview


class StudentGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    can_view = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + "," + self.name


class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    student_no = models.IntegerField(null=True, unique=True)
    has_group = models.BooleanField(default=False)
    group = models.ForeignKey(StudentGroup, null=True, on_delete=models.CASCADE)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            full_name = self.user.first_name + " " + self.user.last_name
        return full_name


class Supervisor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            full_name = self.user.first_name + " " + self.user.last_name
        return full_name


class Student_Profile(models.Model):
    student = models.OneToOneField(
        Student,
        related_name="profile",
        primary_key=True,
        on_delete=models.CASCADE,
        default=None,
    )
    course_taken = models.CharField(max_length=50, null=True)
    specialization = models.CharField(max_length=255, null=True)
    area_of_interest = models.CharField(max_length=255, null=True)
    skills = models.CharField(max_length=255, null=True)
    cgpa = models.FloatField()

    def __str__(self):
        return (
            self.student.user.email
            + self.course_taken
            + self.specialization
            + self.area_of_interest
            + self.cgpa
        )


class Client_Type(models.Model):
    id = models.IntegerField(max_length=5, primary_key=True)
    categoryname = models.CharField(max_length=100, null=True)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    progress = models.IntegerField(max_length=3, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class File_Attachment(models.Model):
    id = models.IntegerField(max_length=10, primary_key=True)
    file_path = models.CharField(max_length=255, null=True)
    faprojectid = models.ForeignKey(Project, on_delete=models.CASCADE)


class Client_Request(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True)
    approval_status = models.IntegerField(default=0)


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    feedbacksupervisorid = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    feedbacktaskid = models.ForeignKey(Task, on_delete=models.CASCADE)


class Student_Feedback(models.Model):
    feedbackid = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE)


class Student_Task(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    taskid = models.ForeignKey(Task, on_delete=models.CASCADE)


class Recommended_Project(models.Model):
    group = models.ManyToManyField(StudentGroup)
    client = models.ManyToManyField(Client)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    similarity_score = models.FloatField()
    is_approved = models.IntegerField(default=0)
