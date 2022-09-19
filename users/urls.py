from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, UserView, GetLoggedInUser, ListUserVier
# SetNewPasswordAPIView, VerifyEmail, PasswordTokenCheckAPI, RequestPasswordResetEmail
# from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
#     path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user-list/', ListUserVier.as_view(), name='users-list'),
    path('user/<int:pk>/', UserView.as_view(), name='users'),
    path('user/me/', GetLoggedInUser.as_view(), name='loggedIn-user'),

#     path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
#     path('request-reset-email/', RequestPasswordResetEmail.as_view(),
#          name="request-reset-email"),
#     path('password-reset/<uidb64>/<token>/',
#          PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
#     path('password-reset-complete', SetNewPasswordAPIView.as_view(),
#          name='password-reset-complete')
]