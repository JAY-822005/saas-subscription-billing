# 📊 SaaS Subscription Billing Platform - Project Overview

**Current Level:** Production-Ready MVP (70% Complete)  
**Last Updated:** May 6, 2026  
**Version:** 1.0.0

---

## 🎯 Project Purpose

This is a **backend API system** for managing SaaS subscriptions, similar to how Stripe, Paddle, or Chargebee work internally.

**Real-world use cases:**
- Managing subscription plans (Starter, Pro, Enterprise)
- Tracking which companies are subscribed to which plans
- Auto-generating invoices every month/year
- Managing failed payments and retries
- Tracking feature usage per customer
- Sending notifications (invoice due, payment failed, etc.)
- Logging all activities for compliance

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│          Frontend (HTML Templates/React)                │
├─────────────────────────────────────────────────────────┤
│                   REST API Layer                        │
│        (Django REST Framework with JWT Auth)            │
├─────────────────────────────────────────────────────────┤
│              Business Logic Layer                       │
│  (ViewSets, Serializers, Services, Permissions)        │
├─────────────────────────────────────────────────────────┤
│              Database Layer (SQLite/PostgreSQL)         │
│   (Users, Organizations, Subscriptions, Invoices, etc) │
├─────────────────────────────────────────────────────────┤
│        Background Jobs (Celery + Redis)                │
│     (Email notifications, Invoice generation, etc)      │
└─────────────────────────────────────────────────────────┘
```

---

## 💾 Data Structure (Database Schema)

### **Core Entities:**

```
User
├── username, email, password
├── role (super_admin, org_admin, manager, member)
├── phone, is_email_verified
└── created_at, updated_at

Organization (Multi-Tenant)
├── name, slug, owner (User)
├── contact_email, is_active
├── trial_ends_at
└── Relationships:
    ├── subscriptions (has one Subscription)
    ├── invoices (has many Invoices)
    ├── team_members (has many TeamMembers)
    ├── usage_records (has many UsageRecords)
    ├── audit_logs (has many AuditLogs)
    └── notifications (has many Notifications)

SubscriptionPlan (Shared across all organizations)
├── name, description
├── monthly_price, yearly_price
├── max_users, usage_limit
├── free_trial_days, is_active
└── Relationships:
    ├── subscriptions (has many Subscriptions)
    └── usage_records (has many UsageRecords)

Subscription (Per Organization)
├── organization (OneToOne)
├── plan (ForeignKey to SubscriptionPlan)
├── status (trial, active, cancelled, expired, past_due)
├── billing_cycle (monthly, yearly)
├── started_at, renews_at, cancelled_at
└── Relationships:
    └── invoices (has many Invoices)

Invoice
├── organization, subscription
├── invoice_number (auto-generated: INV-XXXXX)
├── amount, due_date, status
├── issued_at, paid_at
├── notes
└── Relationships:
    └── payment_recovery (OneToOne)

PaymentRecovery (Dunning)
├── invoice, organization
├── retry_count, max_retries (default: 3)
├── next_retry_at, status
├── failure_reason, recovered_at
└── Purpose: Handle failed payments & retries

TeamMember
├── organization, user
├── role (admin, member, viewer)
├── joined_at

UsageRecord (Feature usage tracking)
├── organization, subscription_plan
├── feature_name (api_calls, team_members, reports, storage, emails)
├── used_units, usage_limit
├── is_over_limit, billing_month
└── Auto-calculates: is_over_limit = used_units > usage_limit

Notification
├── organization
├── notification_type (trial_reminder, renewal, payment_failed, etc)
├── title, message
├── status (pending, sent, failed)
├── scheduled_for, sent_at

