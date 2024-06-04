from django.db import models
from apps.restaurant.models import Restaurant

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    all_restaurants = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class ProductsRestaurant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} at {self.restaurant.name}"
