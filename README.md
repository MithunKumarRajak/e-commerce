# 🛍️ SmartShop E-Commerce Platform

A full-featured e-commerce web application built with Django, offering a seamless shopping experience with modern UI/UX, secure payment processing, and comprehensive order management.

🔗 **Live Demo:** [mithunkumarrajak.pythonanywhere.com](https://mithunkumarrajak.pythonanywhere.com/)

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Project Status](https://img.shields.io/badge/Status-Active-success)

### 👥 Team
| Name | Role | GitHub |
|------|------|--------|
| **Mithun Kumar Rajak** | Backend, Payments, Deployment | [@MithunKumarRajak](https://github.com/MithunKumarRajak) |
| **Sanket Raikwar** | Frontend, Product Content | [@Sanket-Raikwar](https://github.com/Sanket-Raikwar) |

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Environment Configuration](#-environment-configuration)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact--support)

---

## ✨ Features

### 🛒 **Shopping Experience**
- Browse products by categories
- Advanced product search with live autocomplete suggestions
- Product details with image gallery
- Shopping cart with quantity management
- Real-time cart updates

### 👤 **User Management**
- User registration and authentication
- Profile management with avatar
- Order history tracking
- Address management

### 📦 **Order Management**
- Seamless checkout process
- Multiple payment options (PayPal & Razorpay)
- SMS order notifications via Twilio
- Email confirmations
- Order tracking

### 🔒 **Security**
- Secure password handling with Django validators
- CSRF & XSS protection
- SQL injection prevention (Django ORM)
- Clickjacking protection (X-Frame-Options)
- Session security

### 📱 **Responsive Design**
- Mobile-first approach
- Works on all devices
- Modern and intuitive UI with Bootstrap 5

---

## 🛠️ Tech Stack

### **Backend**
- **Framework:** Django 5.2.7
- **Database:** SQLite
- **Authentication:** Django Auth System (Custom User Model)
- **API:** Django REST Framework + SimpleJWT

### **Frontend**
- **Template Engine:** Django Templates
- **Styling:** Bootstrap 5 + Custom CSS
- **JavaScript:** Vanilla JS + jQuery

### **Integrations**
- **Payments:** PayPal SDK + Razorpay
- **SMS Notifications:** Twilio
- **Environment Variables:** python-decouple

### **Additional Libraries**
- **Image Processing:** Pillow
- **Admin Enhancements:** django-admin-thumbnails

---

## 🚀 Quick Start

### Prerequisites

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

#### 6. Run Development Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser 🎉

#### 7. Access Admin Panel

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
│   ├── models.py            # Custom user model (Account)
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
│   ├── sms_service.py       # Twilio SMS integration
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
│   └── views.py             # Core views (home, etc.)
│
├── 📂 static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── 📂 templates/            # HTML templates
│   ├── base.html           # Base template
│   ├── home.html           # Homepage
│   └── ...
│
├── 📂 media/                # User-uploaded files
│
├── 📂 fixtures/             # Sample data
│   ├── categories.json
│   └── products.json
│
├── 📄 .env.example          # Environment template
├── 📄 .gitignore            # Git ignore rules
├── 📄 manage.py             # Django management script
├── 📄 requirements.txt      # Python dependencies
└── 📄 README.md             # This file
```

---

## 📡 API Documentation

This project includes a REST API built with Django REST Framework.

### Base URL
- Development: `http://127.0.0.1:8000/api/`
- Production: `https://mithunkumarrajak.pythonanywhere.com/api/`

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

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

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

| Team Member | GitHub | Email |
|-------------|--------|-------|
| **Mithun Kumar Rajak** | [@MithunKumarRajak](https://github.com/MithunKumarRajak) | mithunkumarrajak01012005@gmail.com |
| **Sanket Raikwar** | [@Sanket-Raikwar](https://github.com/Sanket-Raikwar) | raikwarsanket97@gmail.com |

🔗 **Live Demo:** [mithunkumarrajak.pythonanywhere.com](https://mithunkumarrajak.pythonanywhere.com/)

---

<div align="center">
Made with ❤️ by Mithun Kumar Rajak & Sanket Raikwar
</div>
