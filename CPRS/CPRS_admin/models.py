from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    
    def __str__(self):
        full_name = self.first_name + ' ' + self.last_name
        return full_name

class Client(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=50,null=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            full_name = self.user.first_name + " " + self.user.last_name
        return full_name

class Project (models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    projecttitle = models.CharField(max_length=100,null=True)
    projectoverview = models.CharField(max_length=255,null=True)
    is_assigned = models.BooleanField(default=False) 

    def __str__(self):
        return self.projecttitle + ',' + self.projectoverview

class Student(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    course_taken = models.CharField(max_length=50,null=True)
    specialization = models.CharField(max_length=50,null=True)
    area_of_interest = models.CharField(max_length=50,null=True)
    has_group = models.BooleanField(default=False)
    def __str__(self):
        if self.user.first_name and self.user.last_name:
            full_name = self.user.first_name + " " + self.user.last_name
        return full_name

class StudentGroup(models.Model):
    student = models.ManyToManyField(Student,through='Test')


    def __str__(self):
        return str(self.id)

class Test(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    student_group = models.ForeignKey(StudentGroup,on_delete=models.CASCADE)

    class Meta():
        unique_together = [['student','student_group']]



class Supervisor(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=255,null=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            full_name = self.user.first_name + " " + self.user.last_name
        return full_name


class Student_Profile(models.Model):
    student = models.OneToOneField(Student,null=True,on_delete=models.CASCADE)
    course_taken = models.CharField(max_length=50,null=True)
    specialization = models.CharField(max_length=255,null=True)
    area_of_interest = models.CharField(max_length=255,null=True)
    skills = models.CharField(max_length=255,null=True)
    cgpa = models.FloatField()

    def __str__(self):
        return self.student.user.email + self.course_taken + self.specialization + self.area_of_interest + self.cgpa 

class Client_Type (models.Model):
    id = models.IntegerField(max_length=5,primary_key=True)
    categoryname = models.CharField(max_length=100,null=True)


class Task (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    date = models.CharField(max_length=255,null=True)
    progress = models.IntegerField(max_length=3,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

class File_Attachment (models.Model):
    id = models.IntegerField(max_length=10,primary_key=True)
    file_path = models.CharField(max_length=255,null=True)
    faprojectid = models.ForeignKey(Project,on_delete=models.CASCADE)

class Request (models.Model):
    clientid = models.ForeignKey(Client,on_delete=models.CASCADE)
    id = models.CharField(max_length=150,primary_key=True)
    message = models.CharField(max_length=255,null=True)
    approval = models.CharField(max_length=1,null=True)


class Feedback (models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=255,null=True)
    feedbacksupervisorid = models.ForeignKey(Supervisor,on_delete=models.CASCADE)
    feedbacktaskid = models.ForeignKey(Task,on_delete=models.CASCADE)

class Student_Feedback (models.Model):
    feedbackid = models.ForeignKey(Feedback,on_delete=models.CASCADE)
    studentid = models.ForeignKey(Student,on_delete=models.CASCADE)


class Student_Task (models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    taskid = models.ForeignKey(Task,on_delete=models.CASCADE)


class Recommended_Project(models.Model):
    group = models.ManyToManyField(StudentGroup)
    client = models.ManyToManyField(Client)
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    similarity_score = models.FloatField()



