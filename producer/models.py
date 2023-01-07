from django.db import models
from users.models import User


class Producer(User):
    """Model for Petro"""

    def __str__(self):
        return self.company_name