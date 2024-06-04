from django.db import models

# Create your models here.
class WaiterShift(models.Model):
    waiter = models.ForeignKey('users.Waiter', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)

    def __str__(self):
        return f"Shift {self.id} for Waiter {self.waiter.id} at Restaurant {self.restaurant.id}"