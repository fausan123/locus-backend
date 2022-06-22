from django.urls import path
from .views import ActiveExams, SubmittedExams, SubmitExam, ActiveExamsId

urlpatterns = [
    path('active/', ActiveExams.as_view()),
    path('active/<int:id>', ActiveExamsId.as_view()),
    path('submitted/', SubmittedExams.as_view()),
    path('submit/<int:id>/', SubmitExam.as_view())
]
