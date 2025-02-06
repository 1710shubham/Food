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

class Admin(models.Model):
    Food_Name = models.CharField(max_length=100)
    Food_Description = models.CharField(max_length=100)
    Food_Price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for prices
    Food_Category = models.CharField(max_length=100)
    Food_Image = models.ImageField(upload_to='food_images/')  # Image field to handle image uploads

    def __str__(self):
        return self.Food_Name