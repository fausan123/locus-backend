from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.

class Exam(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    start_on = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    students = models.ManyToManyField(User, related_name="exams")

    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=15)
    exam = models.ForeignKey(Exam, related_name="subjects", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exam} - {self.name}"

class Question(models.Model):
    title = models.TextField()
    option_a = models.CharField(max_length=50)
    option_b = models.CharField(max_length=50)
    option_c = models.CharField(max_length=50)
    option_d = models.CharField(max_length=50)
    correct_answer = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    exam = models.ForeignKey(Exam, related_name="questions", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="questions", on_delete=models.CASCADE)  # required cascade?

    def __str__(self):
        return f"{self.title}"

class ExamSubmission(models.Model):
    student = models.ForeignKey(User, related_name="submissions", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name="submissions", on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.exam} - {self.student}"

class QuestionAnswer(models.Model):
    exam = models.ForeignKey(ExamSubmission, related_name="questionanswers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="submissions", on_delete=models.CASCADE)
    answer = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], blank=True)

    def __str__(self):
        return f"{self.question} - {self.answer}"


