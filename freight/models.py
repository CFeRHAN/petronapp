from django.db import models
from users.models import User
from file_manager.models import Attachment


class Freight(models.Model):
    """Model for Express"""
    user = models.OneToOneField(User, related_name='Freight_Profile', on_delete=models.DO_NOTHING)
    permission_file = models.CharField(max_length=35, blank=False, null=False)

    # vehicle_no = models.IntegerField() 

    def __str__(self):
        return self.user.company_name


class VehicleType(models.Model):
    """model that represents a vehicle type"""

    TYPECHOICES = [
    ('0', 'Mini Truck'),
    ('1', 'Truck'),
    ('2', 'Heavy Truck'),
    ]

    CONTAINER_CHOICES = [
    ('0', 'Open Air'),
    ('1', 'Regular'),
    ('2', 'Fridge'),
    ]

    vehicle_type = models.CharField(max_length=1, choices=TYPECHOICES)
    container_type = models.CharField(max_length=1, choices=CONTAINER_CHOICES)
    capacity = models.PositiveIntegerField()
