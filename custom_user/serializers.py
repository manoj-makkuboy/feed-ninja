# from django.contrib.auth.models import User
from models import CustomUser
from rest_framework.serializers import ModelSerializer
from rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(ModelSerializer):
    register_serializer = RegisterSerializer()

    class Meta:
        model = CustomUser
        fields = ('user', 'location',)
