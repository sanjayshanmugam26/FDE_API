from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    unique_number = models.CharField(max_length=10, unique=True)