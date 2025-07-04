# 🏗️ Sprint 1: Backend Foundation (15 minutes)

## 🎯 **COPY-PASTE PROMPT FOR SPRINT 1**

````text
Build a complete Flask backend for a fitness club membership system with the following requirements:

MODELS NEEDED:
1. Member (id, first_name, last_name, email, phone, date_of_birth, gender, emergency_contact, emergency_phone, join_date, status)
2. MembershipPlan (id, name, description, monthly_price, benefits)
3. Trainer (id, name, specialization, email, phone)
4. WorkoutSession (id, title, description, trainer_id, session_date, start_time, end_time, max_capacity, current_bookings)
5. MemberPlan (id, member_id, plan_id, start_date, end_date, status)
6. SessionBooking (id, member_id, session_id, booking_date, status)

FILES TO CREATE:
- src/models.py (SQLAlchemy models with relationships)
- src/config.py (Flask configuration with ABSOLUTE database path)
- src/app.py (Flask app with routes for dashboard, members, plans, sessions)
- src/init_db.py (database initialization with sample data)

IMPORTANT DATABASE PATH CONFIG:
In config.py, use absolute path to prevent "unable to open database file" error:

```python
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "instance", "fitness_club.db")}'
````

ROUTES NEEDED:

- / (dashboard with statistics)
- /members (list with search)
- /members/create (member registration)
- /members/\<id\> (member details)
- /plans (membership plans)
- /sessions (workout sessions)
- /sessions/schedule (session scheduling)

Include comprehensive sample data: 3 members, 3 plans, 3 trainers, 3 sessions with proper relationships.
Use SQLite database in src/instance/fitness_club.db

````

## ✅ **VALIDATION COMMANDS**

```bash
# Activate virtual environment
.venv\Scripts\activate
cd src
python init_db.py
python app.py
# Visit http://localhost:5000 - should show dashboard
````

## 🛠️ **TROUBLESHOOTING**

**If you get "unable to open database file" error:**

- Ensure config.py uses absolute path with `basedir = os.path.abspath(os.path.dirname(__file__))`
- Verify `src/instance/` directory exists
- Check that database URI uses forward slashes: `f'sqlite:///{os.path.join(basedir, "instance", "fitness_club.db")}'`

## 🎯 **EXPECTED DELIVERABLES**

- ✅ Complete database schema with 6 tables
- ✅ Flask app with 7+ routes
- ✅ Sample data with relationships
- ✅ Working API endpoints
- ✅ Database file created and populated

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre-Sprint-Setup.md) - 🔧 Setup & Environment
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 🎯 **NEXT STEP**

After completing Sprint 1, proceed to: **[4_Sprint2-Frontend.md](4_Sprint2-Frontend.md)** - Frontend Templates
