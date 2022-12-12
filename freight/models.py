from django.db import models
from users.models import User
from file_manager.models import Attachment


class Freight(User):
    """Model for Express"""
    permission = models.ForeignKey(Attachment, related_name="attachment", on_delete=models.CASCADE, null=True)

    # vehicle_no = models.IntegerField() 

    def __str__(self):
        return self.company_name


