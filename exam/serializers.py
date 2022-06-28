from rest_framework import serializers
from .models import *


##########################################################################
class ActiveQuestionViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ['id', 'question_no', 'title', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e']

class ActiveSubjectViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    questions = ActiveQuestionViewSerializer(many=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'questions']

class ActiveExamViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subjects = ActiveSubjectViewSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'start_on', 'subjects', 'is_open', 'is_completed']

class ActiveExamsViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'start_on', 'is_open', 'is_completed']

###########################################################################
class CompletedQuestionViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], allow_blank=True)

    class Meta:
        model = Question
        fields = ['id', 'question_no', 'title', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'correct_answer', 'answer']

class CompletedSubjectViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    questions = CompletedQuestionViewSerializer(many=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'questions']

class CompletedExamViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subjects = CompletedSubjectViewSerializer(many=True)
    submitted_on = serializers.DateTimeField()
    score = serializers.IntegerField()


    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'start_on', 'subjects', 'score', 'submitted_on']

##########################################################################################################

class SubmitExamSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], allow_blank=True)




