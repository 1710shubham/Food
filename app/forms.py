# forms.py
from django import forms
from .models import Order_Place

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order_Place
        fields = ['food_item', 'quantity']

    def save(self, user, commit=True):
        # Create the order object
        order = super().save(commit=False)
        
        # Assign the user who placed the order
        order.user = user
        
        # Calculate the total price for the order
        order.total_price = order.food_item.Food_Price * order.quantity
        
        # Save the order instance to the database
        if commit:
            order.save()

        return order