AuditLog (Compliance & security)
├── user, organization
├── action (create, update, delete, login, payment, etc)
├── model_name, object_id
├── ip_address, changes_made
└── created_at (immutable record)
```

---

## 🔑 Core Features Implemented

### ✅ **1. User Management (100% Complete)**

**Features:**
- ✅ Custom User model with roles (super_admin, org_admin, manager, member)
- ✅ JWT token-based authentication
- ✅ Email verification ready (flag exists: `is_email_verified`)
- ✅ User registration (public endpoint)
- ✅ User profile management
- ✅ Role-based permission checks

**Endpoints:**
```
POST   /api/users/register/              - Register new user
POST   /api/token/                       - Login (get JWT token)
POST   /api/token/refresh/               - Refresh token
GET    /api/users/profile/               - Get own profile
PUT    /api/users/profile/               - Update own profile
```

**Status:** ✅ Production-ready

---

### ✅ **2. Organization Management (100% Complete)**

**Features:**
- ✅ Multi-tenant architecture (each org is isolated)
- ✅ Create/read/update/delete organizations
- ✅ Organization ownership (user is owner)
- ✅ Unique slugs for clean URLs
- ✅ Trial period tracking
- ✅ Search & filter by name/email
- ✅ Automatic audit logging

**Endpoints:**
```
GET    /api/organizations/               - List user's organizations
POST   /api/organizations/               - Create new organization
GET    /api/organizations/{id}/          - Get single organization
PUT    /api/organizations/{id}/          - Update organization
DELETE /api/organizations/{id}/          - Delete organization
```

**Database:** 
- Stored in `organizations_organization` table
- Links to User as owner (Foreign Key)

**Status:** ✅ Production-ready

---

### ✅ **3. Subscription Plans (100% Complete)**

**Features:**
- ✅ Create billing plans (Starter, Pro, Enterprise, etc)
- ✅ Monthly and yearly pricing
- ✅ Max users per plan
- ✅ Usage limits
- ✅ Free trial days
- ✅ Read-only API (plans managed by admin)
- ✅ Search & filter

**Endpoints:**
```
GET    /api/subscriptions/plans/         - List all active plans
GET    /api/subscriptions/plans/{id}/    - Get single plan
```

**Database:** 
- Stored in `subscriptions_subscriptionplan` table
- Shared across all organizations

**Example Plans:**
```
Starter Plan:
  - Monthly: $9.99
  - Yearly: $99.90
  - Max Users: 3
  - Usage Limit: 1,000 API calls/month
  - Free Trial: 14 days

Pro Plan:
  - Monthly: $49.99
  - Yearly: $499.90
  - Max Users: 10
  - Usage Limit: 50,000 API calls/month
  - Free Trial: 14 days

Enterprise:
  - Custom pricing
  - Unlimited users
  - Custom limits
  - No trial
```

**Status:** ✅ Production-ready

---

### ✅ **4. Subscriptions (95% Complete)**

**Features:**
- ✅ Subscribe organization to a plan
- ✅ Monthly/yearly billing cycles
- ✅ Track status: trial → active → expired/cancelled
- ✅ Trial period management
- ✅ Renewal date tracking
- ✅ Upgrade/downgrade (logic ready)
- ✅ Search & filter by status
- ⚠️ Auto-renewal logic (partially done)

**Endpoints:**
```
GET    /api/subscriptions/               - List org's subscriptions
POST   /api/subscriptions/               - Create new subscription
GET    /api/subscriptions/{id}/          - Get single subscription
PUT    /api/subscriptions/{id}/          - Update subscription
DELETE /api/subscriptions/{id}/          - Cancel subscription
```

**Database:** 
- Stored in `subscriptions_subscription` table
- OneToOne relationship per organization (one org = one active subscription at a time)
- Tracks all status transitions

**Status:** ✅ 95% - Just needs auto-renewal task scheduling

---

### ✅ **5. Invoice Management (95% Complete)**

**Features:**
- ✅ Auto-generate invoice numbers (INV-XXXXX)
- ✅ Link invoices to subscriptions
- ✅ Track status: pending → paid/overdue/failed
- ✅ Mark invoices as paid
- ✅ Mark invoices as overdue
- ✅ Due date calculation
- ✅ Search & filter by status
- ⚠️ Auto-generate monthly invoices (scheduled task needed)

**Endpoints:**
```
GET    /api/invoices/                    - List invoices
POST   /api/invoices/                    - Create invoice
GET    /api/invoices/{id}/               - Get single invoice
PUT    /api/invoices/{id}/               - Update invoice
DELETE /api/invoices/{id}/               - Delete invoice (soft delete)

