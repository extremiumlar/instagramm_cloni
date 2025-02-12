from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import SignupSerializer
from .models import User

class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    #yangi foydalanuvchilarni hech qanday token , id si bo'lmaydi ularni kira olishi uchun Allowany qilish kerak
    permission_classes = (permissions.AllowAny,)
