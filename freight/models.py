from django.db import models
from users.models import User
from file_manager.models import Attachment


class Freight(User):
    """Model for Express"""
    permission_file = models.CharField(max_length=35, null=True)

    # vehicle_no = models.IntegerField() 

    def __str__(self):
        return self.company_name


