# 🔑 Platform Environment Variables Setup

## ⚠️ IMPORTANT: Required Environment Variables

Your application **REQUIRES** these environment variables to be set on your deployment platform:

---

## 🔴 **Critical (MUST SET for Production)**

### 1. SECRET_KEY
**Required:** Yes  
**Default:** Insecure fallback (will show warning)

```bash
# Generate a secure key:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Example output:
django-insecure-abc123xyz789...
```

**Set on platform:**
```
SECRET_KEY=your-generated-secret-key-here
```

---

### 2. DEBUG
**Required:** No  
**Default:** `False` (production mode)

```bash
# For development
DEBUG=True

# For production (recommended)
DEBUG=False
```

---

### 3. ALLOWED_HOSTS
**Required:** No  
**Default:** `localhost,mithunkumarrajak,127.0.0.1,127.0.0.1:8000,mithunkumarrajak.pythonanywhere.com`

```bash
# Add your domain(s)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## 🟡 **Database (Recommended for Production)**

### DATABASE_URL
**Required:** No (uses SQLite by default)  
**Recommended:** Yes for production

```bash
# PostgreSQL (Heroku, Railway, Render auto-provide this)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Or MySQL
DATABASE_URL=mysql://user:pass@host:3306/dbname
```

**Note:** Most platforms (Heroku, Railway, Render) automatically set this when you add a database.

---

## 🟢 **Email (Optional)**

### Email Settings
**Required:** No (uses console backend by default)

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

---

## 📋 Platform-Specific Instructions

### **Heroku**

```bash
# Set environment variables
heroku config:set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com

# Database URL is automatically set when you add PostgreSQL addon
heroku addons:create heroku-postgresql:mini
```

**View all config:**
```bash
heroku config
```

---

### **Railway**

1. Go to your project → **Variables** tab
2. Add variables:
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app.up.railway.app
   ```
3. DATABASE_URL is automatically set when you add PostgreSQL service

**Or via CLI:**
```bash
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG=False
```

---

### **Render**

1. Go to your web service → **Environment** tab
2. Add environment variables:
   - **Key:** `SECRET_KEY`
   - **Value:** Your generated secret key
   - **Key:** `DEBUG`
   - **Value:** `False`
   - **Key:** `ALLOWED_HOSTS`
   - **Value:** `your-app.onrender.com`

3. DATABASE_URL is automatically set when you create a PostgreSQL database

**Or in `render.yaml`:**
```yaml
services:
  - type: web
    name: smartshop
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn smartShop.wsgi
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: DATABASE_URL
        fromDatabase:
          name: smartshop-db
          property: connectionString
```

---

### **PythonAnywhere**

Edit your `.env` file on the server:

```bash
# SSH into your PythonAnywhere account
cd ~/e-commerce
nano .env
```

Add:
```env
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

---

### **AWS/DigitalOcean/VPS**

Create `.env` file on your server:

```bash
cd /var/www/e-commerce
sudo nano .env
```

Add all required variables:
```env
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

Make sure `.env` is secured:
```bash
sudo chmod 600 .env
sudo chown www-data:www-data .env
```

---

## ✅ Verification

After setting environment variables, verify they're loaded:

### On Heroku:
```bash
heroku run python -c "import os; print(os.environ.get('SECRET_KEY'))"
```

### On Railway/Render (check logs):
Look for the warning message. If you see:
```
WARNING: Using insecure SECRET_KEY!
```
Then your SECRET_KEY is not properly set!

### Local Testing:
```bash
# Without .env file
python manage.py check

# Should show:
# WARNING: Using insecure SECRET_KEY! Set SECRET_KEY environment variable in production!
```

---

## 🔒 Security Checklist

Before going to production:

- [ ] ✅ **SECRET_KEY** is set and unique (minimum 50 characters)
- [ ] ✅ **DEBUG** is set to `False`
- [ ] ✅ **ALLOWED_HOSTS** includes your domain
- [ ] ✅ **DATABASE_URL** points to production database (PostgreSQL recommended)
- [ ] ✅ No `.env` file committed to Git (check `.gitignore`)
- [ ] ✅ Email settings configured (if using email features)
- [ ] ✅ SSL/HTTPS enabled on your domain

---

## 🚨 Common Errors and Solutions

### Error: `decouple.UndefinedValueError: SECRET_KEY not found`

**Old Version (before fix):**
- Application crashes immediately

**New Version (with fix):**
- Application starts but shows warning
- Still runs but INSECURE

**Solution:**
Set SECRET_KEY environment variable on your platform!

### Error: `DisallowedHost at /`

**Cause:** Your domain is not in ALLOWED_HOSTS

**Solution:**
```bash
# Add your domain to ALLOWED_HOSTS
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost
```

### Error: Database connection issues

**Solution:**
Verify DATABASE_URL is correctly set:
```bash
# On Heroku
heroku config:get DATABASE_URL

# Should return something like:
# postgres://user:pass@host:5432/dbname
```

---

## 📝 Example: Complete .env File

For reference, here's a complete `.env` file:

```env
# Django Core
SECRET_KEY=django-insecure-abc123xyz789definitelychangethis567890
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (Production)
DATABASE_URL=postgresql://ecommerce_user:securepass@localhost:5432/ecommerce_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com  
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_USE_TLS=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

---

## 🎯 Quick Setup Commands

### Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Set on Heroku:
```bash
heroku config:set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
```

### Set on Railway:
```bash
railway variables set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
```

---

**After setting environment variables, redeploy or restart your application!**
