# 🔧 SIMPLE EMAIL FIX - Gmail App Password

## ❌ Your Error:
```
535, b'5.7.8 Username and Password not accepted
```

**Gmail is rejecting your password `Aniket@9096` because it's not an App Password!**

---

## ✅ FIX IN 3 STEPS:

### STEP 1: Get Gmail App Password

1. **Go to:** https://myaccount.google.com/apppasswords
   - (If link doesn't work, go to: https://myaccount.google.com/security → 2-Step Verification → App passwords)

2. **If you see "2-Step Verification is off":**
   - Click "Turn on" first
   - Follow the steps (needs your phone)

3. **Create App Password:**
   - Select: **App = Mail**
   - Select: **Device = Other (Custom name)**
   - Type: `Django App`
   - Click **"Generate"**

4. **COPY THE 16-CHARACTER PASSWORD!**
   - Example: `abcd efgh ijkl mnop`
   - Remove spaces: `abcdefghijklmnop`
   - **⚠️ YOU'LL ONLY SEE THIS ONCE!**

---

### STEP 2: Update .env File

1. Open `.env` file in your project

2. Find this line:
   ```
   EMAIL_HOST_PASSWORD=Aniket@9096
   ```

3. Replace with your App Password:
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   *(Use your actual 16-character App Password)*

4. **Save the file**

---

### STEP 3: Restart Server

1. Stop your Django server (press `Ctrl+C`)

2. Start it again:
   ```bash
   python manage.py runserver
   ```

---

## ✅ DONE!

Now when you:
- ✅ Create an evaluator → Email sent automatically
- ✅ Create a student → Email sent automatically

**All credentials will be sent via email!** 📧

---

## 🔍 Quick Check:

**Your current .env should have:**
```env
EMAIL_HOST_USER=aniketkapale2002@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password_here  ← Must be App Password!
```

**NOT:**
```env
EMAIL_HOST_PASSWORD=Aniket@9096  ← This won't work!
```

---

## 🆘 Still Not Working?

1. Make sure 2-Step Verification is ON
2. Make sure you're using the 16-character App Password (not regular password)
3. Remove any spaces from the App Password
4. Restart Django server after updating .env

---

**That's it! Follow these 3 steps and emails will work.** ✉️✅



