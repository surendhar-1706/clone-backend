from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.backends import TokenBackend

from .pagination import CustomPaginator
from .serializers import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination, permissions
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = self.request.data
        email = data['email']
        name = data['name']
        password = data['password']
        password2 = data['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                return Response({'error': 'email erakanve  register agi irukuda'})
            if len(password) < 6:
                return Response({'error': 'password chinatha iruku doode'})
            else:
                user = User.objects.create_user(
                    email=email, password=password, name=name)
                user.save()
                return Response({'success': 'Account Create agiruchu da'})

        else:
            return Response({'error': 'password match agala'})


class ProfileData(generics.RetrieveAPIView):
    model = Profile
    queryset = Profile.objects.all()
    serializer_class = Profileserialzier

    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(
                algorithm='HS256').decode(token, verify=False)
            user = valid_data['user_id']
            self.user_id = user
        except ValidationError as v:
            print("validation error", v)
            print('current user ------------', request)
        print('self.user------', self.user_id)
        profile = Profile.objects.get(user=self.user_id)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