POST   /api/invoices/{id}/mark_paid/     - Mark as paid
POST   /api/invoices/{id}/mark_overdue/  - Mark as overdue
```

**Database:** 
- Stored in `invoices_invoice` table
- Foreign keys to Organization and Subscription
- Status tracking with timestamps

**Status:** ✅ 95% - Just needs scheduled invoice generation

---

### ✅ **6. Payment Recovery (Dunning) (90% Complete)**

**Features:**
- ✅ Track failed payments
- ✅ Auto-retry logic (configurable max retries)
- ✅ Schedule next retry
- ✅ Track retry count
- ✅ Store failure reason
- ✅ Search & filter
- ⚠️ Actual payment processor integration (Stripe webhook)
- ⚠️ Auto-retry scheduling task

**Endpoints:**
```
GET    /api/billing/                     - List payment recovery records
POST   /api/billing/                     - Create recovery record
GET    /api/billing/{id}/                - Get details
PUT    /api/billing/{id}/                - Update retry count/status
```

**Statuses:**
- pending → retrying → recovered/failed → cancelled

**Database:** 
- Stored in `billing_paymentrecovery` table
- OneToOne link to Invoice

**Status:** ✅ 90% - Needs Stripe webhook integration

---

### ✅ **7. Usage Tracking (100% Complete)**

**Features:**
- ✅ Track feature usage per organization
- ✅ Features: API calls, team members, reports, storage, emails
- ✅ Compare against limits
- ✅ Auto-flag overage
- ✅ Get upgrade recommendations
- ✅ Search & filter
- ✅ Monthly billing cycles

**Endpoints:**
```
GET    /api/usage-tracking/              - List usage records
POST   /api/usage-tracking/              - Log usage
GET    /api/usage-tracking/{id}/         - Get details
PUT    /api/usage-tracking/{id}/         - Update usage
GET    /api/usage-tracking/{id}/recommendation/  - Upgrade suggestion
```

**Database:** 
- Stored in `usage_tracking_usagerecord` table
- Tracks: used_units, usage_limit, is_over_limit
- Auto-calculates: is_over_limit = used_units > usage_limit

**Example:**
```
Organization: "Startup A"
Feature: "API Calls"
Used: 45,000 / Limit: 50,000 (90% of limit)
Status: ⚠️ Approaching limit → Recommend upgrade to Pro plan
```

**Status:** ✅ Production-ready

---

### ✅ **8. Team Management (100% Complete)**

**Features:**
- ✅ Add team members to organizations
- ✅ Assign roles (admin, member, viewer)
- ✅ Track join dates
- ✅ Remove team members
- ✅ Search & filter

**Endpoints:**
```
GET    /api/teams/                       - List team members
POST   /api/teams/                       - Add team member
GET    /api/teams/{id}/                  - Get member details
PUT    /api/teams/{id}/                  - Update role
DELETE /api/teams/{id}/                  - Remove member
```

**Roles:**
- **admin** - Full access to organization settings
- **member** - View and use organization resources
- **viewer** - Read-only access

**Database:** 
- Stored in `teams_teammember` table

**Status:** ✅ Production-ready

---

### ✅ **9. Audit Logging (100% Complete)**

**Features:**
- ✅ Log all user actions
- ✅ Track: create, update, delete, login, payment, subscription changes
- ✅ Store: user, organization, action, model name, object ID
- ✅ IP address logging
- ✅ Immutable records (for compliance)
- ✅ Search & filter
- ✅ Read-only API (can't delete logs)

**Endpoints:**
```
GET    /api/audit-logs/                  - List logs
GET    /api/audit-logs/{id}/             - Get log details
```

**Database:** 
- Stored in `audit_logs_auditlog` table
- Immutable (no delete/update allowed)

**Use Cases:**
- Compliance audits (GDPR, SOC2)
- Security investigations
- User activity tracking

**Status:** ✅ Production-ready

---

### ✅ **10. Notifications (90% Complete)**

**Features:**
- ✅ Store notification templates
- ✅ Schedule notifications
- ✅ Track notification status
- ✅ Types: trial_reminder, renewal_reminder, payment_failed, invoice_due, upgrade_suggestion
- ✅ Search & filter
- ⚠️ Email sending (Celery task needed)
- ⚠️ SMS/push notifications (not started)

**Endpoints:**
```
GET    /api/notifications/               - List notifications
POST   /api/notifications/               - Create notification
GET    /api/notifications/{id}/          - Get details
PUT    /api/notifications/{id}/          - Update (e.g., mark sent)
DELETE /api/notifications/{id}/          - Delete
```

**Statuses:**
- pending → sent / failed

**Database:** 
- Stored in `notifications_notification` table

**Status:** ✅ 90% - Just needs email sending task

---

### ✅ **11. Analytics & Dashboard (80% Complete)**

**Features:**
- ✅ Dashboard view with key metrics
- ✅ Revenue calculation
- ✅ Subscription counts
- ✅ Invoice summaries
- ✅ Recent activity
- ⚠️ Advanced analytics (not started)

**Endpoints:**
```
GET    /api/analytics/dashboard/         - Get dashboard metrics
```

**Metrics Provided:**
```
{
  "total_organizations": 5,
  "total_active_subscriptions": 4,
  "total_invoices": 12,
  "total_revenue_paid": 599.88,
  "revenue_pending": 99.99,
  "recent_invoices": [...],
  "recent_subscriptions": [...]
}
```

**Database:** 
- Aggregated from existing tables (no new table)

**Status:** ✅ 80% - Basic dashboard works, advanced analytics still needed

---

### ✅ **12. Frontend Pages (80% Complete)**

**Features:**
- ✅ Login page
- ✅ Register page
- ✅ Dashboard with metrics
- ✅ Organizations list
- ✅ Subscriptions list
- ✅ Invoices list
- ✅ User profile
- ⚠️ Advanced editing (mostly done)

**URLs:**
```
GET  /                                   - Redirect to dashboard
GET  /login/                             - Login page
GET  /register/                          - Register page
GET  /dashboard/                         - Main dashboard
GET  /organizations/                     - Organizations list
GET  /subscriptions/                     - Subscriptions list
GET  /invoices/                          - Invoices list
GET  /profile/                           - User profile
GET  /logout/                            - Logout
```

**Templates:** Bootstrap 5 responsive design

**Status:** ✅ 80% - Core pages work, some features missing

---

## 📊 How Data Flows

### **Example: Company Signs Up**

```
Step 1: Register
  User fills: email, username, password
  → POST /api/users/register/
  → User created in database

