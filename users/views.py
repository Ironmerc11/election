# Create your views here.

from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, views

from rest_framework.permissions import AllowAny
# from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserFilter

from .permissions import IsSuperUser
from .serializers import (RegisterAdminSerializer,
                          UserSerializer, EmailTokenObtainSerializer)

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

User  = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterAdminSerializer



class GetLoggedInUser(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = UserSerializer
    ordering = ['id']
    
    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request, format=None):
        """
        Return the logged in user details.
        """
        user = User.objects.get(email=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().order_by('id')
    # queryset = User.objects.filter(is_staff=True).filter(is_superuser=False)
    permission_classes = (IsSuperUser,)
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # res = serializer.data
        # del res['password']
        return Response(serializer.data)
    
    # def get(self, request, *args, **kwargs):
    #     response = super().get(request, *args, **kwargs)
    #     print(response)
    #     return response
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ListUserVier(generics.ListAPIView):
    queryset = User.objects.all()
    # queryset = User.objects.filter(is_staff=True).filter(is_superuser=False)
    permission_classes = (IsSuperUser,)
    serializer_class = UserSerializer
    ordering = ['id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    filterset_class = UserFilter
    
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = EmailTokenObtainSerializer
    
    


# Update this
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user.first_name,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Know Your candidate"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


