# 📧 Gmail SMTP Setup Guide - FIX Email Authentication Error

## 🔴 Problem:
Error: `535, b'5.7.8 Username and Password not accepted. For more information, go to\n5.7.8 https://support.google.com/mail/?p=BadCredentials`

**This happens because Gmail no longer accepts regular passwords for SMTP authentication. You MUST use an App Password.**

---

## ✅ Solution: Create a Gmail App Password

### Step 1: Enable 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** (left sidebar)
3. Scroll down to **"2-Step Verification"**
4. Click **"Get started"** or **"Turn on"**
5. Follow the prompts to enable 2-Step Verification
   - You'll need your phone number
   - Google will send a verification code
   - Enter the code to verify

**⚠️ IMPORTANT:** You MUST enable 2-Step Verification before you can create an App Password!

---

### Step 2: Create an App Password

1. Go back to **Google Account → Security**
2. Scroll down to **"2-Step Verification"** section
3. Click on **"App passwords"** (at the bottom of 2-Step Verification section)
   - If you don't see "App passwords", make sure 2-Step Verification is enabled first!

4. You may need to sign in again for security

5. In the **"Select app"** dropdown, choose **"Mail"**

6. In the **"Select device"** dropdown, choose **"Other (Custom name)"**
   - Enter: `Student Report System` or `Django App`

7. Click **"Generate"**

8. **📋 COPY THE 16-CHARACTER PASSWORD IMMEDIATELY!**
   - It will look like: `abcd efgh ijkl mnop` (with spaces)
   - Or: `abcdefghijklmnop` (without spaces)
   - **⚠️ You can only see this password ONCE! Save it immediately!**

---

### Step 3: Update Your .env File

1. Open your `.env` file in the project root

2. Replace the `EMAIL_HOST_PASSWORD` with your **App Password**:

   **BEFORE:**
   ```
   EMAIL_HOST_PASSWORD=Aniket@9096
   ```

   **AFTER:**
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   (Use the 16-character App Password - remove spaces if any)

3. **Keep the email address the same:**
   ```
   EMAIL_HOST_USER=aniketkapale2002@gmail.com
   DEFAULT_FROM_EMAIL=aniketkapale2002@gmail.com
   ```

4. Save the `.env` file

---

### Step 4: Restart Your Django Server

1. Stop your Django server (Ctrl+C)
2. Start it again:
   ```bash
   python manage.py runserver
   ```

---

### Step 5: Test Email Sending

1. Try creating a new evaluator or student
2. The email should now be sent successfully!

---

## 📝 Complete .env Email Configuration

```env
# Email Configuration - SMTP Enabled
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=aniketkapale2002@gmail.com
EMAIL_HOST_PASSWORD=YOUR_16_CHARACTER_APP_PASSWORD_HERE
DEFAULT_FROM_EMAIL=aniketkapale2002@gmail.com
SITE_URL=http://127.0.0.1:8000
```

---

## 🔍 Troubleshooting

### Issue: "App passwords" option not visible
**Solution:** Make sure 2-Step Verification is enabled first. The "App passwords" option only appears after 2-Step Verification is turned on.

### Issue: Still getting authentication error
**Solutions:**
1. Make sure you're using the **App Password**, not your regular Gmail password
2. Remove any spaces from the App Password
3. Check that `EMAIL_HOST_USER` matches your Gmail address exactly
4. Restart your Django server after updating `.env`

### Issue: "Less secure app access" 
**Note:** Gmail no longer supports "Less secure app access". You MUST use App Passwords with 2-Step Verification enabled.

---

## ✅ When Emails Are Sent:

1. **Evaluator Created by Admin:**
   - Email sent to evaluator's email address
   - Contains: Username, Password, Login URL

2. **Student Created by Evaluator:**
   - Email sent to student's email address
   - Contains: Username, Password, Login URL

3. **Student Self-Registration:**
   - Confirmation email sent
   - Approval notification email sent after evaluator approves

4. **Password Reset:**
   - Password reset email sent via SMTP

---

## 🔐 Security Notes:

- ✅ App Passwords are secure - they're separate from your main password
- ✅ You can revoke App Passwords anytime from Google Account settings
- ✅ App Passwords work only for the specific app (Django in this case)
- ✅ Your main Gmail password remains unchanged

---

## 📞 Need Help?

If you continue to have issues:
1. Check that 2-Step Verification is enabled
2. Verify the App Password was copied correctly (no spaces)
3. Check `.env` file has the correct App Password
4. Restart Django server after changes
5. Check Django logs for detailed error messages

---

**After setting up the App Password, email sending will work perfectly!** ✉️✅




