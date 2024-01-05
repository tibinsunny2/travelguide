from .models import *
from  rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # ad,in register
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    # admin login
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=50)
    password=serializers.CharField(max_length=50)
    
    
from rest_framework import serializers
from .models import TravelPackage

class TravelPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPackage
        fields = '__all__'
        
class userregserializer(serializers.ModelSerializer):
    class Meta:
        model=userreg
        fields='__all__'
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class TravelblogSerializer(serializers.ModelSerializer):
    class Meta:
        model = travelblog
        fields = ['username', 'title', 'message','image1','image2','image3','date']
        read_only_fields=['date']