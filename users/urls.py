# from django.contrib.auth.views import LogoutView

from .serializers import SignupSerializer, ChangeUserInformation
from django.urls import path
from .views import (
    CreateUserView,
    VerifyAPIView,
    GetNewVerification,
    ChangeUserInformationView,
    ChangeUserPhotoView,
    LoginView,
    LoginRefreshView,
    LogOutView,
    ForgotPasswordView,
ResetPassworView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', LoginRefreshView.as_view(), name='login_refresh'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('new-verify/', GetNewVerification.as_view(), name='new-verify'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change-user'),
    path('change-photo/', ChangeUserPhotoView.as_view(), name='change-photo'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPassworView.as_view(), name='reset-password'),
]
