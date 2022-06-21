from django.urls import path
from .views import StudentRegister, StudentAuthToken, StudentView

urlpatterns = [
    path('register/', StudentRegister.as_view()),
    path('login/', StudentAuthToken.as_view()),
    path('details/', StudentView.as_view()),
]

