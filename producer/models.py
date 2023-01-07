from django.db import models
from users.models import User


class Producer(models.Model):
    user = models.OneToOneField(User, related_name='Producer_Profile', on_delete=models.DO_NOTHING)
    """Model for Petro"""

    def __str__(self):
        return self.company_name