from django.db import models
from django.utils import timezone 
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
    name = models.CharField(max_length=255, null=True)
    id = models.AutoField(primary_key=True)
    is_active = models.IntegerField(default=1)
    client_type = models.CharField(null=True, max_length=50)



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
    school = models.CharField(max_length=255,null=True)
    contact = PhoneNumberField(null=True,unique=True)

class UniversityClient(models.Model):
    client = models.OneToOneField(
        User,
        primary_key=True,
        default=None,
        related_name="university",
        on_delete=models.CASCADE,
    )
    faculty = models.CharField(max_length=255,null=True)
    contact = models.CharField(max_length=255,null=True)


PROJECT_STATUS = (
    ("New", "New"),
    ("Started", "Started"),
    ("Ongoing", "Ongoing"),
    ("In QA", "In QA"),
    ("Completed", "Completed"),
)
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    overview = models.TextField(null=True)
    requirements = models.TextField(null=True)
    is_assigned = models.BooleanField(default=False)
    status = models.CharField(max_length= 50, choices= PROJECT_STATUS, default= "New")
    file = models.FileField(upload_to="documents/", null=True)

    def __str__(self):
        return self.title 


class Supervisor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    id = models.AutoField(primary_key=True)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            full_name = self.user.first_name + " " + self.user.last_name
        return full_name


class Supervisor_Profile(models.Model):
    supervisor = models.OneToOneField(
        Supervisor,
        related_name="profile",
        primary_key=True,
        on_delete=models.CASCADE,
        default=None,
    )
    school = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)

class StudentGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    project = models.OneToOneField(Project, null=True, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, null=True, on_delete=models.CASCADE)
    can_view = models.IntegerField(default=0)
    has_project = models.BooleanField(default=False)

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
    group = models.ForeignKey(StudentGroup,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return (
            self.student.user.email
            + self.course_taken
            + self.specialization
            + self.area_of_interest
            + self.cgpa
        )








class Client_Request(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True)
    approval_status = models.IntegerField(default=0)




class Recommended_Project(models.Model):
    group = models.ManyToManyField(StudentGroup)
    client = models.ManyToManyField(Client)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    similarity_score = models.FloatField()
    is_approved = models.IntegerField(default=0)


TASK_STATUS = (
    ("New", "New"),
    ("Started", "Started"),
    ("Ongoing", "Ongoing"),
    ("In QA", "In QA"),
    ("Completed", "Completed"),
)

class Task(models.Model):
    '''The Task dataclass to store the task in database'''
    title = models.CharField(max_length= 70,null=True)
    project = models.ForeignKey(Project, on_delete= models.CASCADE, null= True)
    group = models.ForeignKey(StudentGroup, on_delete= models.CASCADE, null= True)
    description = models.TextField(max_length= 500, null= True)
    created_date = models.DateField(default= timezone.now, blank= True)
    due_date = models.DateField(default= timezone.now, blank= True)
    created_by = models.ForeignKey(
        Student,
        null= True,
        blank= True,
        related_name="task_created_by",
        on_delete= models.CASCADE,
    )
    assigned_to = models.ForeignKey(
        Student,
        null= True,
        blank= True,
        related_name="task_assigned_to",
        on_delete= models.CASCADE,
    )
    # assigned_by = models.ForeignKey(User, on_delete= models.CASCADE)
    status = models.CharField(max_length= 50, choices= TASK_STATUS, default= "New")
    # attachments = models.FileField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("task-detail", kwargs= {"pk": self.pk})
