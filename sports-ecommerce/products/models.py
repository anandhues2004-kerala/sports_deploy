from django.db import models
#product model

class Product(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,"live"),(DELETE,"delete"))
    
    title=models.CharField(max_length=200)
    price=models.FloatField()
    description=models.TextField()
    image=models.ImageField(upload_to="media/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    priority=models.IntegerField(default=0)
    delete_status=models.IntegerField(choices= DELETE_CHOICES,default=LIVE)

    def __str__(self):
        return self.title
    
