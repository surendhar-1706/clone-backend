from django.db.models import fields
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import ValidationError
from accounts.models import Profile


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = '__all__'


class ChatRoomMessageSerializer(serializers.ModelSerializer):
    messages = ChatSerializer(many=True)

    class Meta:
        models = ChatRoom
        fields = '__all__'
