from django.urls import path
from .views import StudentRegister, StudentAuthToken

urlpatterns = [
    path('register/', StudentRegister.as_view()),
    path('login/', StudentAuthToken.as_view())
]

