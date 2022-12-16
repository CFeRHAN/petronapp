from threading import ThreadError
from rest_framework import serializers

from producer.models import Producer


class CreateProducerProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a new petro profile"""
    class Meta:
        model = Producer
        exclude = ['is_active','is_staff','is_superuser', 'groups', 'user_permissions']


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['company_name', 'ceo_name','id']