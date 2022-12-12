from rest_framework import serializers
from users.models import OTP, User

class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices=OTP.OtpChannel.choices)


class RequestOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields =['request_id', 'password']

class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)
    

class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    created = serializers.BooleanField()
    user_role = serializers.CharField(max_length=128, allow_null=True)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mobile', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



