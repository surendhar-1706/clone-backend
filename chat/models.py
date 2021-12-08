from django.core.checks import messages
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from accounts.models import Profile
# Create your models here.


class ChatMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=CASCADE, default=1)
    name = models.CharField(blank=True, null=True, max_length=100)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_ten(self):
        return ChatMessage.objects.order_by('-timestamp').all()[:10]

    def __str__(self):
        return self.content


class ChatRoom(models.Model):
    user_id_1 = models.CharField(blank=True, default='1', max_length=100)
    user_id_2 = models.CharField(blank=True, default='2', max_length=100)
    room_name = models.CharField(blank=True, default='cool', max_length=100)
    messages = models.ManyToManyField(
        ChatMessage)

    def __str__(self):
        return self.room_name
