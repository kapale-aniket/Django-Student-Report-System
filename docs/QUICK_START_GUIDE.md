# 🚀 QUICK START GUIDE

## 📍 HOW TO ACCESS HOME PAGE

### Correct URL:
```
http://127.0.0.1:8000/
```
**This is the root URL - it shows the login form (home page)**

### Wrong URLs (These are dashboards, not home page):
- ❌ `http://127.0.0.1:8000/reports/admin/` (Admin Dashboard)
- ❌ `http://127.0.0.1:8000/reports/evaluator/` (Evaluator Dashboard)
- ❌ `http://127.0.0.1:8000/reports/student/` (Student Dashboard)

---

## 🔄 FIXING BROWSER CACHE ISSUE

### Problem: Browser shows old cached page

### Solution 1: Hard Refresh (Quickest)
1. Open browser
2. Go to: `http://127.0.0.1:8000/`
3. Press: **`Ctrl + F5`** (Windows/Linux) or **`Cmd + Shift + R`** (Mac)
4. Should see fresh login page

### Solution 2: Clear Browser Cache
1. Open browser settings
2. Go to Privacy/Security
3. Click "Clear browsing data"
4. Select "Cached images and files"
5. Click "Clear data"
6. Refresh page

### Solution 3: Use DevTools (Best for Development)
1. Press **`F12`** to open DevTools
2. Go to **Network** tab
3. Check **"Disable cache"** checkbox
4. Keep DevTools open while testing
5. Now all pages will load fresh

### Solution 4: Use Incognito/Private Window
1. Open new incognito window:
   - Chrome: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`
   - Edge: `Ctrl + Shift + N`
2. Go to: `http://127.0.0.1:8000/`
3. Should see fresh page (no cache)

---

## 🏁 STARTING THE SERVER

### Start Server:
```bash
python manage.py runserver
```

### Expected Output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Note:
- **You DON'T need to restart server** to see changes
- The issue is **browser cache**, not server
- Just clear cache or use hard refresh

---

## ✅ VERIFY HOME PAGE LOADS

### Step-by-Step:

1. **Start Server:**
   ```bash
   python manage.py runserver
   ```

2. **Open Browser:**
   - Go to: `http://127.0.0.1:8000/`
   - Press `Ctrl + F5` (hard refresh)

3. **What You Should See:**
   - ✅ Login form
   - ✅ "Welcome" message
   - ✅ "Register as Student" link
   - ✅ "Forgot Password?" link
   - ❌ NO sidebar
   - ❌ NO navbar (except maybe minimal)
   - ❌ NO dashboard content

4. **If You See Dashboard:**
   - You're logged in
   - Click logout button
   - Or clear cookies
   - Or use incognito window

---

## 🧪 TEST ALL BUTTONS WORK

### Admin Buttons (After Login):
1. ✅ Dashboard → `/reports/admin/`
2. ✅ All Reports → `/reports/all-reports/`
3. ✅ Users → `/reports/users/`
4. ✅ Add Evaluator → `/reports/users/add-evaluator/`
5. ✅ Assign Students → `/reports/users/assign-students/`
6. ✅ Profile (dropdown) → `/accounts/profile/`
7. ✅ Logout (dropdown) → `/accounts/logout/`

### Evaluator Buttons (After Login):
1. ✅ Dashboard → `/reports/evaluator/`
2. ✅ All Reports → `/reports/all-reports/`
3. ✅ Add Student → `/reports/students/add/`
4. ✅ My Students (sidebar) → `/reports/students/list/`
5. ✅ Profile (dropdown) → `/accounts/profile/`
6. ✅ Logout (dropdown) → `/accounts/logout/`

### Student Buttons (After Login):
1. ✅ Dashboard → `/reports/student/`
2. ✅ Submit Report → `/reports/submit/`
3. ✅ Profile (dropdown) → `/accounts/profile/`
4. ✅ Logout (dropdown) → `/accounts/logout/`

---

## 🔍 TROUBLESHOOTING

### Issue: "Old page still showing"
**Fix:** 
- Press `Ctrl + F5` (hard refresh)
- Or clear browser cache
- Or use incognito window

### Issue: "Need to restart server every time"
**Fix:** 
- You DON'T need to restart server
- The issue is browser cache
- Use hard refresh instead

### Issue: "Home page shows dashboard"
**Fix:**
- You're logged in
- Logout first
- Or clear cookies
- Home page only shows login form

### Issue: "Buttons don't work"
**Fix:**
- Check browser console (F12) for errors
- Verify you're logged in (if needed)
- Check URL is correct
- Verify server is running

### Issue: "Forms don't submit"
**Fix:**
- Fill all required fields
- Check for validation errors
- Verify server is running
- Check browser console for errors

---

## 📋 QUICK CHECKLIST

Before testing, ensure:
- [ ] Server is running: `python manage.py runserver`
- [ ] Browser cache is cleared (or use hard refresh)
- [ ] You're at correct URL: `http://127.0.0.1:8000/`
- [ ] You're NOT logged in (to see home page)
- [ ] DevTools "Disable cache" is checked (optional)

---

## 🎯 WHAT TO EXPECT

### When NOT Logged In:
- Visit: `http://127.0.0.1:8000/`
- See: **Login form** (home page)
- Can: Login or register

### When Logged In:
- Visit: `http://127.0.0.1:8000/`
- Automatically redirected to your dashboard:
  - Admin → `/reports/admin/`
  - Evaluator → `/reports/evaluator/`
  - Student → `/reports/student/`

### After Logout:
- Click logout button
- Redirected to: `http://127.0.0.1:8000/` (home/login page)
- See: **Login form** (NOT cached dashboard)

---

## 💡 PRO TIPS

1. **Always use hard refresh** (`Ctrl + F5`) when testing
2. **Keep DevTools open** with "Disable cache" checked during development
3. **Use incognito window** for clean testing
4. **Check browser console** (F12) if buttons don't work
5. **Verify URL** - make sure you're at the right page

---

**Follow this guide and everything will work correctly!**


