"""
إعدادات مشروع مطعم Dinear
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-dev-key-change-in-production',
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

_allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
_allowed_hosts.append('dinear-j7hu.onrender.com')
# السماح بنطاقات Cursor Cloud أثناء التطوير وRender في الإنتاج
if DEBUG:
    _allowed_hosts.extend(['.cursorvm.com', '.agent.cvm.dev'])
_allowed_hosts.append('.onrender.com')
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts if h.strip()]

# أصول موثوقة لـ CSRF (للإنتاج أو عبر متغير بيئة)
_csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(',') if o.strip()]
# نطاقات Render الافتراضية
CSRF_TRUSTED_ORIGINS += [
    'https://dinear-j7hu.onrender.com',
    'https://.onrender.com',
]
if DEBUG:
    CSRF_TRUSTED_ORIGINS += [
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'https://.cursorvm.com',
        'https://.agent.cvm.dev',
    ]

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# إعدادات البروكسي والكوكيز
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

if DEBUG:
    # تطوير محلي / Cursor Cloud
    SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_HTTPONLY = False
else:
    # إنتاج Render (HTTPS)
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menu',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'restaurant.middleware.CloudDevCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'restaurant.middleware.DashboardAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'restaurant.middleware.IngressTokenMiddleware',
]

ROOT_URLCONF = 'restaurant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'menu.context_processors.dashboard_tokens',
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurant.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/dashboard/login/'
