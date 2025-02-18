# import datetime
from datetime import datetime

from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer
from .models import User, CODE_VERIFIED,NEW


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    #yangi foydalanuvchilarni hech qanday token , id si bo'lmaydi ularni kira olishi uchun Allowany qilish kerak
    permission_classes = (permissions.AllowAny,)

class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        code = request.data.get('code',)
        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "token": user.token()['refresh_token'],
            }
        )
    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(),code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else :
            verifies.update(is_confirmed=True)
        if user.auth_status==NEW:
            user.auth_status=CODE_VERIFIED
            user.save()
        return True

