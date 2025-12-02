# 🚨 URGENT: Fix Gmail Email Error NOW

## ❌ Current Error:
```
535, b'5.7.8 Username and Password not accepted. For more information, go to
5.7.8 https://support.google.com/mail/?p=BadCredentials
```

**This means Gmail is rejecting your password. You MUST use an App Password!**

---

## ⚡ QUICK FIX (5 Minutes):

### 1️⃣ Enable 2-Step Verification
**Link:** https://myaccount.google.com/security

1. Click **"2-Step Verification"**
2. Click **"Get started"**
3. Follow the steps (you'll need your phone)

### 2️⃣ Create App Password
**Link:** https://myaccount.google.com/apppasswords

1. Select **App:** `Mail`
2. Select **Device:** `Other (Custom name)`
3. Enter name: `Student Report System`
4. Click **"Generate"**
5. **COPY THE 16-CHARACTER PASSWORD** (you'll only see it once!)

### 3️⃣ Update .env File

Open `.env` file and change:

**FROM:**
```env
EMAIL_HOST_PASSWORD=Aniket@9096
```

**TO:**
```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```
*(Replace with your actual 16-character App Password - no spaces!)*

### 4️⃣ Restart Server

```bash
# Stop server (Ctrl+C)
python manage.py runserver
```

### 5️⃣ Test Email

Run this command to test:
```bash
python test_email.py
```

---

## ✅ What Happens After Fix:

- ✅ Admin creates Evaluator → Email sent to evaluator
- ✅ Evaluator creates Student → Email sent to student  
- ✅ All credentials delivered via email automatically

---

## 🔍 Verify Your Setup:

**Current email:** `aniketkapale2002@gmail.com` ✅

**Current password:** `Aniket@9096` ❌ (Gmail rejects this)

**You need:** 16-character App Password ✅

---

## 📋 Checklist:

- [ ] 2-Step Verification enabled
- [ ] App Password generated (16 characters)
- [ ] `.env` file updated with App Password
- [ ] Django server restarted
- [ ] Test email sent successfully

---

## 🆘 Still Not Working?

1. **Check .env file:**
   ```bash
   # View email settings
   Get-Content .env | Select-String -Pattern "EMAIL"
   ```

2. **Verify App Password:**
   - Should be 16 characters
   - No spaces
   - No special characters like @

3. **Test email configuration:**
   ```bash
   python test_email.py
   ```

4. **Check logs:**
   - Look in `logs/errors.log` for detailed error messages

---

**Follow these steps and your emails will work!** ✉️✅



