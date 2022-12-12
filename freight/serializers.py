from rest_framework import serializers

from freight.models import Freight


class CreateFreightProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a new Express profile"""
    class Meta:
        model = Freight
        exclude = ['is_active','is_staff','is_superuser', 'groups', 'user_permissions']