from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from accounts.models import Profile
User = get_user_model()


@receiver(post_save, sender=User)
def profile_creation(sender, instance, created, **kwargs):
    print('wow----------------------------------------')
    if created:
        Profile.objects.create(user=instance)
        print(instance)
