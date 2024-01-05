from django.shortcuts import render
from .serializer import *
# Create your views here.
from rest_framework import generics
from .models import *
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import  authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password

class UserCreationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "Registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    
class signview(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            uname=serializer.validated_data.get("username")
            password=serializer.validated_data.get("password")
            user = authenticate(request,username=uname,password=password)
            if user:
                login(request,user)
                return Response({'msg':'Logged in Successfully'})
            else:
                return Response({'msg':"Login Failed"})
            
class logoutview(APIView):
    def post(self,request):
        logout(request)
        return Response({'msg':'Logged out Sccessfully..'})
    

class TravelPackageListView(generics.ListAPIView):
    queryset = TravelPackage.objects.all()
    serializer_class = TravelPackageSerializer

class TravelPackageCreateView(generics.CreateAPIView):
    serializer_class = TravelPackageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TravelPackageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TravelPackage.objects.all()
    serializer_class = TravelPackageSerializer
    permission_classes = [IsAuthenticated]
    
    
class UserRegListCreateView(generics.ListCreateAPIView):
    queryset = userreg.objects.all()
    serializer_class = userregserializer

    def create(self, request, *args, **kwargs):
        # Check if the user already exists based on unique fields (e.g., email)
        existing_user = userreg.objects.filter(email=request.data.get('email')).first()

        if existing_user:
            response_data = {
                'error': 'User with the provided email already exists.',
                # 'data': userregserializer(existing_user).data
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = {
            'message': 'User registered successfully!',
            'data': serializer.data
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UserRegUpdateAPIView(APIView):
    def get(self, request, id):
        user = get_object_or_404(userreg, id=id)
        serializer = userregserializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(userreg, id=id)
        serializer = userregserializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = userreg(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = userreg.objects.all()
    serializer_class = userregserializer
    
    

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                user = userreg.objects.get(username=username, password=password)
                # If user is found, login successful
                response_data = {
                    'message': 'Login successful',
                    'data': userregserializer(user).data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except userreg.DoesNotExist:
                # If user is not found, authentication failed
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # If serializer validation fails, return the validation errors with a custom error code
            error_data = {
                'error_code': 'BAD_REQUEST',
                'errors': serializer.errors
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
    
        

class SubmitFeedbackView(APIView):
    def get(self, request, *args, **kwargs):
        feedback_entries = travelblog.objects.all()
        serializer = TravelblogSerializer(feedback_entries, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TravelblogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)