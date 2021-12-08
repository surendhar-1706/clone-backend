from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, ):
        if not email:
            return ValueError('No Email Address Found')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.email


class Languages(models.Model):
    language = models.CharField(max_length=255)

    def __str__(self):
        return self.language


class Freelancer_skills(models.Model):
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return self.skill_name


class Testimonials(models.Model):
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text


class EmploymentHistory(models.Model):
    employment_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.employment_history


class Profile(models.Model):
    UserType = (
        ('Client', 'Client'),
        ('Freelancer', 'Freelancer')
    )

    user = models.ForeignKey(UserAccount, on_delete=CASCADE)
    usertype = models.CharField(
        max_length=25, blank=True, null=True, choices=UserType)
    dp = models.ImageField(upload_to='profile_pic', blank=True)
    verified = models.BooleanField(default=False)
    languages = models.ManyToManyField(Languages, blank=True)
    bio = models.TextField(blank=True, null=True)
    total_earnings = models.FloatField(blank=True, null=True)
    total_jobs = models.IntegerField(blank=True, default=0)
    video_intro_link = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    employment_history = models.TextField(blank=True, null=True)
    skill = models.ManyToManyField('base.Skill', blank=True)

    def __str__(self):
        return self.user.email