Step 2: Login
  User fills: username, password
  → POST /api/token/
  → Returns JWT token (valid for 30 mins)

Step 3: Create Organization
  User clicks "New Organization"
  → POST /api/organizations/ (with JWT token)
  → Organization created, user is owner

Step 4: Choose Plan
  User sees available plans
  → GET /api/subscriptions/plans/
  → Shows Starter ($9.99/mo), Pro ($49.99/mo), Enterprise

Step 5: Subscribe
  User selects "Starter Plan"
  → POST /api/subscriptions/
  → Subscription created with status="trial"
  → 14-day trial begins

Step 6: Trial Ends, Generate Invoice
  (Automatic - needs Celery task)
  → Invoice created: $9.99, due_date=30 days later
  → Notification sent: "Invoice due on [date]"

Step 7: Payment Processing
  (Integrates with Stripe - needs webhook)
  → Payment received: status="paid", paid_at=now
  → Next billing date: today + 30 days

Step 8: Auto-renew
  (Automatic - needs Celery beat)
  → Invoice created again for next month
  → Cycle repeats...

Step 9: Audit Trail
  All actions logged:
  - User login
  - Organization created
  - Subscription activated
  - Invoice created
  - Payment received
```

---

## 🔌 API Authentication

### **JWT Token Flow:**

```
1. POST /api/token/
   Request: { "username": "user@example.com", "password": "..." }
   Response: { "access": "eyJ0...", "refresh": "eyJ1..." }

