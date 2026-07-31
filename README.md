# Dinear - مطعم إلكتروني

موقع مطعم إلكتروني كامل بواجهة عربية (RTL) مبني بـ Django، يتضمن منيو تفاعلي، سلة طلبات، ولوحة تحكم لصاحب المطعم.

## المميزات

- منيو مقسم لأقسام (مقبلات، سلطات، أطباق رئيسية، مشروبات، حلويات)
- سلة تسوق تفاعلية (Vanilla JS) مع عداد كمية
- سلة جانبية على الديسكتوب وشريط ثابت على الموبايل
- تأكيد الطلب مع نافذة ملخص
- لوحة تحكم لصاحب المطعم (تسجيل دخول + إدارة الطلبات)
- تصميم متجاوب بالكامل مع دعم RTL

## المتطلبات

- Python 3.10+
- PostgreSQL 14+

## التثبيت والتشغيل

### 1. إعداد PostgreSQL

```bash
# إنشاء مستخدم وقاعدة بيانات
sudo -u postgres psql
CREATE USER restaurant WITH PASSWORD 'restaurant123';
CREATE DATABASE restaurant_db OWNER restaurant;
\q
```

### 2. إعداد المشروع

```bash
# إنشاء بيئة افتراضية وتثبيت المتطلبات
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# تطبيق migrations
python manage.py migrate

# تعبئة البيانات الأولية (المنيو + مستخدم المدير)
python manage.py seed_menu
```

### 3. تشغيل السيرفر

```bash
python manage.py runserver
```

افتح المتصفح على: http://127.0.0.1:8000/

## بيانات الدخول

| الحساب | اسم المستخدم | كلمة المرور |
|--------|-------------|-------------|
| لوحة التحكم | `admin` | `admin123` |
| Django Admin | `admin` | `admin123` |

## الروابط

| الصفحة | الرابط |
|--------|--------|
| المنيو | `/` |
| تسجيل الدخول | `/dashboard/login/` |
| الطلبات الواردة | `/dashboard/orders/` |
| Django Admin | `/admin/` |

## متغيرات البيئة (اختياري)

| المتغير | القيمة الافتراضية |
|---------|-------------------|
| `DB_NAME` | `restaurant_db` |
| `DB_USER` | `restaurant` |
| `DB_PASSWORD` | `restaurant123` |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `5432` |
| `DJANGO_SECRET_KEY` | مفتاح تطوير |
| `DJANGO_DEBUG` | `True` |

## هيكلة المشروع

```
restaurant/
├── restaurant/           # إعدادات المشروع
├── menu/                 # تطبيق المنيو والطلبات
│   ├── models.py         # Category, Product, Order, OrderItem
│   ├── views.py          # عرض المنيو + API الطلبات + لوحة التحكم
│   ├── templates/        # قوالب HTML
│   └── management/       # أوامر إدارة (seed_menu)
├── static/
│   ├── css/              # ملفات التصميم
│   └── js/               # cart.js, dashboard.js
└── requirements.txt
```

## التقنيات المستخدمة

- **Backend:** Django 6 (Templates + JsonResponse)
- **Database:** PostgreSQL
- **Frontend:** HTML + CSS + Vanilla JavaScript
- **Auth:** django.contrib.auth
