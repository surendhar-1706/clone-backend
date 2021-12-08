from django.db.models import fields
from . models import *
from . views import *
from rest_framework import serializers
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import ValidationError
from accounts.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    print('Running post serializer')
    skill = SkillSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    def set_the_user(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(
                algorithm='HS256').decode(token, verify=False)
            user = valid_data['user_id']

            profile = Profile.objects.get(user=user)

            new_test = User.objects.get(id=int(user))
            self.user = new_test
            print('new_test00000000000000', new_test)

        except ValidationError as v:
            print("validation error", v)
            print('current user ------------', request)

    def create(self, validated_data):
        print('from create', self.user)
        validated_data["user"] = self.user
        skill_data = validated_data.pop('skill')
        post = Post.objects.create(**validated_data)
        for skill in skill_data:
            print(skill, 'printing skill from serializer')
            skill, created = Skill.objects.get_or_create(name=skill['name'])
            post.skill.add(skill)
        return post


class PostSerializerStaticPage(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id']
