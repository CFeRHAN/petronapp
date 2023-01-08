from rest_framework import serializers

from freight.models import Freight
from users.models import User


class CreateFreightProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a new Express profile"""
    permission_file = serializers.CharField()

    class Meta:
        model = Freight
        # fields = '__all__'
        exclude = ['is_active','is_staff','is_superuser', 'groups', 'user_permissions', 'last_login', 'role']
        # depth = 1