from django.urls import path
from .views import StudentRegister

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', StudentRegister.as_view()),
    path('login/', obtain_auth_token)
]

