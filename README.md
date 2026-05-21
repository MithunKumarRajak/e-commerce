# 🛍️ SmartShop E-Commerce Platform

A full-featured e-commerce web application built with Django, offering a seamless shopping experience with modern UI/UX, secure payment processing, and comprehensive order management.

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🛒 **Shopping Experience**
- Browse products by categories
- Advanced product search and filtering
- Product details with image gallery
- Shopping cart with quantity management
- Wishlist functionality
- Real-time cart updates

### 👤 **User Management**
- User registration and authentication
- Profile management
- Order history tracking
- Address management

### 📦 **Order Management**
- Seamless checkout process
- Multiple payment options
- Order tracking
- Email notifications
- Invoice generation

### 🔒 **Security**
- Secure password handling
- CSRF protection
- XSS protection
- SQL injection prevention
- HTTPS enforcement in production
- Session security

### 📱 **Responsive Design**
- Mobile-first approach
- Works on all devices
- Modern and intuitive UI

---

## 🛠️ Tech Stack

### **Backend**
- **Framework:** Django 5.2.7
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** Django Auth System
- **API:** Django REST Framework
- **Task Queue:** Uvicorn (ASGI)

### **Frontend**
- **Template Engine:** Django Templates
- **Styling:** Bootstrap 5 + Custom CSS
- **JavaScript:** Vanilla JS + jQuery

### **Deployment**
- **WSGI Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Database Adapter:** dj-database-url
- **Environment Variables:** python-decouple

### **Additional Libraries**
- **Image Processing:** Pillow
- **JWT:** djangorestframework-simplejwt
- **Admin Enhancements:** django-admin-thumbnails

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **pip** (comes with Python)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/MithunKumarRajak/e-commerce.git
cd e-commerce
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv env
source env/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Environment Setup

Create a `.env` file in the project root:

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

Edit `.env` and configure your settings (see [Environment Configuration](#-environment-configuration))

#### 5. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# (Optional) Load sample data
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/products.json
```

#### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 7. Run Development Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser 🎉

#### 8. Access Admin Panel

Visit **http://127.0.0.1:8000/admin**
- Username: Your superuser username
- Password: Your superuser password

---

## 🔧 Environment Configuration

### Required Environment Variables

Create a `.env` file with the following variables:

```env
# Django Core Settings
SECRET_KEY=your-secret-key-here-minimum-50-characters
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Optional: Override email backend
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Twilio SMS Configuration (for Order Notifications)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
```

### Generating a Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Gmail App Password Setup

1. Enable 2-Factor Authentication on your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use this password in `EMAIL_HOST_PASSWORD`
---

## 📁 Project Structure

```
e-commerce/
│
├── 📂 accounts/              # User authentication & management
│   ├── models.py            # Custom user model
│   ├── views.py             # Auth views (login, register, profile)
│   ├── forms.py             # User forms
│   └── urls.py              # Account routes
│
├── 📂 carts/                # Shopping cart functionality
│   ├── models.py            # Cart & CartItem models
│   ├── views.py             # Cart operations
│   ├── context_processors.py  # Cart counter
│   └── urls.py
│
├── 📂 category/             # Product categorization
│   ├── models.py            # Category model
│   ├── context_processors.py # Menu links
│   └── admin.py
│
├── 📂 orders/               # Order management
│   ├── models.py            # Order & OrderProduct models
│   ├── views.py             # Checkout & order processing
│   └── urls.py
│
├── 📂 products/             # Product catalog
│   ├── models.py            # Product & Variation models
│   ├── views.py             # Product listing & details
│   └── urls.py
│
├── 📂 smartShop/            # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI config
│   └── views.py             # Core views (home, about, etc.)
│
├── 📂 static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── 📂 staticfiles/          # Collected static files (production)
│
├── 📂 templates/            # HTML templates
│   ├── base.html           # Base template
│   ├── home.html           # Homepage
│   ├── pages/              # Static pages
│   └── ...
│
├── 📂 media/                # User-uploaded files
│
├── 📂 fixtures/             # Sample data
│   ├── categories.json
│   └── products.json
│
├── 📄 .env                  # Environment variables (not in repo)
├── 📄 .env.example          # Environment template
├── 📄 .gitignore            # Git ignore rules
├── 📄 manage.py             # Django management script
├── 📄 Procfile              # Heroku process file
├── 📄 runtime.txt           # Python version specification
├── 📄 requirements.txt      # Python dependencies
└── 📄 README.md             # This file
```

---

## 📡 API Documentation

This project includes a REST API built with Django REST Framework.

### Base URL
- Development: `http://127.0.0.1:8000/api/`
- Production: `https://your-domain.com/api/`

### Authentication
Uses JWT (JSON Web Tokens) for API authentication.

#### Get Token
```bash
POST /api/token/
{
    "username": "user@example.com",
    "password": "password"
}
```

#### Refresh Token
```bash
POST /api/token/refresh/
{
    "refresh": "your-refresh-token"
}
```

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List all products | No |
| GET | `/api/products/{id}/` | Get product details | No |
| GET | `/api/categories/` | List all categories | No |
| GET | `/api/cart/` | Get user's cart | Yes |
| POST | `/api/cart/add/` | Add item to cart | Yes |
| DELETE | `/api/cart/{item_id}/` | Remove from cart | Yes |
| GET | `/api/orders/` | List user's orders | Yes |
| POST | `/api/orders/create/` | Create new order | Yes |

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test products

# Run with coverage
pip install coverage
coverage run manage.py test
coverage report
```

---

## 🛡️ Security Features

### Production Security Checklist

- ✅ **DEBUG = False** in production
- ✅ **SECRET_KEY** unique and secure
- ✅ **HTTPS enforcement** via `SECURE_SSL_REDIRECT`
- ✅ **Secure cookies** (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- ✅ **HSTS** enabled with 1-year duration
- ✅ **XSS protection** enabled
- ✅ **CSRF protection** on all forms
- ✅ **Content-Type sniffing** prevention
- ✅ **Clickjacking protection** (X-Frame-Options)
- ✅ **Password validation** enforced
- ✅ **SQL injection** prevention (Django ORM)

### Running Security Checks

```bash
python manage.py check --deploy
```

---

## 🔍 Troubleshooting

### Common Issues

#### Issue: Static files not loading in production
**Solution:**
```bash
python manage.py collectstatic --noinput
# Ensure WhiteNoise is properly configured in settings.py
```

#### Issue: Database connection errors
**Solution:**
```bash
# Check DATABASE_URL in .env
# Ensure PostgreSQL is running
# Verify database credentials
```

#### Issue: Email not sending
**Solution:**
```bash
# Check email settings in .env
# For Gmail, use App Password, not regular password
# Verify EMAIL_USE_TLS=True for port 587
```

#### Issue: ModuleNotFoundError
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact & Support

- **Author:** SmartShop
- **Email:** esmartshopoffical@gmail.com
- **GitHub:** [@MithunKumarRajak](https://github.com/MithunKumarRajak)
- **Website:** [your-website.com](https://your-website.com)

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- All contributors and supporters

---

## 📊 Project Status

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Maintenance](https://img.shields.io/badge/Maintained-Yes-green.svg)

**Version:** 1.0.0  
**Last Updated:** November 2025

---

<div align="center">
Made with ❤️ by SmartShop
</div>
