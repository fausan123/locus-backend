from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe  

from .models import *  


# Register your models here.
admin.site.register(Exam)
admin.site.register(Subject)
admin.site.register(Question)

@admin.register(ExamSubmission)
class ExamSubmissionAdmin(admin.ModelAdmin):
    list_display = ("exam", "student_link", "submitted_on", "score")
    list_filter = ("submitted_on", "exam")

    def score(self, obj):
        score = 0
        qas = obj.questionanswers.all()
        for q in qas:
            if (q.answer == q.question.correct_answer):
                score += 1
        
        return score
    
    def student_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_user_change", args=(obj.student.pk,)),
            obj.student
        ))
    student_link.short_description = "Student"

    search_fields = ("student__first_name__startswith", )
    ordering = ("-submitted_on", )

admin.site.register(QuestionAnswer)