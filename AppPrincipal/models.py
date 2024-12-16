from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)  
    subtitle = models.CharField(max_length=200, blank=True, null=True)  
    body = models.TextField()  
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='posts/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title