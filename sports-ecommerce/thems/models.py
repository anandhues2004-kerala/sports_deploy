from django.db import models

class Sitesettings(models.Model):
    banner=models.ImageField(upload_to="media/site")
    caption=models.TextField()
