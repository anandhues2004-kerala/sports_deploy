from django.db import models
from django.contrib.auth.models import User
#customer model
class Customer(models.Model):
     LIVE=1
     DELETE=0
     DELETE_CHOICES=((LIVE,"live"),(DELETE,"delete"))
        
     name=models.CharField(max_length=200)
     address=models.TextField()
     phone=models.CharField(max_length=10)
     user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer_profile")
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)
     delete_status=models.IntegerField(choices= DELETE_CHOICES,default=LIVE)
    
     def __str__(self):
        return self.user.username

