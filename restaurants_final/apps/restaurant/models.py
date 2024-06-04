from django.db import models
# from apps.products.models import Product
# from apps.users.models import Waiter

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    direction = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.IntegerField()
    PersonCapacity = models.IntegerField()



class TablesRestaurant(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Table {self.table.number} in {self.restaurant.name}"
    
class Order(models.Model):
    waiter = models.ForeignKey("users.Waiter", on_delete=models.CASCADE)
    table_restaurant = models.ForeignKey(TablesRestaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} by {self.waiter.user.first_name}"


class ProductsOrder(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in Order {self.order.id}"


class Bill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    tip_percent = models.DecimalField(max_digits=5, decimal_places=2)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill {self.id} for Order {self.order.id}"