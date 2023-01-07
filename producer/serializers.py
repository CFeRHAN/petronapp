from threading import ThreadError
from rest_framework import serializers

from producer.models import Producer
from users.models import User


class CreateProducerProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a new petro profile"""
    class Meta:
        model = User
        exclude = ['is_active','is_staff','is_superuser', 'groups', 'user_permissions', 'last_login', 'role']


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'company_name', 'ceo_name']