from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    

class Students(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    id = models.IntegerField(max_length=11,primary_key=True)
    course_taken = models.CharField(max_length=50,null=True)
    specialization = models.CharField(max_length=50,null=True)
    area_of_interest = models.CharField(max_length=50,null=True) 

    


class Client(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    id = models.IntegerField(max_length=20,primary_key=True)
    company = models.CharField(max_length=50,null=True)



class Supervisor(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    id = models.IntegerField(max_length=20,primary_key=True)



