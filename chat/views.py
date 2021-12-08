from django.shortcuts import render
from rest_framework import generics, pagination
# Create your views here.
from rest_framework.views import APIView
from django.shortcuts import render
from .models import *
from .serializers import *
from .pagination import *
from rest_framework.views import APIView


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


# class ChatListview(generics.ListAPIView):
#     queryset = ChatMessage.objects.order_by('-id').all()
#     serializer_class = ChatSerializer
#     pagination_class = ChatPaginator

class ChatListview(APIView):
    print('ran_ChatListview------------------------')

    def get(self, request, *args, **kwargs):

        room_name = self.kwargs.get('msg_fetch_room_name', None)
        # print(room_name, 'room_name')

        queryset = ChatRoom.objects.get(room_name=room_name)
        queryset = queryset.messages.order_by('-id').all()
        print(queryset, 'queryset-------------------W')
        paginator = ChatPaginator()
        response = paginator.generate_response(
            queryset, ChatSerializer, request)

        return response
