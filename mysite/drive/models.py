
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')  # 'documents/' is the folder where files will be stored.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title