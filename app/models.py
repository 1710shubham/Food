from django.db import models
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    Role = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def get_email_field_name(self):
        return 'Email'


class Admin(models.Model):
    Food_Name = models.CharField(max_length=100)
    Food_Description = models.CharField(max_length=100)
    Food_Price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for prices
    Food_Category = models.CharField(max_length=100)
    Food_Image = models.ImageField(upload_to='food_images/')  # Image field to handle image uploads

    def __str__(self):
        return self.Food_Name
    
class Order_Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who placed the order
    food_item = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Link to the food item ordered
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the food item ordered
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    order_status = models.CharField(max_length=20, default='Pending')  # Order status (e.g., Pending, Completed, etc.)
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time the order was placed

    def __str__(self):
        return f"Order {self.id} by {self.user.Name}"
