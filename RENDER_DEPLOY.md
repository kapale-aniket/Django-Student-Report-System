# Deploy on Render

## Build Command (must include demo user creation)
Use one of these so demo users are created during build:

```bash
./build.sh
```

If you get "Permission denied", use:

```bash
chmod +x build.sh && ./build.sh
```

Or run the steps explicitly:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_demo_users
```

## Start Command
Use one of these so demo users exist even if build skipped them:

```bash
./start.sh
```

Or:

```bash
bash start.sh
```

Or inline (same behavior):

```bash
python manage.py create_demo_users || true && gunicorn student_report_system.wsgi:application --bind 0.0.0.0:$PORT
```

## Demo login (after deploy)
- **Admin:** `admin1` / `demo123`
- **Evaluator:** `evaluator1` / `demo123`
- **Student:** `student1` / `demo123`
