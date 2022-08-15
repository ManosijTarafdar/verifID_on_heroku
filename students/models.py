from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StudentData(models.Model):
    collegeid = models.CharField(max_length=30,null=True)
    firstname = models.CharField(max_length=50,primary_key=True)
    lastname = models.CharField(max_length=50)
    department = models.CharField(max_length=20)
    email  =models.CharField(max_length=50)
    phoneno = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    year = models.CharField(max_length=10,null=True)
    profile_pic = models.ImageField(null=True,blank=True)
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.collegeid