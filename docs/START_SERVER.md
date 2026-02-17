# 🚀 HOW TO START THE SERVER

## ❌ Error: "Connection Refused"
**This means the Django server is not running.**

## ✅ Solution: Start the Server

### Method 1: Using Command Prompt/Terminal

1. **Open Command Prompt or Terminal**
2. **Navigate to project directory:**
   ```bash
   cd D:\django\Django-Student-Report-System
   ```

3. **Start the server:**
   ```bash
   python manage.py runserver
   ```

4. **Wait for this message:**
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

5. **Open browser and go to:**
   ```
   http://127.0.0.1:8000/
   ```

---

## 🔍 Troubleshooting

### If Server Won't Start:

#### 1. **Check if Port 8000 is Already in Use**
```bash
netstat -an | findstr ":8000"
```
If something is using port 8000, either:
- Stop that application, OR
- Use a different port:
  ```bash
  python manage.py runserver 8001
  ```
  Then access: `http://127.0.0.1:8001/`

#### 2. **Check Python Installation**
```bash
python --version
```
Should show Python 3.x

#### 3. **Check if Django is Installed**
```bash
python -m django --version
```

#### 4. **Check Database Connection**
If you get database errors:
```bash
python manage.py migrate
```

---

## 📋 Quick Start Steps

1. ✅ Open terminal/command prompt
2. ✅ Go to project folder: `cd D:\django\Django-Student-Report-System`
3. ✅ Run: `python manage.py runserver`
4. ✅ Wait for: "Starting development server..."
5. ✅ Open browser: `http://127.0.0.1:8000/`

---

## ⚠️ Important Notes

- **Keep the terminal open** - Closing it will stop the server
- **Server runs until you stop it** - Press `Ctrl+C` to stop
- **Don't close terminal window** - Server needs it to run

---

## 🎯 After Server Starts

Once you see:
```
Starting development server at http://127.0.0.1:8000/
```

You can:
- ✅ Access home page: `http://127.0.0.1:8000/`
- ✅ Login to the system
- ✅ Test all features

---

**The server must be running for the website to work!**

