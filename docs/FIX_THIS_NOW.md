# 🚨 FIX EMAIL ERROR - DO THIS NOW

## ❌ You're Still Getting This Error:
```
535, b'5.7.8 Username and Password not accepted
```

**This means your `.env` file still has the wrong password!**

---

## ✅ DO THESE 4 STEPS RIGHT NOW:

### ⚡ STEP 1: Open This Link
**https://myaccount.google.com/apppasswords**

If you see "2-Step Verification is off":
- Click "Turn on" first
- Follow the steps (needs your phone)

---

### ⚡ STEP 2: Create App Password

1. On the App Passwords page:
   - **Select app:** Choose `Mail`
   - **Select device:** Choose `Other (Custom name)`
   - **Type name:** `Django App`
   - Click **"Generate"**

2. **COPY THE 16-CHARACTER PASSWORD!**
   - It looks like: `abcd efgh ijkl mnop`
   - Remove spaces: `abcdefghijklmnop`
   - **⚠️ YOU'LL ONLY SEE THIS ONCE!**

---

### ⚡ STEP 3: Edit .env File

1. Open this file: `D:\django\Django-Student-Report-System\.env`

2. Find this line:
   ```
   EMAIL_HOST_PASSWORD=Aniket@9096
   ```

3. **REPLACE IT** with:
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   *(Use your actual 16-character App Password from Step 2)*

4. **SAVE THE FILE** (Ctrl+S)

---

### ⚡ STEP 4: Restart Server

1. In your terminal, press **Ctrl+C** to stop the server

2. Start it again:
   ```bash
   python manage.py runserver
   ```

---

## ✅ DONE! Test It:

1. Create a new evaluator or student
2. Email should send successfully! ✅

---

## 🔍 Verify It Worked:

**Before (WRONG):**
```env
EMAIL_HOST_PASSWORD=Aniket@9096  ❌
```

**After (CORRECT):**
```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop  ✅
```
*(16 characters, no @ symbol, no spaces)*

---

## 🆘 Still Not Working?

1. **Check .env file:**
   - Make sure you saved it
   - Make sure it's the right file (in project root)
   - Make sure no spaces in the App Password

2. **Check App Password:**
   - Should be 16 characters
   - No special characters like @
   - No spaces

3. **Restart server:**
   - Must restart after changing .env!

---

## 📧 What Will Work After Fix:

- ✅ Admin creates Evaluator → Email sent
- ✅ Evaluator creates Student → Email sent
- ✅ All credentials delivered via email

---

**Follow these 4 steps exactly and the error will be fixed!** ✉️✅



