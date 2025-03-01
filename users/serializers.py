from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from rest_framework.generics import get_object_or_404
# from django.db.models.query import ValuesIterable
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken

# from rest_framework_simplejwt.views import TokenObtainPairView

from shared.utility import check_email_or_phone, check_user_type
from .models import User, UserConfirmation, VIA_EMAIL , VIA_PHONE, NEW , CODE_VERIFIED , DONE, PHOTO_DONE
# from rest_framework import exceptions
# from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from shared.utility import send_mail



class SignupSerializer(serializers.ModelSerializer):
    #read_only =True faqat get so'rovi uchun ishlaydi . Post va put uchun ishlamaydi .
    id = serializers.UUIDField(read_only=True)

    def __init__(self,*args,**kwargs):
        #super qilish orqali SignupSerializerni o'zini qaytadan chaqirvolayapmiz
        super(SignupSerializer,self).__init__(*args,**kwargs)
        # modelda yo'q fieldni postman orqali (api orqali) qo'shish uchun funksiya bu
        self.fields['email_phone_number']=serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'auth_type',
            'auth_status',
            # 'user_roles',
        )
        extra_kwargs = {
            # read only kiritilishi shart emas , avtomatik olamiz faqat get so'rovi ishlaydi , tahrirlash va o'chirish ishlamaydi
            # required =false bu maydon majburiy emas , post va put so'rovlarini jo'natmasa ham bo'ladi degani
            # auth_type = serializers.CharField(read_only=True, required=False) qilib idni tagidan ham yossa bo'ladi
            'auth_type': {'required': False,'read_only' : True},
            'auth_status': {'required': False, 'read_only' : True},
        }

    def validate(self,data):
        super(SignupSerializer,self).validate(data)
        data = self.auth_validate(data)
        return data
    def create(self,validate_data):
        # validatsiyadan o'tgan ma'lumotni olib yangi user yaratib o'zgaruvchiga saqlayapti databasega saqlanmayapti lekin
        user = super(SignupSerializer,self).create(validate_data)
        # print(user)
        if user.auth_type==VIA_EMAIL:
            code = user.create_verify_code(verify_type=VIA_EMAIL)
            # print(code)
            send_mail(user.email, code)
        elif user.auth_type==VIA_PHONE:
            code = user.create_verify_code(verify_type=VIA_PHONE)
            # send_phone_code(user.phone_number, code)
            send_mail(user.phone_number, code)
        user.save()

        return user
    @staticmethod
    def auth_validate(data):
        # print(data)
        # postman orqali jo'natilagan email_phone_number o'zgaruvchisini user_inputga biriktiramiz
        user_input = str(data.get('email_phone_number')).lower()
        # check_email_or_phone funksiyasi bor tekshirish uchun ,
        input_type = check_email_or_phone(user_input)
        # print(user_input)
        # print(input_type)
        if input_type == 'email':
            data = {
                "email": user_input,
                "auth_type": VIA_EMAIL,
            }
        elif input_type == 'phone':
            data = {
                "phone_number": user_input,
                "auth_type": VIA_PHONE,
            }
        else :
            data = {
                "success": False,
                "message": "Invalid Email or Phone Number",
            }
            raise ValidationError(data)
        # print("data", data)
        '''
        {
            "id": "204ae766-e52d-44bf-ba64-6edaa9b9d89d",
            "auth_type": "via_email",
            "auth_status": "new"
        }
        return data qigandagi natija qaytargani Meta classini ichidag yozilgan fieldlar qaytararkan
        '''
        return data
    def validate_email_phone_number(self,value):
        value = value.lower()
        if value and User.objects.filter(email=value).exists():
            data = {
                "success": False,
                "message": "Bu email allaqachon ishlatilgan",
            }
            raise ValidationError(data)
        elif value and User.objects.filter(phone_number=value).exists():
            data = {
                "success": False,
                "message": "Bu telefon raqami allaqachon ishlatilgan",
            }
            raise ValidationError(data)
        return value
    def to_representation(self, instance):
        # tokenni ham colsolegan qaytarish uchun funksiya
        # print(instance)
        data = super(SignupSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data

class ChangeUserInformation(serializers.Serializer):
    #required=True kiritish majburiy maydon
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self,data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        if password != confirm_password:
            raise ValidationError(
                {
                    "message": "Parolilingiz bir biriga mos emas "
                }
            )

        if password:
            #parolni avtomatik validatsiya qiladi tayyor validate orqali
            validate_password(password)
        return data
    def validate_username(self,username):
        # parolni validatsiya qilish uchun qo'lda yozilgan shartlar
        if len(username) < 5 or len(username)>30:
            raise ValidationError(
                {
                    "message": "Username must be between 5 and 30 characters long"
                }
            )
        if username.isdigit():
            raise ValidationError(
                {
                    "message": "This username is entirely numeric"
                }
            )

        # databasedagi username bilan bir xil bo'lib qolmasligini tekshirish uchun
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                {
                    "message": "This username is already taken"
                }
            )
        return username
    def validate_first_name(self,first_name):
        if len(first_name) < 5 or len(first_name)>30:
            raise ValidationError(
                {
                    "message": "First name must be between 5 and 30 characters long"
                }
            )
        if first_name.isdigit():
            raise ValidationError(
                {
                    "message": "This username is entirely numeric"
                }
            )
        return first_name
    def validate_last_name(self,last_name):
        if len(last_name) < 5 or len(last_name)>30:
            raise ValidationError(
                {
                    "message": "Last name must be between 5 and 30 characters long"
                }
            )
        if last_name.isdigit():
            raise ValidationError(
                {
                    "message": "This username is entirely numeric"
                }
            )
        return last_name
    def update(self,instance,validated_data):
        #databazadagi ma'lumotlarni yangilash uchun funksiya

        #username modelidagi firs_name to'ldirilayapti
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        if validated_data.get('password'):
            # passwordni set_password yordamida databasega heshlab joylayapti
            instance.set_password(validated_data.get('password'))
        if instance.auth_status==CODE_VERIFIED:
            instance.auth_status=DONE
        instance.save()
        return instance

class ChangeUserPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=[
            "jpg", "jpeg", "png", 'heic', 'heif'
        ])],
    )
    def update(self,instance,validated_data):
        photo = validated_data.get('photo')
        if photo:
            instance.photo = photo
            instance.auth_status = PHOTO_DONE
            instance.save()
        return instance

class LoginSerializer(TokenObtainPairSerializer):

    def __init__(self,*args,**kwargs):
        super(LoginSerializer,self).__init__(*args,**kwargs)
        self.fields['userinput'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(required=False, read_only=True)
    def auth_validate(self,data):
        user_input = data.get('userinput')
        if check_user_type(user_input)=='username':
            username = user_input
        elif check_user_type(user_input)=='email':
            user = self.get_user(email=user_input)
            username = user.username
        elif check_user_type(user_input)=='phone':
            user = self.get_user(phone=user_input)
            username = user.username
        else :
            data = {
                "success": False,
                'message': "Siz email, username yoki telefon raqam kiritishingiz kerak "
            }
            raise ValidationError(data)
        authentication_kwargs = {
            self.username_field: username,
            'password': data['password'],
        }

        current_user = User.objects.filter(username=username).first()
        if current_user is not None and current_user.auth_status in [CODE_VERIFIED, NEW]:
            raise ValidationError(
                {
                    "success": False,
                    "message": "Siz ro'yxatdan to'liq o'tmagansiz !"
                }
            )

        user = authenticate(**authentication_kwargs)
        # print(**authentication_kwargs)
        if user is not None:
            self.user = user
        else :
            raise ValidationError(
                {
                    "success": False,
                    "message": "Kechirasiz login yoki parol xato . Iltimos tekshirib qaytadan kring !"
                }
            )

    def validate(self,data):
        self.auth_validate(data)
        if self.user.auth_status not in [DONE, PHOTO_DONE]:
            raise PermissionDenied("Siz login qila olmaysiz , ruxstatingiz yo'q ")
        data = self.user.token()
        data['auth_status']=self.user.auth_status
        data['full_name']=self.user.full_name
        return data





    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError(
                {
                    "message": "Foydalanuvchi topilmadi "
                }
            )
        return users.first()

class LoginRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id = user_id)
        update_last_login(None, user)
        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()












