from django.db import models
from django.contrib.auth.models import User
import calendar
# Create your models here.
choice=[('P',"pending"),('IN',"in Progress"),('C',"Completed")]
class Task(models.Model ):
    title=models.CharField(max_length=100)
    assignedTo=models.ForeignKey(User,on_delete=models.SET_NULL, null= True, related_name='assigned_taks')
    createdBy= models.ForeignKey(User,on_delete=models.SET_NULL, null= True, related_name='created_task') # wanna it to let the name exist even the user is deleted --make sure of it--
    status=models.CharField(max_length=2,choices=choice,default="P")
    createdDate=models.DateTimeField(auto_now_add=True)
    dueDate=models.DateField()
    description =models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.title} assigned to {self.assignedTo}, due date is :{self.dueDate}" #to return data if the object put into --> print (object) this will be the defult format 
