from shared.utility import check_email_or_phone
from .models import User, UserConfirmation, VIA_EMAIL , VIA_PHONE, NEW , CODE_VERIFIED , DONE, PHOTO_STEP
from rest_framework import exceptions
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class SignupSerializer(serializers.ModelSerializer):
    #read_only =True faqat get so'rovi uchun ishlaydi . Post va put uchun ishlamaydi .
    id = serializers.UUIDField(read_only=True)

    def __init__(self,*args,**kwargs):
        #super qilish orqali SignupSerializerni o'zini qaytadan chaqirvolayapmiz
        super(SignupSerializer,self).__init__(*args,**kwargs)
        # modelda yo'q fieldni qo'shish uchun kerak
        self.fields['email_phone_number']=serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'auth_type',
            'auth_status',
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
    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_email_or_phone(user_input)
        print(user_input)
        print(input_type)
        return data