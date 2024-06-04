from django.db import models
from django.contrib.auth.models import User


class Waiter(models.Model):
    MANAGER = 'MG'
    ADMINTABLES = 'AT'
    EXTRA = 'EX'
    
    CHARGE_CHOICES = [
        (MANAGER, 'MANAGER'),
        (ADMINTABLES, 'ADMINTABLES'),
        (EXTRA, 'EXTRA')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    charge = models.CharField(max_length=2, choices=CHARGE_CHOICES, default=EXTRA)

    def __str__(self):
        return f"Waiter {self.user.first_name}"