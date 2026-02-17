#!/usr/bin/env bash
# Run at service start so demo users exist (even if build didn't run create_demo_users)
set -e
python manage.py create_demo_users || true
exec gunicorn student_report_system.wsgi:application --bind 0.0.0.0:${PORT:-10000}
