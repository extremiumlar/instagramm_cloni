# Instagram Clone — Django REST API

Instagram'ning backend qismi: foydalanuvchilar, postlar, kommentlar (javob-kommentlar bilan),
like tizimi. Django REST Framework'da yozilgan o'quv-portfolio loyihasi.

## Asosiy imkoniyatlar

- Foydalanuvchi ro'yxatdan o'tishi va autentifikatsiya
- Post yaratish (rasm + caption, fayl turi validatsiyasi)
- Kommentlar va **nested** javoblar (`parent` orqali komment ichida komment)
- Post va komment uchun like/unlike
- **1 foydalanuvchi — 1 like** qoidasi baza darajasida: `UniqueConstraint(author, post)` —
  parallel so'rovda ham ikkita like yaratib bo'lmaydi

## Texnologiyalar

- Python, Django, Django REST Framework
- PostgreSQL (sozlamalar `.env` orqali)
- Pipenv

## Loyiha tuzilishi

```
config/    — Django sozlamalari va asosiy urls
users/     — foydalanuvchilar (custom User, auth)
postlar/   — postlar, kommentlar, like'lar (UniqueConstraint bilan)
shared/    — BaseModel (UUID id, created_at kabi umumiy maydonlar)
```

## Ishga tushirish

```bash
pipenv install
# .env faylida DB sozlamalarini to'ldiring (PostgreSQL)
python manage.py migrate
python manage.py runserver
```

## Nima uchun bu loyiha muhim

Bu yerdagi `UniqueConstraint` yondashuvi — "bir amal faqat bir marta" talabining to'g'ri
yechimi: tekshiruv faqat kodda emas, **ma'lumotlar bazasi darajasida** kafolatlanadi.
Xuddi shu mexanika bir martalik promo-kod/QR aktivatsiyasi kabi masalalarda ishlatiladi.
