from .serializers import SignupSerializer, ChangeUserInformation
from django.urls import path
from .views import (
    CreateUserView,
    VerifyAPIView,
    GetNewVerification,
    ChangeUserInformationView,
    ChangeUserPhotoView,
    LoginView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/',VerifyAPIView.as_view(), name='verify'),
    path('new-verify/', GetNewVerification.as_view(), name='new-verify'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change-user'),
    path('change-photo/', ChangeUserPhotoView.as_view(), name='change-photo'),
]