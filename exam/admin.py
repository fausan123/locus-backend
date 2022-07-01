from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe  

from .models import *  


# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "created_on", "is_open", "is_completed", "numquestions")
    list_filter = ("created_on", "is_open", "is_completed")

    def numquestions(self, obj):
        return obj.questions.count()    

    search_fields = ("name__startswith", )
    ordering = ("-created_on", )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "exam_link", "numquestions")
    list_filter = ("exam", )

    def numquestions(self, obj):
        return obj.questions.count()

    def exam_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:exam_exam_change", args=(obj.exam.pk,)),
            obj.exam
        ))
    exam_link.short_description = "Exam"

    search_fields = ("name__startswith", )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_no", "title", "option_a", "option_b", "option_c", "option_d", "option_e", "correct_answer", "subject", "exam")
    list_filter = ("exam", "subject", )

    search_fields = ("title__startswith", )

@admin.register(ExamSubmission)
class ExamSubmissionAdmin(admin.ModelAdmin):
    list_display = ("exam", "student_link", "submitted_on", "numquestions", "questions_attempted", "score")
    list_filter = ("submitted_on", "exam")

    def score(self, obj):
        score = 0
        qas = obj.questionanswers.all()
        for q in qas:
            if (q.answer == q.question.correct_answer):
                score += 1
        
        return score
    
    def numquestions(self, obj):
        return obj.exam.questions.count()
    
    def questions_attempted(self, obj):
        return obj.questionanswers.count()
    
    def student_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_user_change", args=(obj.student.pk,)),
            obj.student
        ))
    student_link.short_description = "Student"

    search_fields = ("student__first_name__startswith", )
    ordering = ("-submitted_on", )

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "exam", "answer", "correct_answer")

    def correct_answer(self, obj):
        return obj.question.correct_answer
