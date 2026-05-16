# System Architecture

## Overview

The system follows a modular, multi-tenant architecture built on Django REST Framework.

## Core Components

**Frontend:** Django templates with Bootstrap 5 for dashboards and user interfaces.

**REST API:** Django REST Framework endpoints with JWT authentication for external clients.

**Database:** PostgreSQL or SQLite for data persistence, supporting multi-tenant isolation.

**Message Queue:** Celery with Redis for asynchronous task processing (invoice generation, notifications, etc).

**Caching:** Redis for session management and query caching.

**Admin:** Django admin interface for internal management.

## Data Model

**Organizations:** Top-level tenants, containing subscriptions and teams.

**Users:** System users with roles (admin, owner, manager, member).

**Subscriptions:** Active product subscriptions with plans and billing cycles.

**Invoices:** Generated from subscriptions, tracked through their lifecycle.

**Usage Tracking:** Records API calls, seat usage, and other metered features.

**Audit Logs:** All significant changes for compliance.

## Key Design Decisions

**Multi-tenancy:** Organizations are isolated; no cross-organization data access.

**API-First:** All data access flows through REST APIs and serializers.

**Async Processing:** Long-running operations (invoicing, emails) use Celery tasks.

**Validation:** Serializers enforce business logic and data integrity.

**Separation of Concerns:** Each app handles a specific domain (users, subscriptions, billing, etc).
        │                        │                               │
        │  ┌─────────────────────▼──────────────────────────────┐│
        │  │         AUTHENTICATION LAYER (JWT)                 ││
        │  │  - Token generation                               ││
        │  │  - Token validation                               ││
        │  │  - Permission checks (IsAuthenticated, etc)       ││
        │  └─────────────────────┬──────────────────────────────┘│
        │                        │                               │
        │  ┌─────────────────────▼──────────────────────────────┐│
        │  │        BUSINESS LOGIC LAYER                        ││
        │  │                                                     ││
        │  │  ┌────────────────┐   ┌────────────────┐          ││
        │  │  │ ViewSets       │   │ Serializers    │          ││
        │  │  │ (Handle HTTP)  │   │ (Validation)   │          ││
        │  │  └────────────────┘   └────────────────┘          ││
        │  │                                                     ││
        │  │  ┌────────────────┐   ┌────────────────┐          ││
        │  │  │ Services       │   │ Models         │          ││
        │  │  │ (Business logic)   │ (Data schema)  │          ││
        │  │  └────────────────┘   └────────────────┘          ││
        │  └─────────────────────┬──────────────────────────────┘│
        │                        │                               │
        │  ┌─────────────────────▼──────────────────────────────┐│
        │  │         EXCEPTION HANDLER                          ││
        │  │  - Format error responses                          ││
        │  │  - Return consistent JSON                          ││
        │  └─────────────────────┬──────────────────────────────┘│
        │                        │                               │
        └────────────────────────┼───────────────────────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
        ┌────────▼────┐  ┌───────▼──────┐  ┌───▼─────────┐
        │  Database   │  │  Redis/Cache │  │   Celery    │
        │ (SQLite or  │  │   (Optional) │  │   Tasks     │
        │ PostgreSQL) │  │              │  │ (Background)│
        │             │  │ - Session    │  │             │
        │ Tables:     │  │   cache      │  │ - Email     │
        │ - users     │  │ - Data cache │  │ - Invoices  │
        │ - orgs      │  │              │  │ - Retries   │
        │ - subs      │  └──────────────┘  │             │
        │ - invoices  │                    └─────────────┘
        │ - audit_logs│
        │ - usage     │
        │ etc...      │
        └─────────────┘
```

---

## Request/Response Flow

```
1. USER REGISTERS
   ┌─────────────┐
   │   Browser   │
   └──────┬──────┘
          │ POST /register
          │ {email, username, password}
          ▼
   ┌─────────────────────────┐
   │ Django Request Handler  │
   └──────┬──────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ RegisterView (ViewSet)        │
   │ - Permission: AllowAny        │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ RegisterSerializer           │
   │ - Validate email unique      │
   │ - Validate password strength │
   │ - Hash password              │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ User Model (Create)          │
   │ INSERT INTO users_user ...   │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ Response (201 Created)       │
   │ {id, email, username, ...}   │
   └──────┬───────────────────────┘
          │
          ▼
   ┌─────────────┐
   │   Browser   │ ← "User registered successfully!"
   └─────────────┘

2. USER LOGS IN
   ┌─────────────┐
   │   Browser   │
   └──────┬──────┘
          │ POST /api/token
          │ {username, password}
          ▼
   ┌──────────────────────────────┐
   │ TokenObtainPairView          │
   │ - Authenticate user          │
   │ - Verify password            │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ JWT Token Generation         │
   │ - Create access token (30min)│
   │ - Create refresh (7 days)    │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ Response (200 OK)            │
   │ {                            │
   │   "access": "eyJ0...",       │
   │   "refresh": "eyJ1..."       │
   │ }                            │
   └──────┬───────────────────────┘
          │
          ▼
   ┌─────────────┐
   │   Browser   │ ← Store token, use in future requests
   └─────────────┘

