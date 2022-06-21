from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .serializers import StudentRegisterSerializer, StudentLoginSerializer, StudentViewSerializer
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
                return Response({'Success': "Student Created Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_approved:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk
            }, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Unauthorized", "Message": "The account has not been apporved yet!"}, 
            status=status.HTTP_401_UNAUTHORIZED)

class StudentView(generics.GenericAPIView):
    serializer_class = StudentViewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Student Details View",
                         responses={ 200: 'Data Successfully Fetched',
                                400: 'Given token is invalid'})

    def get(self, request):

        try:
            user_serializer = self.serializer_class(data=request.user.__dict__)
            user_serializer.is_valid(raise_exception=True)

            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": type(e).__name__, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

