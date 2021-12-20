from django.shortcuts import render
from rest_framework import generics, pagination
# Create your views here.
from rest_framework.views import APIView
from django.shortcuts import render
from .models import *
from .serializers import *
from .pagination import *
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
User = get_user_model()
from accounts.models import Profile
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


class ChatRoomView(APIView):
    # print('Chat Room View ran')
    # print('get method ran----------- from ChatRoomView')
    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        # print(token,'from ChatRoomView')
        valid_data = TokenBackend(
                algorithm='HS256').decode(token, verify=False)
        user = valid_data['user_id']
        # profile = Profile.objects.get(user=user)
        # new_test = User.objects.get(id=int(user))
        # all_rooms = ChatRoom.objects.filter(user)
        queryset = ChatRoom.objects.filter(user_id_1=user)|ChatRoom.objects.filter(user_id_2=user)
        print('printing combined queryset-------------------W')
        serializer = ChatRoomNameSerializer(queryset,many=True)
        ah_print = Response(serializer.data)
        print(ah_print.data)
        return Response(serializer.data)