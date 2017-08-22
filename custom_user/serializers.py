# from django.contrib.auth.models import User
from custom_user.models import CustomUser
from rest_framework.serializers import ModelSerializer


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('location',)
