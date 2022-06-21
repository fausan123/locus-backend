from genericpath import exists
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
from .models import Exam, QuestionAnswer, Subject, Question, ExamSubmission
from .serializers import ActiveExamViewSerializer, CompletedExamViewSerializer, SubmitExamSerializer

import json

class ActiveExams(generics.GenericAPIView):
    serializer_class = ActiveExamViewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Active Exams View",
                         responses={ 200: 'Data Successfully Fetched',
                                400: 'Given data is invalid'})
    
    def get(self, request):

        try:
            submitted_exams = request.user.submissions.values('exam')
            exams = Exam.objects.exclude(is_completed=True).exclude(id__in = submitted_exams)

            exam_dicts = []
            for exam in exams:
                subjects = exam.subjects.all()
                subs = []
                for sub in subjects:
                    ques = sub.questions.all()
                    ques = [que.__dict__ for que in ques]
                    subs.append({'id': sub.pk, 'name': sub.name, 'questions': ques})
                e_dict = exam.__dict__
                e_dict['subjects'] = subs
                exam_dicts.append(e_dict)    

            exam_ser = self.serializer_class(data=exam_dicts, many=True)
            exam_ser.is_valid(raise_exception=True)
            return Response(exam_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": type(e).__name__, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class SubmittedExams(generics.GenericAPIView):
    serializer_class = CompletedExamViewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Submitted Exams View",
                         responses={ 200: 'Data Successfully Fetched',
                                400: 'Given data is invalid'})

    def get(self, request):

        try:
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
                    subs.append({'id': sub.pk, 'name': sub.name, 'questions': que_dicts})
                e_dict = su.exam.__dict__
                e_dict['subjects'] = subs
                e_dict['score'] = score
                e_dict['submitted_on'] = su.submitted_on
                exam_dicts.append(e_dict)    

            #print(exams)
            exam_ser = self.serializer_class(data=exam_dicts, many=True)
            exam_ser.is_valid(raise_exception=True)
            return Response(exam_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": type(e).__name__, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class SubmitExam(generics.GenericAPIView):
    serializer_class = SubmitExamSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Submit Exam",
                         responses={ 201: 'Exam Successfully Submitted',
                                409: 'Given data conflict with existing ones',
                                400: 'Given data is invalid'})
    
    def post(self, request, id):

        serializer = self.serializer_class(data=request.data, many=True)
        
        if serializer.is_valid():
            exam_data = serializer.data
            if (not Exam.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given exam does not exist!"}, status=status.HTTP_409_CONFLICT)
            if (ExamSubmission.objects.filter(exam=id, student=request.user).exists()):
                return Response({ "Error": "Existing Submission" , "Message": "You have already submitted the exam!"}, status=status.HTTP_409_CONFLICT)

            try:
                exam = Exam.objects.get(pk=id)
                examsubmit = ExamSubmission(student=request.user, exam=exam)
                examsubmit.save()

                for ques in exam_data:
                    if (not Question.objects.filter(pk=ques['id']).exists()):
                        ques_subs = QuestionAnswer.objects.filter(exam=examsubmit)
                        ques_subs.delete()
                        examsubmit.delete()
                        return Response({ "Error": "Invalid ID" , "Message": f"The given question with id {ques['id']} does not exist!"}, status=status.HTTP_409_CONFLICT)
                    
                    question = Question.objects.get(pk=ques['id'])
                    quessubmit = QuestionAnswer(exam=examsubmit, question=question, answer=ques['answer'])
                    quessubmit.save()

                return Response({'Success': "Exam Submitted Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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

