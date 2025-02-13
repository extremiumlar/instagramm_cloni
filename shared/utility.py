import re

from rest_framework.exceptions import ValidationError

# email to'g'ri kiritilganini tekshirish uchun regax
email_regax = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# telefon raqam to'g'ri kiritilganini tekshirish uchun regax
phone_regax = re.compile(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$")

#email yoki phone_number ekanligini tekshirish uchun funksiya
def check_email_or_phone(email_or_phone):
    if re.fullmatch(email_regax, email_or_phone):
        email_or_phone = "email"
    elif re.fullmatch(phone_regax, email_or_phone):
        email_or_phone = "phone"
    else:
        data = {
            "success": False,
            "message": "Invalid Email or Phone Number",
        }
        raise ValidationError(data)

    return email_or_phone