2. Use access token in all requests:
   GET /api/organizations/
   Header: Authorization: Bearer eyJ0...

3. Token expires in 30 minutes
   POST /api/token/refresh/
   Request: { "refresh": "eyJ1..." }
   Response: { "access": "eyJ2..." }  (new access token)
```

---

## 🚀 What Works Right Now (Testing)

### **Fully Functional:**
✅ User registration & login  
✅ Create organizations  
✅ List organizations (with search)  
✅ View subscription plans  
✅ Create subscriptions  
✅ List subscriptions (with filter)  
✅ Create invoices  
✅ List invoices (with filter)  
✅ Track usage  
✅ View audit logs  
✅ Add team members  
✅ Dashboard with metrics  

### **Partially Functional:**
⚠️ Auto-invoice generation (manual works, auto-scheduled doesn't)  
⚠️ Payment recovery (tracking works, retry automation missing)  
⚠️ Notifications (storage works, email sending missing)  
⚠️ Frontend forms (basic works, validation incomplete)  

### **Not Yet Implemented:**
❌ Stripe integration (webhook, payment capture)  
❌ Email sending via Celery  
❌ SMS notifications  
❌ PDF invoice generation  
❌ Advanced analytics/reporting  
❌ Rate limiting  
❌ Database indexes  

---

## 🛠️ Technology Stack

### **Backend:**
- Python 3.14
- Django 6.0.4 (Web framework)
- Django REST Framework 3.17 (API)
- PostgreSQL or SQLite (Database)
- Celery 5.6.3 (Background tasks) - configured but not used yet
- Redis 7.4.0 (Cache & message broker) - configured but optional
- JWT SimplePy (Authentication) - Token-based auth

### **Frontend:**
- HTML/CSS/JavaScript
- Bootstrap 5 (Responsive design)
- Django Templates

### **DevOps:**
- Docker & Docker Compose (Containerization)
- Gunicorn (Production WSGI server)
- Pytest (Testing)

### **API Documentation:**
- Swagger/OpenAPI (Interactive docs)
- drf-yasg (Swagger generator)

---

## 📊 Current Project Maturity Level

| Area | Completion | Status |
|------|-----------|--------|
| **Data Models** | 100% | ✅ All models designed & migrated |
| **API Endpoints** | 95% | ✅ All CRUD operations work |
| **Authentication** | 100% | ✅ JWT fully functional |
| **Multi-tenancy** | 100% | ✅ Complete isolation per org |
| **Business Logic** | 85% | ⚠️ Core logic works, automation missing |
| **Scheduled Tasks** | 10% | ❌ Celery configured but not used |
| **Email Notifications** | 0% | ❌ Not implemented |
| **Payment Integration** | 0% | ❌ Not implemented |
| **Frontend** | 80% | ✅ Core pages work |
| **Testing** | 30% | ⚠️ Basic tests exist |
| **Documentation** | 95% | ✅ Well documented |
| **Production Ready** | 65% | ⚠️ MVP ready, not production yet |

### **Overall: 70% Complete - Production MVP**

---

## 🎯 How to Use the System

### **1. Register & Login:**
```bash
# 1. Open http://localhost:8000/register
# 2. Create account with email & password
# 3. Login with credentials
# 4. Redirects to dashboard
```

### **2. Create Organization:**
```bash
# Via Frontend:
# Click "New Organization" on dashboard
# Enter name, contact email
# Click "Create"

# Via API:
curl -X POST http://localhost:8000/api/organizations/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Startup A", "contact_email": "contact@startup.com"}'
```

### **3. View Available Plans:**
```bash
# Browser: http://localhost:8000/subscriptions/
# Or API: GET /api/subscriptions/plans/
```

### **4. Subscribe to Plan:**
```bash
# Via API:
curl -X POST http://localhost:8000/api/subscriptions/ \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "organization": "org-uuid",
    "plan": "plan-uuid",
    "billing_cycle": "monthly"
  }'
```

### **5. Track Usage:**
```bash
# Log API call usage:
curl -X POST http://localhost:8000/api/usage-tracking/ \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "organization": "org-uuid",
    "subscription_plan": "plan-uuid",
    "feature_name": "api_calls",
    "used_units": 1000,
    "usage_limit": 50000,
    "billing_month": "2026-05-01"
  }'
