from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.


class CustomAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_active')


admin.site.register(UserAccount, CustomAdmin)
admin.site.register(Profile)
admin.site.register(Languages)
admin.site.register(EmploymentHistory)
