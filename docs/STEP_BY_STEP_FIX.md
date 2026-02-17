# 📋 STEP-BY-STEP: Fix Gmail Email Error

## 🎯 Goal:
Fix the error: `535, b'5.7.8 Username and Password not accepted`

---

## 📝 Step-by-Step Instructions:

### STEP 1: Enable 2-Step Verification (If Needed)

1. **Open your browser**
2. **Go to:** https://myaccount.google.com/security
3. **Scroll down** to find "2-Step Verification"
4. **Click "Turn on"** or "Get started"
5. **Follow the prompts:**
   - Enter your phone number
   - Verify with code sent to phone
   - Complete the setup

**⏱️ Time: 2-3 minutes**

---

### STEP 2: Generate Gmail App Password

1. **Go to:** https://myaccount.google.com/apppasswords
   - (If this doesn't work, go to: https://myaccount.google.com/security → Click "2-Step Verification" → Scroll down to "App passwords")

2. **You'll see a form:**
   - **"Select app"** dropdown → Choose **"Mail"**
   - **"Select device"** dropdown → Choose **"Other (Custom name)"**
   - **Text box appears** → Type: `Student Report System`
   - **Click "Generate" button**

3. **A 16-character password appears:**
   - Example: `abcd efgh ijkl mnop`
   - **COPY IT IMMEDIATELY!**
   - Remove spaces: `abcdefghijklmnop`
   - **⚠️ YOU CAN ONLY SEE THIS ONCE!**

**⏱️ Time: 1-2 minutes**

---

### STEP 3: Update .env File

1. **Open File Explorer**
2. **Navigate to:** `D:\django\Django-Student-Report-System`
3. **Find file:** `.env` (it might be hidden - enable "Show hidden files")
4. **Right-click** → **Open with** → **Notepad** (or any text editor)

5. **Find this line:**
   ```
   EMAIL_HOST_PASSWORD=Aniket@9096
   ```

6. **Replace it with:**
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   *(Replace `abcdefghijklmnop` with your actual App Password from Step 2)*

7. **Save the file:**
   - Press **Ctrl+S**
   - Or **File** → **Save**

**⏱️ Time: 1 minute**

---

### STEP 4: Restart Django Server

1. **Go to your terminal/command prompt**
2. **Find the window where Django is running**
3. **Press:** `Ctrl+C` (to stop the server)
4. **Start it again:**
   ```bash
   python manage.py runserver
   ```

**⏱️ Time: 10 seconds**

---

## ✅ Test It:

1. **Open your Django app** in browser
2. **Login as admin**
3. **Create a new evaluator** (or student)
4. **Check if email is sent successfully!**

---

## 🔍 How to Verify:

**Run this command to check your configuration:**
```bash
python verify_email_config.py
```

This will tell you if your `.env` file is configured correctly.

---

## 📋 Checklist:

- [ ] 2-Step Verification enabled on Google account
- [ ] App Password generated (16 characters)
- [ ] `.env` file opened and edited
- [ ] `EMAIL_HOST_PASSWORD` line updated with App Password
- [ ] `.env` file saved
- [ ] Django server restarted
- [ ] Tested by creating evaluator/student

---

## 🆘 Troubleshooting:

### "App passwords" option not showing
**Fix:** Make sure 2-Step Verification is enabled first. The option only appears after 2-Step Verification is turned on.

### Still getting error after updating .env
**Fix:**
1. Make sure you saved the `.env` file
2. Make sure you're using the App Password (16 chars, no @)
3. **Restart Django server** (this is important!)
4. Check for typos in the password

### Can't find .env file
**Fix:**
1. Enable "Show hidden files" in File Explorer
2. Or create a new `.env` file if it doesn't exist
3. Copy from `env.example` and update the password

---

## 🎯 Summary:

**Problem:** Gmail rejects regular passwords  
**Solution:** Use Gmail App Password (16 characters)  
**Action:** Update `.env` file and restart server

**Total time needed: ~5 minutes**

---

**Follow these steps exactly and your emails will work!** ✉️✅



