from rest_framework import serializers

from trader.models import Trader
from users.models import User


class CreateTraderProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a new trader profile"""
    class Meta:
        model = Trader
        exclude = ['is_active','is_staff','is_superuser', 'groups', 'user_permissions', 'last_login', 'role']