3. CREATE ORGANIZATION (Authenticated)
   ┌─────────────┐
   │   Browser   │
   └──────┬──────┘
          │ POST /api/organizations/
          │ Header: Authorization: Bearer eyJ0...
          │ {name, contact_email}
          ▼
   ┌──────────────────────────────┐
   │ Check JWT Token              │
   │ - Verify signature           │
   │ - Check expiration           │
   │ - Extract user_id            │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ Request = Authenticated      │
   │ request.user = <User object> │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ OrganizationViewSet          │
   │ - Permission: IsAuthenticated│
   │ ✓ User has access           │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ OrganizationSerializer       │
   │ - Validate name unique       │
   │ - Validate email format      │
   │ - Auto-generate slug         │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ Organization Model (Create)  │
   │ INSERT INTO organizations... │
   │ owner_id = 42 (logged-in user)
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ Audit Log (Automatic)        │
   │ INSERT INTO audit_logs...    │
   │ action="create", model="Org" │
   └──────┬───────────────────────┘
          │
          ▼
   ┌──────────────────────────────┐
   │ Response (201 Created)       │
   │ {id, name, slug, owner, ...} │
   └──────┬───────────────────────┘
          │
          ▼
   ┌─────────────┐
   │   Browser   │ ← "Organization created!"
   └─────────────┘
```

---

## Database Relationships (ER Diagram)

```
User (1) ─────────────── (N) Organization
  │                          │
  │ owns_organizations        │
  │                           │ has_one
  │                           ▼
  │                       Subscription
  │                       │    │
  │                       │    └──► SubscriptionPlan
  │                       │
  │                       └──────► (N) Invoice
  │                                  │
  │                                  └──► PaymentRecovery
  │
  │
  ├─────────────────────► (N) AuditLog
  │
  └────────► (N) TeamMember
                 │
                 └─────────► Organization


Organization ─────────► (N) UsageRecord
             │              │
             │              └──► SubscriptionPlan
             │
             ├────────► (N) Notification
             │
             └────────► (N) AuditLog
```

---

## Subscription Lifecycle

```
Time ────────────────────────────────────────────────────────────────►

User subscribes
to "Starter" plan      Day 30 (Billing date)    Day 60
      │                       │                    │
      ▼                       ▼                    ▼
   TRIAL              ACTIVE (1st month)    ACTIVE (2nd month)
(14 days free)      [Invoice generated]   [Invoice generated]
      │                  │                    │
      │                  ▼                    ▼
      │            Invoice sent         Invoice sent
      │            "Pay $9.99"           "Pay $9.99"
      │                  │                    │
      ▼                  ▼                    ▼
[Day 14]      [Payment received]     [Payment received]
Status→ACTIVE    Status→PAID           Status→PAID
             [Next invoice in 30d]  [Next invoice in 30d]

Alternative paths:
- Payment fails → PaymentRecovery created → Retries 3x → Status→FAILED
- User cancels → Status→CANCELLED → No more invoices
- User upgrades → Switch to better plan → Proration calculated
```

---

## Multi-Tenancy Data Isolation

```
Database has 1 table per entity, but data is segregated:

invoices table:
┌────┬──────────────┬─────────────────────┐
│ id │ organization │ invoice_number      │
├────┼──────────────┼─────────────────────┤
│ 1  │ org_A (User1)│ INV-A001 ($9.99)   │
│ 2  │ org_A (User1)│ INV-A002 ($9.99)   │
│ 3  │ org_B (User2)│ INV-B001 ($49.99)  │
│ 4  │ org_B (User2)│ INV-B002 ($49.99)  │
│ 5  │ org_C (User2)│ INV-C001 ($99.99)  │
└────┴──────────────┴─────────────────────┘

When User1 queries:
  GET /api/invoices/
  ↓
  ViewSet filters:
  WHERE organization.owner = User1
  ↓
  Returns: [Invoice 1, Invoice 2]
  ✓ User1 can only see their own invoices

When User2 queries:
  GET /api/invoices/
  ↓
  ViewSet filters:
  WHERE organization.owner = User2
  ↓
  Returns: [Invoice 3, Invoice 4, Invoice 5]
  ✓ User2 can only see their own invoices
```

---

## API Response Structure

```
Success (200 OK):
┌────────────────────────────┐
│ {                          │
│   "id": "uuid-123",        │
│   "name": "Startup A",     │
│   "slug": "startup-a",     │
│   "contact_email": "...",  │
│   "is_active": true,       │
│   "created_at": "2026-05-06T10:00:00Z",
│   "updated_at": "2026-05-06T10:00:00Z"
│ }                          │
└────────────────────────────┘

