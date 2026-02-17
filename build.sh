#!/usr/bin/env bash
set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Running migrations..."
python manage.py migrate

echo "==> Creating demo users..."
python manage.py create_demo_users

echo "==> Build completed successfully!"
