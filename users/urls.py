from .serializers import SignupSerializer, ChangeUserInformation
from django.urls import path
from .views import CreateUserView, VerifyAPIView, GetNewVerification, ChangeUserInformationView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('verify/',VerifyAPIView.as_view(), name='verify'),
    path('new-verify/', GetNewVerification.as_view(), name='new-verify'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change-user'),
]