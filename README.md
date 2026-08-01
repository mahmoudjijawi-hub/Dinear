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

## التثبيت والتشغيل

```bash
# إنشاء بيئة افتراضية وتثبيت المتطلبات
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# تطبيق migrations (ينشئ db.sqlite3 تلقائياً)
python manage.py migrate

# تعبئة البيانات الأولية (المنيو + مستخدم المدير)
python manage.py seed_menu

# تشغيل السيرفر
python manage.py runserver
```

افتح المتصفح على: http://127.0.0.1:8000/

## النشر على Render

1. أنشئ **Web Service** جديد واربطه بالمستودع
2. **Build Command:**
   ```bash
   ./build.sh
   ```
3. **Start Command:**
   ```bash
   gunicorn restaurant.wsgi:application
   ```
4. أضف متغيرات البيئة:
   - `DJANGO_DEBUG=False`
   - `DJANGO_SECRET_KEY` — مفتاح سري عشوائي
   - `DJANGO_ALLOWED_HOSTS` — نطاق Render (مثل: `your-app.onrender.com`)
   - `CSRF_TRUSTED_ORIGINS` — `https://your-app.onrender.com`

> يتم جمع الملفات الثابتة تلقائياً عبر `collectstatic` في `build.sh`، وتُخدم عبر **WhiteNoise**.

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
- **Database:** SQLite3
- **Static Files:** WhiteNoise
- **Frontend:** HTML + CSS + Vanilla JavaScript
- **Auth:** django.contrib.auth
