import re
import threading
import phonenumbers

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

# email to'g'ri kiritilganini tekshirish uchun regax
email_regax = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# telefon raqam to'g'ri kiritilganini tekshirish uchun regax
phone_regax = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")

#email yoki phone_number ekanligini tekshirish uchun funksiya
def check_email_or_phone(email_or_phone):
    phone_number = phonenumbers.parse(email_or_phone)
    if re.fullmatch(email_regax, email_or_phone):
        email_or_phone = "email"
    elif phonenumbers.is_valid_number(phone_number):
        email_or_phone = "phone"
    else:
        data = {
            "success": False,
            "message": "Invalid Email or Phone Number",
        }
        raise ValidationError(data)

    return email_or_phone


class EmailThread(threading.Thread):
    # aytaylik 1000 ta foydalanuvchi bir vaqtda ro'yxatdan o'tsa 1-foydalanuvchiga birinchi keyin 2 chisiga
    # keyin 3 chisiga qilmasdan hammasiga bir vaqtda kode jo'natadi
    # ya'ni asosiy dasturni to'xtatmasdan o'zi ham unga paralel ishlovradi
    def __init__(self, email):
        # emailni registratsiya qilish uchun
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send()

class Email:
    # EmailThreadni ishlatish va emailni jo'natish uchun ishlatiladi
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            to=[data["to_email"]],
        )
        if data.get('content_type')=='html':
            email.content_subtype = 'html'
        EmailThread(email).start()


# email va codeni olib Email classi orqali emailga jo'natadi
def send_mail(email, code):
    # render to string orqali activate_account.html fayliga codeni qo'shib html_contentga o'girib beryapti
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {"code": code},
    )

    # Email classi ichidagi send_email funksiyasiga data yuborish uchun ishlatidi
    Email.send_email(
        {
            "subject": "Ro'yxatdan o'tish",
            "to_email": email,
            "body": html_content,
            "content_type": "html",
        }
    )
