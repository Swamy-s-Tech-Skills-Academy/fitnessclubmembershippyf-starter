# 🏗️ Sprint 1: Backend Foundation (15 minutes)

## 🎯 **COPY-PASTE PROMPT FOR SPRINT 1**

```text
Build a complete Flask backend for a fitness club membership system with the following requirements:

MODELS NEEDED (with template compatibility properties):
1. Member (id, first_name, last_name, email, phone, date_of_birth, gender, emergency_contact, emergency_phone, join_date, status)
   - @property full_name -> return f"{first_name} {last_name}"
   - @property age -> calculate from date_of_birth
   - @property current_plans -> return active member plans

2. MembershipPlan (id, name, description, monthly_price, benefits)
   - @property price -> return monthly_price (for template compatibility)
   - @property duration_months -> return 1 (default monthly billing)

3. Trainer (id, name, specialization, email, phone)

4. WorkoutSession (id, title, description, trainer_id, session_date, start_time, end_time, max_capacity, current_bookings)
   - @property duration_minutes -> calculate from start_time to end_time
   - @property available_spots -> return max_capacity - current_bookings
   - @property is_full -> return current_bookings >= max_capacity
   - @property bookings -> return session_bookings (alias for compatibility)

5. MemberPlan (id, member_id, plan_id, start_date, end_date, status)
   - @property is_active -> check if status='active' and end_date is valid

6. SessionBooking (id, member_id, session_id, booking_date, status)

ESSENTIAL ROUTES (must match template expectations):
- / (dashboard with comprehensive statistics)
- /members (list with search and filtering)
- /members/create (member registration form)
- /members/<id> (member detail view)
- /members/<id>/edit (member edit form - required by templates)
- /plans (membership plans display)
- /sessions (workout sessions list)
- /sessions/schedule (session scheduling form)

CONFIGURATION REQUIREMENTS:
- POSTS_PER_PAGE = 10 (required for pagination)
- WTF_CSRF_ENABLED = True
- SECRET_KEY properly set
- SQLite database in src/instance/fitness_club.db

FILES TO CREATE:
- src/models.py (SQLAlchemy models with ALL compatibility properties)
- src/config.py (Flask configuration with pagination settings)
- src/app.py (Flask app with ALL routes matching template expectations)
- src/init_db.py (database initialization with comprehensive sample data)

SAMPLE DATA REQUIREMENTS:
- 5 members (with varied statuses: active/inactive)
- 3 membership plans (Basic $29.99, Premium $49.99, VIP $79.99)
- 3 trainers (with different specializations)
- 5 workout sessions (some today, some future, varied capacity)
- 3 member-plan relationships (active memberships)
- 2 session bookings (test booking system)

CRITICAL: All model properties must support template usage in Sprint 2 and advanced features in Sprint 3.
```

## ✅ **VALIDATION COMMANDS**

```bash
# ✅ Activate virtual environment
.venv\Scripts\activate

# ✅ Install dependencies (if not already done)
pip install flask flask-sqlalchemy flask-wtf

# ✅ Initialize database with sample data
cd src
python init_db.py

# ✅ Run the application
python app.py
# Visit http://localhost:5000 - should show dashboard with stats

# ✅ Test all routes work
# - http://localhost:5000/ (dashboard)
# - http://localhost:5000/members (member list)
# - http://localhost:5000/members/create (registration form)
# - http://localhost:5000/plans (membership plans)
# - http://localhost:5000/sessions (workout sessions)

# ✅ Verify database file created
ls instance/fitness_club.db
```

## 🎯 **EXPECTED DELIVERABLES**

- ✅ Complete database schema with 6 tables
- ✅ Flask app with ALL required routes (8 routes minimum)
- ✅ Models with compatibility properties for templates
- ✅ Comprehensive sample data (5 members, 3 plans, 3 trainers, 5 sessions)
- ✅ Working API endpoints with proper error handling
- ✅ Database file created and populated with relationships
- ✅ Configuration supporting pagination and security
- ✅ All routes accessible and returning proper responses

## 🚨 **CRITICAL SUCCESS CRITERIA**

- ✅ member.full_name property works
- ✅ plan.price property returns monthly_price
- ✅ session.duration_minutes calculates correctly
- ✅ All template-expected routes exist (/members/<id>/edit)
- ✅ POSTS_PER_PAGE configuration exists
- ✅ Sample data includes active/inactive members
- ✅ Ready for Sprint 2 template integration