```

### **6. View Invoices:**
```bash
# Browser: http://localhost:8000/invoices/
# Or API: GET /api/invoices/
# Filter: GET /api/invoices/?status=pending
# Search: GET /api/invoices/?search=INV-1234
```

---

## 📈 Next Steps to Production

### **Priority 1 (Must Have) - 2 weeks:**
- [ ] Setup Celery workers
- [ ] Create scheduled invoice generation task
- [ ] Add email sending integration
- [ ] Stripe webhook integration
- [ ] Unit tests for models

### **Priority 2 (Should Have) - 3 weeks:**
- [ ] Payment retry automation
- [ ] Database indexes
- [ ] Rate limiting
- [ ] Advanced frontend validation
- [ ] PDF invoice generation

### **Priority 3 (Nice to Have) - 4 weeks:**
- [ ] SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Usage-based metering
- [ ] Mobile app API
- [ ] Customer portal (self-service)

---

## 🧪 Testing

### **Run Tests:**
```bash
# All tests
pytest

# Specific test file
pytest tests/test_subscriptions.py

# With coverage
pytest --cov=apps

# Verbose output
pytest -v
```

### **Sample Data:**
```bash
# Generate 3 users, 5 organizations
python manage.py generate_sample_data --users 3 --orgs 5
```

---

## 🔐 Security Features

✅ JWT token authentication  
✅ Password hashing (Django default)  
✅ CSRF protection  
✅ SQL injection prevention (ORM)  
✅ XSS protection (template escaping)  
✅ Role-based access control  
✅ Multi-tenant isolation  
✅ Audit logging  
⚠️ Rate limiting (not configured)  
⚠️ CORS (currently open - should restrict in production)  

---

## 📝 Database Schema Summary

```
Total Tables: 13 main apps + Django system tables
Total Fields: 150+
Relationships: 20+ ForeignKey relationships
Indexes: Basic Django indexes only (needs optimization)
Constraints: Unique emails, unique invoice numbers, etc.
```

---

## 🎓 Learning Path If Extending

1. **Understand Models** - Read `apps/*/models.py`
2. **Understand Views** - Read `apps/*/views.py` (ViewSets)
3. **Understand Serializers** - Read `apps/*/serializers.py` (validation)
4. **Understand Services** - Read `apps/*/services.py` (business logic)
5. **Add Tests** - Expand `tests/` directory
6. **Implement Celery** - Create `apps/*/tasks.py`
7. **Add Webhooks** - Create webhook handlers

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start server | `.\.venv\Scripts\python.exe manage.py runserver` |
| Run tests | `pytest` |
| Generate sample data | `python manage.py generate_sample_data` |
| Create superuser | `python manage.py createsuperuser` |
| Make migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Collect static files | `python manage.py collectstatic` |
| Access Swagger API | http://localhost:8000/swagger/ |
| Access Django Admin | http://localhost:8000/admin/ |
| Reset database | Delete `db.sqlite3` then `migrate` |

---

## ✅ Summary

**This SaaS billing platform is:**
- ✅ **Architecture-complete** - All major components designed
- ✅ **API-complete** - All endpoints implemented
- ✅ **Frontend-functional** - Core pages work
- ⚠️ **Automation-incomplete** - Background jobs not wired up
- ❌ **Payment-incomplete** - No Stripe integration yet
- ⚠️ **Production-limited** - Needs optimization & hardening

**Current Use:** Development, testing, learning, MVP demos  
**Ready for:** Small-scale deployments, learning projects, proof-of-concepts  
**Not ready for:** Large-scale production with real payments (yet)  

**Estimated effort to production:** 3-4 weeks of focused development

---

## 🎉 Congratulations!

You have a solid, well-structured SaaS billing backend that demonstrates professional software architecture. All the hard parts (multi-tenancy, API design, data modeling) are done. The remaining work is mostly integration & automation.

This is **70% of a production SaaS billing system**! 🚀

