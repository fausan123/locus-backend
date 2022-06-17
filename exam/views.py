from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from drf_yasg.utils import swagger_auto_schema

from users.models import User
from .models import Exam, Subject, Question, ExamSubmission
from .serializers import ExamCreateSerializer, ActiveExamViewSerializer, CompletedExamViewSerializer

import json

class ActiveExams(generics.GenericAPIView):
    serializer_class = ActiveExamViewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Active Exams View",
                         responses={ 200: 'Data Successfully Fetched',
                                400: 'Given data is invalid'})
    
    def get(self, request):
        submitted_exams = request.user.submissions.values_list('id', flat=True)
        #print(submitted_exams)
        exams = Exam.objects.exclude(id__in = submitted_exams, is_completed=True)

        exam_dicts = []
        for exam in exams:
            subjects = exam.subjects.all()
            subs = []
            for sub in subjects:
                ques = sub.questions.all()
                ques = [que.__dict__ for que in ques]
                subs.append({'name': sub.name, 'questions': ques})
            e_dict = exam.__dict__
            e_dict['subjects'] = subs
            exam_dicts.append(e_dict)    

        #print(exams)
        exam_ser = self.serializer_class(data=exam_dicts, many=True)
        exam_ser.is_valid(raise_exception=True)
        return Response(exam_ser.data, status=status.HTTP_200_OK)

class SubmittedExams(generics.GenericAPIView):
    serializer_class = CompletedExamViewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Submitted Exams View",
                         responses={ 200: 'Data Successfully Fetched',
                                400: 'Given data is invalid'})

    def get(self, request):
        submissions = request.user.submissions.all()

        exam_dicts = []
        for su in submissions:
            subjects = su.exam.subjects.all()
            subs = []
            score = 0
            for sub in subjects:
                ques = sub.questions.all()
                que_dicts = []
                for q in ques:
                    qa = q.submissions.get(exam__student=request.user)
                    q_dict = q.__dict__
                    q_dict['answer'] = qa.answer
                    que_dicts.append(q_dict)
                    if qa.answer == q.correct_answer:
                        score += 1
                subs.append({'name': sub.name, 'questions': que_dicts})
            e_dict = su.exam.__dict__
            e_dict['subjects'] = subs
            e_dict['score'] = score
            e_dict['submitted_on'] = su.submitted_on
            exam_dicts.append(e_dict)    

        #print(exams)
        exam_ser = self.serializer_class(data=exam_dicts, many=True)
        exam_ser.is_valid(raise_exception=True)
        return Response(exam_ser.data, status=status.HTTP_200_OK)

    




# Current plan: use django admin interface
'''
class ExamCreate(GenericAPIView):
    serializer_class = ExamCreateSerializer

    @swagger_auto_schema(operation_description="Exam Create",
                         responses={ 201: 'Created Successfully',
                                409: 'Database error',
                                400: 'Given data is invalid'})

    def post(self, request):
        serializer = self.serializer_class(request.data)

        if serializer.is_valid():
            data = serializer.data
            try:
                exam = Exam(name=data['name'], description=data['description'], start_on=data['start_on'])
                exam.save()

                for sub in data['subjects']:
                    subject = Subject(name=sub['name'], exam=exam)
                    subject.save()

                for question in data['questions']:
                    subject = Subject.objects.get(exam=exam, subject=question['subject'])
                    if subject is None:
                        return Response({"Error": "Invalid Field", "Message": "The given subject for question does not exist"}, status=status.HTTP_400_BAD_REQUEST)
'''                    

