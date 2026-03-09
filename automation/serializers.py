from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password', 'role']

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'role': user.role,
                }
            }
        raise serializers.ValidationError("Invalid email or password")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'role']


from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

from rest_framework import serializers
from .models import Device  # Ensure Device model is imported

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

from rest_framework import serializers
from .models import AutomationRule  # Ensure this model exists

class AutomationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationRule
        fields = '__all__'


# class UserInteractionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInteraction
#         fields = ['id', 'user', 'device', 'command', 'timestamp', 'success']