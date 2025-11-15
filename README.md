# 🛍️ ReviewApp - E-commerce Review Platform

A modern, full-stack web application built with Django 5.1.7 that enables users to browse products, write reviews, and interact with a comprehensive rating system. Features role-based authentication, Google OAuth integration, and an intuitive admin dashboard.

![Django](https://img.shields.io/badge/Django-5.1.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔐 Authentication System
- **Dual Authentication:** Traditional username/password and Google OAuth integration
- **Role-Based Access Control:** Separate User and Admin roles with distinct permissions
- **Secure Login:** Custom authentication backend with session management
- **Auto-Fill Prevention:** Enhanced security with autocomplete disabled on sensitive forms

### 👥 User Features
- **Product Catalog:** Browse beautifully designed product cards with images and ratings
- **Review System:** Write detailed reviews with star ratings (1-5 stars)
- **Interactive Engagement:** Like/dislike reviews and add threaded replies
- **Personalized Dashboard:** View all products with real-time rating aggregation
- **User Profile:** Customized greeting with avatar and email display

### 👨‍💼 Admin Features
- **Admin Dashboard:** Comprehensive control panel for product management
- **Product Management:** Full CRUD operations (Create, Read, Update, Delete)
- **Separate Admin Login:** Dedicated secure login portal for administrators
- **Product Image Upload:** Media handling with automatic image storage
- **Review Moderation:** Monitor and manage user reviews and interactions

### 🎨 Modern UI/UX
- **Glass-Morphism Design:** Contemporary aesthetic with transparency effects
- **Gradient Backgrounds:** Beautiful color transitions and animations
- **Responsive Layout:** Mobile-first design that works on all devices
- **Smooth Animations:** Floating elements, hover effects, and transitions
- **Interactive Elements:** Dynamic forms, buttons, and navigation

## 🛠️ Technology Stack

**Backend:**
- Django 5.1.7
- Python 3.13
- SQLite Database
- Django Allauth (Social Authentication)

**Frontend:**
- HTML5
- CSS3 (Modern features: Grid, Flexbox, Animations)
- JavaScript (ES6+)
- Custom CSS Framework

**Authentication:**
- Django Authentication System
- Custom Authentication Backend
- Google OAuth 2.0 Integration

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.11 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Anjana2552/Django.git
cd Django
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django==5.1.7
pip install django-allauth
pip install Pillow
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 🔑 Google OAuth Setup (Optional)

To enable Google OAuth login:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
6. Update `settings.py` with your credentials

## 📁 Project Structure

```
reviewproj/
├── manage.py
├── db.sqlite3
├── README.md
├── reviewapp/
│   ├── models.py          # Database models (CustomUser, Product, Review, etc.)
│   ├── views.py           # View functions and business logic
│   ├── forms.py           # Django forms for user input
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin panel configuration
│   ├── migrations/        # Database migrations
│   └── templatetags/      # Custom template filters
├── reviewproj/
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/
│   ├── landing.html       # Homepage
│   ├── login.html         # User login page
│   ├── signup.html        # User registration
│   ├── admin_login.html   # Admin login portal
│   ├── user_dashboard.html    # User dashboard
│   ├── admin_dashboard.html   # Admin control panel
│   ├── product_detail.html    # Product details & reviews
│   ├── add_product.html       # Add new product (Admin)
│   ├── edit_product_list.html # Edit products (Admin)
│   └── view_reviews.html      # Review management
└── media/
    └── product_images/    # Uploaded product images
```

## 🎯 Usage Guide

### For Users:
1. **Sign Up:** Create an account via traditional signup or Google OAuth
2. **Browse Products:** View the product catalog on your dashboard
3. **View Details:** Click on any product to see full details and reviews
4. **Write Reviews:** Rate products (1-5 stars) and write detailed feedback
5. **Engage:** Like/dislike reviews and reply to other users' comments

### For Admins:
1. **Admin Login:** Access via `http://127.0.0.1:8000/admin_login/`
2. **Add Products:** Upload product images, set prices, and descriptions
3. **Edit Products:** Update existing product information
4. **Delete Products:** Remove products from the catalog
5. **Monitor Reviews:** View all reviews and user interactions

## 🔧 Configuration

### Key Settings (`settings.py`)

```python
# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'reviewapp.backends.EmailBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Social Account Providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}
```

## 📱 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/login` | GET/POST | User login |
| `/signup/` | GET/POST | User registration |
| `/admin_login/` | GET/POST | Admin login |
| `/dashboard/user/` | GET | User dashboard |
| `/dashboard/admin/` | GET | Admin dashboard |
| `/add-product/` | GET/POST | Add new product (Admin) |
| `/product/<id>/` | GET | Product detail page |
| `/product/<id>/review/` | POST | Submit review |
| `/reviews/<id>/like/` | POST | Like/unlike review |
| `/google-oauth-login/` | POST | Google OAuth handler |

## 🎨 Design Features

- **Color Scheme:** Purple gradient (`#667eea → #764ba2 → #f093fb`)
- **Typography:** 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Effects:** Glass-morphism, backdrop-filter blur, box-shadows
- **Animations:** Floating elements, hover transforms, smooth transitions
- **Responsive:** Mobile-first design with media queries

## 🔒 Security Features

- CSRF Protection on all forms
- Password hashing with Django's authentication system
- Session-based authentication
- Role-based access control
- Autocomplete disabled on sensitive inputs
- Secure file upload handling

## 🐛 Known Issues & Future Enhancements

**Future Enhancements:**
- [ ] Add search functionality for products
- [ ] Implement product categories and filtering
- [ ] Add pagination for product listings
- [ ] Email verification for new users
- [ ] Password reset functionality
- [ ] User profile editing
- [ ] Advanced analytics dashboard for admins
- [ ] Export reviews to CSV/PDF

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Developer

**Anjana**
- GitHub: [@Anjana2552](https://github.com/Anjana2552)
- LinkedIn: [Connect with me](https://www.linkedin.com)

## 🙏 Acknowledgments

- Django Documentation
- Django Allauth for social authentication
- Google OAuth for authentication services
- Icons and design inspiration from modern UI/UX trends

## 📞 Support

For support, email anjanaviswanath9910@gmail.com or open an issue in the GitHub repository.

---

**⭐ If you found this project helpful, please consider giving it a star!**

Made with ❤️ using Django
