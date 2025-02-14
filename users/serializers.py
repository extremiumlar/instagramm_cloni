from shared.utility import check_email_or_phone
from .models import User, UserConfirmation, VIA_EMAIL , VIA_PHONE, NEW , CODE_VERIFIED , DONE, PHOTO_STEP
from rest_framework import exceptions
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
        print(user)
        if user.auth_type==VIA_EMAIL:
            code = user.create_verify_code(verify_type=VIA_EMAIL)
            print(code)
            send_mail(user.email, code)
        elif user.auth_type==VIA_PHONE:
            code = user.create_verify_code(verify_type=VIA_PHONE)
            send_phone_code(user.phone_number, code)
        user.save()
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
        print("data", data)
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
        # to do keyinchalik
        return value
