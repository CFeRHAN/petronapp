from django.db import models
from users.models import User


class Trader(User):
    """Model For Trader"""

    def create(self, mobile, role=1):
        trader = self.model(mobile=mobile, role=role)

    # def __str__(self):
    #     return self.User.family_name
