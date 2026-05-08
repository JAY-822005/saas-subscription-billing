# Quick Start Guide - SaaS Billing Platform

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings (if needed)
# For development, defaults should work with PostgreSQL
```

### Step 3: Setup Database
```bash
# Create migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Generate sample data (optional)
python manage.py generate_sample_data --users 3 --orgs 5
```

### Step 4: Run Development Server
```bash
python manage.py runserver
```

### Step 5: Access the Application
Open your browser to:
- **Dashboard**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/swagger/

---

## 📝 Default Credentials (Sample Data)

If you ran `generate_sample_data`:
- **Email**: user1@example.com
- **Password**: testpass123

---

## 🎯 What You Can Do Now

### ✅ Frontend
- [x] Login/Register
- [x] View Dashboard with metrics
- [x] Manage Organizations
- [x] View Subscriptions
- [x] Browse Invoices
- [x] Update Profile

### ✅ API (REST)
- [x] User Authentication (JWT)
- [x] Organization Management
- [x] Subscription Plans
- [x] Subscription Management
- [x] Invoice Tracking
- [x] Billing Operations

### ✅ Admin Panel
- [x] User management
- [x] Organization management
- [x] Subscription management
- [x] Invoice management

---

## 📚 Project Structure

```
saas-subscription-billing/
├── templates/                 # Django HTML templates
│   ├── base.html             # Main layout template
│   ├── auth/                 # Authentication pages
│   │   ├── login.html
│   │   └── register.html
│   └── dashboard/            # Dashboard pages
│       ├── index.html
│       ├── organizations_list.html
│       ├── subscriptions_list.html
│       ├── invoices_list.html
│       └── profile.html
│
├── static/                    # Static files
│   ├── css/                  # Stylesheets
│   └── js/                   # JavaScript
│
├── apps/
│   ├── users/                # User management
│   ├── organizations/        # Organization/tenant management
│   ├── subscriptions/        # Subscription plans & subscriptions
│   ├── invoices/            # Invoice management
│   ├── billing/             # Billing operations
│   ├── notifications/       # Email/SMS notifications
│   ├── usage_tracking/      # Feature usage tracking
│   ├── audit_logs/          # Audit trail
│   ├── analytics/           # Reports & analytics
│   ├── teams/               # Team management
│   └── core/                # Common utilities
│
├── config/                   # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
│
├── tests/                    # Test suite
│
└── manage.py                # Django CLI
```

---

## 🔑 Key Features

### User Roles
- **Super Admin**: Full platform access
- **Organization Admin**: Organization-level access
- **Manager**: Can manage subscriptions and invoices
- **Member**: Limited access
- **Billing Admin**: Billing-specific access

### Subscription Plans
- Monthly and Yearly billing options
- Customizable trial periods
- Usage limits
- Max team member restrictions

### Billing
- Automatic invoice generation
- Payment tracking
- Overdue management
- Payment recovery retry logic
- Multiple payment methods support

---

## 🐛 Common Issues & Solutions

### PostgreSQL Connection Error
```
Error: could not connect to database server

Solution:
1. Ensure PostgreSQL is running
2. Check DB_HOST, DB_USER, DB_PASSWORD in .env
3. Create database: CREATE DATABASE saas_billing_db;
```

### Static Files Not Loading
```
Solution:
python manage.py collectstatic
```

### Permission Denied Errors
```
Solution:
1. Ensure user owns the organization/subscription
2. Check user role and permissions
3. Verify authentication token is valid
```

---

## 📖 API Endpoints

### Authentication
```
POST /api/token/              # Get JWT token
POST /api/token/refresh/      # Refresh token
GET  /login/                  # Frontend login
POST /logout/                 # Logout
```

### Organizations
```
GET    /api/organizations/         # List
POST   /api/organizations/         # Create
GET    /api/organizations/{id}/    # Detail
PUT    /api/organizations/{id}/    # Update
DELETE /api/organizations/{id}/    # Delete
```

### Subscriptions
```
GET    /api/subscriptions/              # List plans & subscriptions
POST   /api/subscriptions/              # Create subscription
GET    /api/subscriptions/{id}/         # Detail
PUT    /api/subscriptions/{id}/         # Update
```

### Invoices
```
GET    /api/invoices/           # List invoices
POST   /api/invoices/           # Create invoice
GET    /api/invoices/{id}/      # Detail
POST   /api/invoices/{id}/mark_paid/    # Mark as paid
POST   /api/invoices/{id}/mark_overdue/ # Mark as overdue
```

---

## 💡 Tips for Development

### 1. Create a Superuser
```bash
python manage.py createsuperuser
# Then access /admin/
```

### 2. View Logs
Logs are output to console. For file logging, update LOGGING in settings.py

### 3. Debug Mode
Set `DEBUG=True` in .env for development (never in production!)

### 4. Database Shell
```bash
python manage.py dbshell
# View data directly in database
```

### 5. Django Shell
```bash
python manage.py shell
# Interactive Python with Django models loaded
from apps.organizations.models import Organization
Organization.objects.all()
```

---

## 🔄 Database Migrations

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### View Migration Status
```bash
python manage.py showmigrations
```

---

## 🧪 Testing

### Run Tests
```bash
pytest
```

### Run Specific Test
```bash
pytest apps/users/tests.py
```

### With Coverage
```bash
pytest --cov=apps
```

---

## 📞 Support

### Documentation Files
- `README.md` - Project overview
- `IMPROVEMENTS.md` - Detailed improvements
- `.env.example` - Environment setup

### API Documentation
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

### Django Documentation
- https://docs.djangoproject.com/
- https://www.django-rest-framework.org/

---

## ✅ Next Steps Checklist

- [ ] Run `generate_sample_data` to populate database
- [ ] Log in to frontend dashboard
- [ ] View API docs in Swagger
- [ ] Create test organization
- [ ] Create subscription for organization
- [ ] Generate test invoices
- [ ] Explore admin panel
- [ ] Check out IMPROVEMENTS.md for detailed changes

---

**Happy Coding! 🚀**

For detailed improvements and next steps, see `IMPROVEMENTS.md`
