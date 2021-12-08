from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('profile_data/', ProfileData.as_view())
]
