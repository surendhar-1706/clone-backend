from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    Freelancer_type = (('Beginner', 'Beginner'),
                       ('Intermediate', 'Intermediate'),
                       ('Expert', 'Expert'))
    CATEGORY = (
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('Web design', 'Web design')
    )
    WEEKLY_LENGTH = (
        ('Less than 30 hours', 'Less than 30 hours'),
        ('More than 30 hours', 'More than 30 hours')
    )
    Expected_length = (
        ('Less than a month', 'Less than a month'),
        ('More than a month', 'More than a month'),
        ('Six months', 'Six months')
    )
    Pay_type = (
        ('Hourly', 'Hourly'),
        ('Fixed-price', 'Fixed-price')
    )
    user = models.ForeignKey(
        User, on_delete=CASCADE, default=1)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(choices=CATEGORY, null=True, max_length=255)
    skill = models.ManyToManyField(Skill)
    freelancer_type = models.CharField(
        choices=Freelancer_type, max_length=255, blank=True)
    pay_type = models.CharField(choices=Pay_type, max_length=255, blank=True)
    from_price = models.FloatField(blank=True, null=True)
    to_price = models.FloatField(blank=True, null=True)
    fixed_price = models.FloatField(blank=True, null=True)
    weekly_length = models.CharField(blank=True,
                                     choices=WEEKLY_LENGTH, null=True, max_length=255)
    total_length = models.CharField(blank=True,
                                    choices=Expected_length, null=True, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
