from django.db import models

# Create your models here.


class User(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Contact = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Role = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
