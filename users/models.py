import hashlib
import uuid
from datetime import datetime, timedelta
import random

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel

ORDINARY_USER, MANAGER, ADMIN = ('ordinary_user', 'manager', 'admin')
VIA_EMAIL , VIA_PHONE = ('via_email', 'via_phone')
NEW, CODE_VERIFIED, DONE , PHOTO_STEP = ('new', 'code_verified', 'done', 'photo_step')
class User(AbstractUser,BaseModel):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_PHONE , VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_STEP, PHOTO_STEP)
    )

    user_roles = models.CharField(max_length=31, choices=USER_ROLES , default=ORDINARY_USER)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE_CHOICES)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(null=True, blank=True, upload_to='user_photos',
                              # faqat rasm yuklash uchun validators qo'shildi
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'heic', 'heif'])])

    def __str__(self):
        return self.username

    @property # user.full_name() oxirida qavs qo'ymaslik uchun va kod tozoroq bo'lishi uchun

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    # verify_code ya'ni email yoki telefonga yuboriladigan kodni create qilish uchun
    def create_verify_code(self,verify_type):
        #random orqali murakkabroq logika tahlil qil
        code = "".join([str(random.randint(0,100)%10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type = verify_type,
            code=code,
        )
        return code

    def check_username(self):
        if not self.username:
            # validatsiya(ro'yxatdan o'tish jarayoni)da boshida email yoki nomer orqali tasdiqlaganda , username
            # hali mavjud bo'lmaydi , nomer yoki email tasdiqlagandan keyin username qo'yadi , ungacha tasodifiy username
            # kerak , o'shani create qilish
            temp_username = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}'
            # uuid4 da random username  qlganda bazada saqlangan bo'lish extimoli juda kam
            # moboda o'xshab qosa username o'zgartirish uchun :
            while User.objects.filter(username=temp_username):
                temp_username = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}'
            self.username = temp_username
    def check_email(self):
        # databaseda emailni tekshirish oson bo'lishi uchun
        if self.email:
            normal_email = self.email.lower()
            self.email = normal_email
    def check_pass(self):
        # huddi boyagi kabi agar password bo'lmasa random hosil qilish uchun
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split("-")[-1]}"
            self.password = temp_password
    def hashing_password(self):
        # ma'lumotlar xavsizligi uchun databasega saqlashdan oldin hashlar kerak (aniqroq surishtirish kerak )
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
    def clean(self):
        self.check_username()
        self.check_pass()
        self.check_email()
        self.hashing_password()

    def save(self, *args, **kwargs):
        self.clean()
        super(User,self).save(*args, **kwargs)






PHONE_EXPIRE = 2 # telefonga kod yuborganda necha minut kutishi
EMAIL_EXPIRE = 2 # emailga kod yuborganda necha minut kutishi

class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE , VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )# kod yuborib tasdiqlash uchun qaysi turdagi kirishni amalga oshirishni aniqlash uchun , tel nomer orqalimi yoki email

    code = models.CharField(max_length=4)# bu uchun alohida funksiya yozilgan
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    # user appdagi User modeli bilan onetomany ko'rinishda bog'landi aksincha bog'lash uchun related name ishlatildi
    # models.CASCADE biror user o'chirilda bu modeldagi user ham o'chib ketishi uchun ishlatiladi
    user = models.ForeignKey('users.User', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True) # kodni yaroqlilik muddatini tugash vaqti
    is_confirmed = models.BooleanField(default=False) # kodni tasdiqlasa True bo'ladi also False
    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs): # ma'lumotlarni saqlash uchun funksiya
        # agara yangi object bo'lsa , yani databasega hali saqlanmagan bo'lsa , sharti
        # chunki yangi objectga hali pk berilmaydi faqat databasega saqlansa keyin pk beriladi
        if self.verify_type == VIA_EMAIL:
            # EMAIL orqali akkaunt tasdiqlanayotgan bo'lsa ,
            # kodni yaroqlilik muddatiga 5 daqiqa qo'shyapti
            self.expiration_time = datetime.now()+timedelta(minutes=EMAIL_EXPIRE)
        else:
            # TELEFON orqali akkaunt tasdiqlayotgan bo'lsa ,
            # kodni yaroqlilik muddatiga 2 minut qo'shyapti
            self.expiration_time = datetime.now()+timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)
