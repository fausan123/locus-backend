from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import StudentRegisterSerializer, StudentLoginSerializer
from .models import User

# Create your views here.

class StudentRegister(generics.GenericAPIView):
    serializer_class = StudentRegisterSerializer
    #queryset = User.objects.all

    @swagger_auto_schema(operation_description="Student Register",
                         responses={ 201: 'Registered Successfully',
                                409: 'Given data conflict with existing users',
                                400: 'Given data is invalid'})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_data = serializer.data
            try:
                student = User(**user_data)
                student.set_password(user_data['password'])
                student.save()
                return Response({'SUCCESS': "Student Created Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO
class StudentLogin(APIView):
    serializer_class = StudentLoginSerializer

    def post(self, request):
        return None


