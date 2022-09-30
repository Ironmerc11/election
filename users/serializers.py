from dataclasses import field
from urllib import response

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, serializers, status, views
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
#from django.contrib.auth.models import User
# from users.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenObtainSerializer)
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .generate_random_username import generate_random_username

User = get_user_model()

class RegisterAdminSerializer(serializers.ModelSerializer):
    
    choices = [('admin', 'admin',), ('superuser', 'superuser')]
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(required=True,validators=[validate_password]
                                     )
    
    account_type = serializers.ChoiceField(choices=choices)

    class Meta:
        model = User
        fields = ('email','password', 'account_type', 'name')
        # extra_kwargs = {
        #     'username': {'required': False},
        #     # 'last_name': {'required': True}
        # }

    def create(self, validated_data):
        print(validated_data)
        account_type = validated_data['account_type']
        user = User.objects.create(
            username=generate_random_username(),
            email=validated_data['email'],
            name=validated_data['name']
        )

        
        user.set_password(validated_data['password'])
        if account_type == 'admin':
            user.is_staff = True
        elif account_type == 'superuser':
            user.is_staff = True
            user.is_superuser = True
        user.save()
        # send email
        return validated_data


class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(message='An account with this email exist', queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password]
                                     )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'id', 'name', 'verified', 'is_superuser', 'is_staff', 'is_active']
        
        
    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')               
            
            



# Forgot and reset password
