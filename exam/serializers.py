from rest_framework import serializers
from .models import *


class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class QuestionCreateSerializer(serializers.ModelSerializer):
    subject = serializers.CharField()
    
    class Meta:
        model = Question
        fields = ['title', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

class ExamCreateSerializer(serializers.ModelSerializer):
    subjects = SubjectCreateSerializer(many=True)
    questions = QuestionCreateSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['name', 'description', 'start_on']

##########################################################################
class ActiveQuestionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'option_a', 'option_b', 'option_c', 'option_d']

class ActiveSubjectViewSerializer(serializers.ModelSerializer):
    questions = ActiveQuestionViewSerializer(many=True)
    
    class Meta:
        model = Subject
        fields = ['name', 'questions']

class ActiveExamViewSerializer(serializers.ModelSerializer):
    subjects = ActiveSubjectViewSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['name', 'description', 'start_on', 'subjects']

###########################################################################
class CompletedQuestionViewSerializer(serializers.ModelSerializer):
    answer = serializers.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], allow_blank=True)

    class Meta:
        model = Question
        fields = ['title', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'answer']

class CompletedSubjectViewSerializer(serializers.ModelSerializer):
    questions = CompletedQuestionViewSerializer(many=True)
    
    class Meta:
        model = Subject
        fields = ['name', 'questions']

class CompletedExamViewSerializer(serializers.ModelSerializer):
    subjects = CompletedSubjectViewSerializer(many=True)
    submitted_on = serializers.DateTimeField()
    score = serializers.IntegerField()


    class Meta:
        model = Exam
        fields = ['name', 'description', 'start_on', 'subjects', 'score', 'submitted_on']

