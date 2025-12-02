# 🔧 FIX: "Connection Refused" Error

## ✅ Server Status
**Your server IS running on port 8000!**

---

## 🌐 Correct URL to Use

### ✅ CORRECT:
```
http://127.0.0.1:8000/
```

OR

```
http://localhost:8000/
```

### ❌ WRONG:
- `https://127.0.0.1:8000/` (Don't use HTTPS)
- `127.0.0.1:8000` (Missing http://)
- `www.127.0.0.1:8000` (Don't use www)

---

## 🔍 Troubleshooting Steps

### Step 1: Check URL Format
- ✅ Use: `http://127.0.0.1:8000/`
- ❌ Don't use: `https://` (SSL not enabled)
- ✅ Make sure to include `http://` at the beginning

### Step 2: Clear Browser Cache
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear data"
4. Try accessing again

### Step 3: Hard Refresh
- Press `Ctrl + F5` (Windows/Linux)
- Press `Cmd + Shift + R` (Mac)
- This forces browser to reload

### Step 4: Try Different Browser
- Try Chrome
- Try Edge
- Try Firefox
- Try Incognito/Private mode

### Step 5: Check Firewall
If firewall is blocking:

**Windows Firewall:**
1. Go to: Settings → Privacy & Security → Windows Security
2. Click "Firewall & network protection"
3. Click "Allow an app through firewall"
4. Make sure Python is allowed

**Or temporarily disable firewall to test:**
1. Go to Windows Security
2. Turn off firewall temporarily
3. Try accessing website
4. Turn firewall back on

### Step 6: Check Server is Actually Running
In terminal, you should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

If not, start the server:
```bash
python manage.py runserver
```

### Step 7: Check Port is Not Blocked
```bash
netstat -an | findstr ":8000"
```

Should show: `LISTENING`

---

## 🚀 Quick Fix Steps

1. **Open browser**
2. **Type exactly:** `http://127.0.0.1:8000/`
3. **Press Enter**
4. **If error persists:**
   - Clear browser cache
   - Try incognito window
   - Try different browser

---

## 📋 Common Mistakes

### ❌ Wrong:
- Using `https://` instead of `http://`
- Forgetting `http://` prefix
- Using wrong port number
- Server not running

### ✅ Correct:
- Using `http://127.0.0.1:8000/`
- Server running in terminal
- Browser cache cleared
- Correct URL format

---

## 🎯 If Still Not Working

### Option 1: Restart Server
1. Stop server: Press `Ctrl+C` in terminal
2. Start again: `python manage.py runserver`
3. Wait for "Starting development server..."
4. Try accessing again

### Option 2: Use Different Port
If port 8000 is blocked:
```bash
python manage.py runserver 8001
```
Then access: `http://127.0.0.1:8001/`

### Option 3: Check Django Settings
Make sure in `settings.py`:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

---

## ✅ Verification Checklist

- [ ] Server is running (check terminal)
- [ ] Using correct URL: `http://127.0.0.1:8000/`
- [ ] Browser cache cleared
- [ ] Tried different browser
- [ ] Firewall not blocking
- [ ] Port 8000 is listening

---

## 🆘 Still Having Issues?

1. **Check terminal for errors:**
   - Look for error messages
   - Check if server crashed

2. **Check browser console:**
   - Press F12
   - Look for errors

3. **Try localhost instead:**
   - `http://localhost:8000/`

4. **Check network settings:**
   - Make sure you're not using proxy
   - Check VPN is not interfering

---

## 📝 Summary

**Server Status:** ✅ Running  
**Port:** 8000  
**Correct URL:** `http://127.0.0.1:8000/`  

**If connection refused:**
- ✅ Check URL format (use http:// not https://)
- ✅ Clear browser cache
- ✅ Try different browser
- ✅ Check firewall settings
- ✅ Restart server if needed

**Everything should work now!**

