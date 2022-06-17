from django.urls import path
from .views import ActiveExams, SubmittedExams

urlpatterns = [
    path('active/', ActiveExams.as_view()),
    path('submitted/', SubmittedExams.as_view())
]