Paginated List (200 OK):
┌────────────────────────────┐
│ {                          │
│   "count": 15,             │
│   "next": "../?page=2",    │
│   "previous": null,        │
│   "results": [             │
│     {...},                 │
│     {...}                  │
│   ]                        │
│ }                          │
└────────────────────────────┘

Error (400 Bad Request):
┌────────────────────────────┐
│ {                          │
│   "success": false,        │
│   "error": "Validation...",│
│   "status_code": 400,      │
│   "details": {             │
│     "email": [             │
│       "Invalid email"      │
│     ]                      │
│   }                        │
│ }                          │
└────────────────────────────┘

Error (403 Forbidden):
┌────────────────────────────┐
│ {                          │
│   "success": false,        │
│   "error": "Permission...",│
│   "status_code": 403,      │
│   "details": null          │
│ }                          │
└────────────────────────────┘
```

---

## Authentication Flow (JWT)

```
┌─────────┐
│ Browser │
└────┬────┘
     │ 1. POST /api/token/ {username, password}
     ▼
┌────────────────────────┐
│ TokenObtainPairView    │
│ - Validate credentials │
│ - Create tokens        │
└────┬───────────────────┘
     │ 2. Response: {access, refresh}
     ▼
┌─────────┐
│ Browser │ (Stores access token)
└────┬────┘
     │ 3. GET /api/organizations/
     │    Header: "Authorization: Bearer access_token"
     ▼
┌─────────────────────────┐
│ JWT Authentication      │
│ - Extract token        │
│ - Verify signature      │
│ - Check expiration      │
│ - Extract user_id       │
└────┬───────────────────┘
     │ 4. Set request.user = <User object>
     ▼
┌─────────────────────────┐
│ ViewSet                 │
│ - Check permission      │
│ - Access request.user   │
│ - Return filtered data  │
└────┬───────────────────┘
     │ 5. Response: [org1, org2, ...]
     ▼
┌─────────┐
│ Browser │ (Displays data)
└─────────┘

Token Expiration Flow:
Access token expires (30 min) → User action fails (401 Unauthorized)
                             ↓
                      POST /api/token/refresh/ {refresh}
                             ↓
                      New access token issued
                             ↓
                      Retry original request
                             ↓
                      ✓ Success
```

---

## Notification Flow (Not Yet Automated)

```
1. Event Occurs
   - Invoice created
   - Payment failed
   - Trial ending soon
   - Usage limit approaching
          │
          ▼
2. Generate Notification
   Organization + Type + Message
   Status = "pending"
   scheduled_for = now/future date
          │
          ▼
3. Store in Database
   INSERT INTO notifications_notification ...
          │
          ▼
4. Celery Task (Not Yet Implemented)
   Check for pending notifications
   → For each notification:
     → Send email (not yet)
     → Mark as "sent" or "failed"
          │
          ▼
5. User Receives Email
   "Your trial is ending in 3 days"
   "Invoice due: $9.99"
   etc.
```

---

## Production Deployment Architecture

```
              INTERNET
                 │
        ┌────────┴────────┐
        │                 │
    ┌───▼──┐          ┌──▼───┐
    │Nginx │          │Nginx │ (Load Balanced)
    └───┬──┘          └──┬───┘
        │                 │
        └────────┬────────┘
                 │
        ┌────────┴────────┐
        │                 │
    ┌───▼──┐          ┌──▼───┐
    │Django│          │Django│ (Multiple containers)
    │Web 1 │          │Web 2 │
    └───┬──┘          └──┬───┘
        │                 │
        └────────┬────────┘
                 │
        ┌────────┴────────┐
        │                 │
    ┌───▼──────┐      ┌──▼────┐
    │PostgreSQL│      │ Redis  │
    │Database  │      │ Cache  │
    └──────────┘      └─┬──┬───┘
                        │  │
                ┌───────┘  │
                │          │
            ┌───▼──┐   ┌──▼────┐
            │Celery│   │ Celery│
            │Beat  │   │Worker │
            └──────┘   └───────┘
```

---

## Performance & Scalability Considerations

```
Current State:
┌─────────────────────────────────┐
│ Single Django Instance (Dev)    │
│ SQLite Database (File-based)    │
│ No caching                      │
│ No background tasks             │
│ Handles: ~100 concurrent users  │
└─────────────────────────────────┘
        ↓ (To scale up)
        ↓

Optimized State:
┌─────────────────────────────────┐
│ Load Balanced (2-4 instances)   │
│ PostgreSQL (Optimized)          │
│ Redis Caching Layer             │
│ Celery Workers (1-4)            │
│ Database Read Replicas (optional)
│ CDN for Static Files            │
│ Handles: ~10,000 concurrent     │
└─────────────────────────────────┘
```

---

## Summary: How Everything Connects

```
1. User interacts → Django routes request
2. Authentication validates JWT token
3. Permission classes check access
4. ViewSet handles the request
5. Serializer validates input
6. Model processes data
7. Service performs business logic
8. Database stores changes
9. Audit log records action
10. Exception handler formats response
11. Browser displays result
```

**It's all connected! 🔗**

