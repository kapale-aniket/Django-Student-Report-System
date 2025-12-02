# 📧 EMAIL ERROR FIX - Gmail Authentication Issue

## ❌ Error You're Seeing:

```
Evaluator 'bapu' created, but email could not be sent.
Email error: (535, b'5.7.8 Username and Password not accepted. For more information, go to\n5.7.8 https://support.google.com/mail/?p=BadCredentials')
```

## 🔍 Root Cause:

Gmail no longer accepts regular passwords for SMTP authentication. You **MUST** use a **Gmail App Password** instead.

**Your current password:** `Aniket@9096` ❌ (Gmail rejects this)
**You need:** A 16-character App Password ✅

---

## ✅ SOLUTION - 3 Simple Steps:

### Step 1: Enable 2-Step Verification (Required First!)

1. Go to: **https://myaccount.google.com/security**
2. Find **"2-Step Verification"** section
3. Click **"Turn on"** or **"Get started"**
4. Follow prompts (you'll need your phone)

**⚠️ IMPORTANT:** You CANNOT create an App Password without 2-Step Verification enabled!

---

### Step 2: Generate Gmail App Password

1. Go to: **https://myaccount.google.com/apppasswords**
   - (Or: Google Account → Security → 2-Step Verification → App passwords)

2. Select:
   - **App:** Mail
   - **Device:** Other (Custom name)
   - **Name:** `Student Report System`

3. Click **"Generate"**

4. **📋 COPY THE 16-CHARACTER PASSWORD!**
   - Example: `abcd efgh ijkl mnop`
   - Remove spaces: `abcdefghijklmnop`
   - **⚠️ YOU'LL ONLY SEE THIS ONCE!**

---

### Step 3: Update Your .env File

1. Open `.env` file in your project root

2. Find this line:
   ```
   EMAIL_HOST_PASSWORD=Aniket@9096
   ```

3. Replace with your App Password:
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   (Use your actual 16-character App Password, no spaces)

4. Save the file

5. **Restart your Django server:**
   ```bash
   # Stop server (Ctrl+C)
   # Start again:
   python manage.py runserver
   ```

---

## ✅ After Fix:

**When Admin creates Evaluator:**
- ✅ Email sent automatically to evaluator's email
- ✅ Credentials included in email

**When Evaluator creates Student:**
- ✅ Email sent automatically to student's email
- ✅ Credentials included in email

**All emails will work!** 📧✨

---

## 📋 Your Current Configuration:

**Email Address:** `aniketkapale2002@gmail.com` ✅ (Keep this)
**Password:** `Aniket@9096` ❌ (Replace with App Password)

---

## 🔗 Quick Links:

- **Enable 2-Step Verification:** https://myaccount.google.com/security
- **Generate App Password:** https://myaccount.google.com/apppasswords
- **Full Detailed Guide:** See `GMAIL_SETUP_GUIDE.md`

---

## 🆘 Still Having Issues?

1. ✅ Make sure 2-Step Verification is enabled
2. ✅ Verify you're using App Password (16 characters, not your regular password)
3. ✅ Check `.env` file has correct App Password (no spaces)
4. ✅ Restart Django server after updating `.env`
5. ✅ Make sure email matches: `aniketkapale2002@gmail.com`

---

**Follow these 3 steps and emails will work perfectly!** 🚀




