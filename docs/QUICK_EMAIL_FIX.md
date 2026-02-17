# ⚡ QUICK EMAIL FIX - Gmail App Password Setup

## 🔴 Current Error:
```
535, b'5.7.8 Username and Password not accepted. For more information, go to
5.7.8 https://support.google.com/mail/?p=BadCredentials
```

**Gmail requires an App Password, not your regular password!**

---

## 🚀 Quick Fix (5 Minutes):

### 1. Enable 2-Step Verification
- Go to: https://myaccount.google.com/security
- Enable **"2-Step Verification"**

### 2. Create App Password
- Go to: https://myaccount.google.com/apppasswords
- Select: **App = Mail**, **Device = Other (Custom name)**
- Enter name: `Student Report System`
- Click **"Generate"**
- **COPY THE 16-CHARACTER PASSWORD** (you'll only see it once!)

### 3. Update .env File
Open `.env` and replace:
```env
EMAIL_HOST_PASSWORD=YOUR_16_CHARACTER_APP_PASSWORD_HERE
```

### 4. Restart Server
```bash
python manage.py runserver
```

**Done! ✅ Emails will now work.**

---

## 📧 Your Current Configuration:

Current email in `.env`:
- `EMAIL_HOST_USER=aniketkapale2002@gmail.com`
- `EMAIL_HOST_PASSWORD=Aniket@9096` ← **THIS NEEDS TO BE APP PASSWORD**

**Steps:**
1. Create App Password for `aniketkapale2002@gmail.com`
2. Replace `Aniket@9096` with the 16-character App Password
3. Save `.env` and restart server

---

## 📖 Full Guide:
See `GMAIL_SETUP_GUIDE.md` for detailed step-by-step instructions with screenshots.

---

**After this fix, all emails will send successfully when:**
- ✅ Admin creates evaluator
- ✅ Evaluator creates student
- ✅ Student self-registers
- ✅ Password reset requested




