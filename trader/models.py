from django.db import models
from users.models import User


class Trader(User):
    # user = models.OneToOneField(User, related_name='Trader_Profile', on_delete=models.DO_NOTHING)
    """Model For Trader"""

    def __str__(self):
        return self.company_name
