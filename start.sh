#!/usr/bin/env bash
# سكربت التشغيل على Render — يهيّئ قاعدة البيانات ثم يشغّل السيرفر
set -o errexit

python manage.py migrate --no-input
python manage.py seed_menu

exec gunicorn restaurant.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
