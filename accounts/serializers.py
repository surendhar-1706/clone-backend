from django.db.models import fields
from rest_framework import serializers
from django.db import models
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import ValidationError
from accounts.models import Profile
User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class Profileserialzier(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user',)
