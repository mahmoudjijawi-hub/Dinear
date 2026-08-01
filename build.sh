#!/usr/bin/env bash
# سكربت البناء لـ Render
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py seed_menu
