# 🏗️ Sprint 1: Backend API Foundation (15 minutes)

## 🎯 **COPY-PASTE PROMPT FOR SPRINT 1**

````text
Build Flask backend API endpoints for a fitness club membership system with the following requirements:

PYTHON VERSION REQUIREMENT:
- Python 3.13.5 (ensure compatibility with Flask 3.0.0 and SQLAlchemy 2.0.41 features)

SPRINT 1 FOCUS: BACKEND API + REAL DATABASE
- A. Keep the existing welcome page (/) unchanged from pre-sprint setup
- B. Create database models and initialize with seed data (real database)
- C. Add JSON API endpoints that return real data from database
- NO UI/Templates in Sprint 1 - that's Sprint 2's job
- Focus on backend functionality, data structure, and database operations

APPROACH:
1. Keep existing src\app.py welcome page route (/) unchanged
2. Create SQLAlchemy models for all entities with relationships
3. Initialize database with realistic seed data (not mock data)
4. Add API routes that return JSON responses with real database data
5. Prepare data structure for Sprint 2 frontend consumption

FILES TO CREATE/UPDATE:
- src\models.py (NEW: SQLAlchemy models with relationships)
- src\config.py (NEW: Flask configuration with database path)
- src\init_db.py (NEW: Database initialization with realistic seed data)
- src\app.py (UPDATE: Add API routes + database imports, keep welcome page unchanged)

REQUIRED API ENDPOINTS:
- GET / - Keep existing welcome page (pre-sprint, unchanged)
- GET /test - Backend verification endpoint (JSON)
- GET /api/members - Get all members (JSON)
- POST /api/members - Create new member (JSON)
- GET /api/plans - Get membership plans (JSON)
- GET /api/sessions - Get workout sessions (JSON)
- GET /api/trainers - Get trainers list (JSON)
- GET /api/stats - Get dashboard statistics (JSON)
- POST /api/sessions/schedule - Schedule session (JSON)

REQUIRED APP.PY STRUCTURE:
```python
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import config
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize SQLAlchemy with app
db = SQLAlchemy(app)

# Import models after db initialization
from models import Member, Plan, Trainer, Session

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Keep the original welcome page from pre-sprint (no changes)
@app.route('/')
def home():
    return render_template('index.html')

# Sprint 1: Backend API endpoints returning real database data

@app.route('/test')
def test():
    """Test endpoint to verify backend is working"""
    return jsonify({
        'status': 'success',
        'message': 'Flask Backend is Working with Database!',
        'endpoint': '/test',
        'timestamp': datetime.now().isoformat(),
        'database_connected': True
    })

@app.route('/api/members', methods=['GET'])
def api_members():
    """API: Get all members from database"""
    try:
        members = Member.query.all()
        members_data = []
        for member in members:
            members_data.append({
                'id': member.id,
                'name': member.name,
                'email': member.email,
                'phone': member.phone,
                'join_date': member.join_date.isoformat() if member.join_date else None,
                'plan_id': member.plan_id,
                'status': member.status
            })

        return jsonify({
            'status': 'success',
            'data': members_data,
            'count': len(members_data),
            'message': f'Retrieved {len(members_data)} members from database'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'count': 0,
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/api/members', methods=['POST'])
def api_create_member():
    """API: Create new member in database"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400

        # Create new member
        new_member = Member(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            plan_id=data.get('plan_id'),
            status=data.get('status', 'active')
        )

        db.session.add(new_member)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Member created successfully',
            'member_id': new_member.id,
            'data': {
                'id': new_member.id,
                'name': new_member.name,
                'email': new_member.email,
                'phone': new_member.phone,
                'plan_id': new_member.plan_id,
                'status': new_member.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to create member: {str(e)}'
        }), 500

# Continue with other API endpoints returning real database data...

@app.route('/api/plans', methods=['GET'])
def api_plans():
    """API: Get all membership plans from database"""
    try:
        plans = Plan.query.all()
        plans_data = []
        for plan in plans:
            plans_data.append({
                'id': plan.id,
                'name': plan.name,
                'description': plan.description,
                'price': float(plan.price),
                'duration_months': plan.duration_months,
                'features': plan.features.split(',') if plan.features else []
            })

        return jsonify({
            'status': 'success',
            'data': plans_data,
            'count': len(plans_data),
            'message': f'Retrieved {len(plans_data)} plans from database'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'count': 0,
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/api/sessions', methods=['GET'])
def api_sessions():
    """API: Get all workout sessions from database"""
    try:
        sessions = Session.query.all()
        sessions_data = []
        for session in sessions:
            sessions_data.append({
                'id': session.id,
                'title': session.title,
                'description': session.description,
                'trainer_id': session.trainer_id,
                'date': session.date.isoformat() if session.date else None,
                'time': session.time.strftime('%H:%M') if session.time else None,
                'capacity': session.capacity,
                'enrolled': session.enrolled,
                'status': session.status
            })

        return jsonify({
            'status': 'success',
            'data': sessions_data,
            'count': len(sessions_data),
            'message': f'Retrieved {len(sessions_data)} sessions from database'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'count': 0,
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/api/trainers', methods=['GET'])
def api_trainers():
    """API: Get all trainers from database"""
    try:
        trainers = Trainer.query.all()
        trainers_data = []
        for trainer in trainers:
            trainers_data.append({
                'id': trainer.id,
                'name': trainer.name,
                'email': trainer.email,
                'phone': trainer.phone,
                'specialization': trainer.specialization,
                'experience_years': trainer.experience_years,
                'bio': trainer.bio,
                'status': trainer.status
            })

        return jsonify({
            'status': 'success',
            'data': trainers_data,
            'count': len(trainers_data),
            'message': f'Retrieved {len(trainers_data)} trainers from database'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'count': 0,
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API: Get dashboard statistics from database"""
    try:
        # Get real statistics from database
        total_members = Member.query.filter_by(status='active').count()
        active_sessions = Session.query.filter_by(status='active').count()
        total_plans = Plan.query.count()
        total_trainers = Trainer.query.filter_by(status='active').count()

        # Calculate revenue (simplified - sum of all active member plans)
        monthly_revenue = 0
        active_members = Member.query.filter_by(status='active').all()
        for member in active_members:
            if member.plan:
                monthly_revenue += float(member.plan.price)

        stats = {
            'total_members': total_members,
            'active_sessions': active_sessions,
            'total_plans': total_plans,
            'total_trainers': total_trainers,
            'monthly_revenue': monthly_revenue,
            'new_members': Member.query.filter(
                Member.join_date >= datetime.now().replace(day=1)
            ).count()  # Members joined this month
        }

        return jsonify({
            'status': 'success',
            'data': stats,
            'message': 'Stats retrieved from database'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': {
                'total_members': 0,
                'active_sessions': 0,
                'total_plans': 0,
                'total_trainers': 0,
                'monthly_revenue': 0,
                'new_members': 0
            },
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/api/sessions/schedule', methods=['POST'])
def api_schedule_session():
    """API: Schedule a new session in database"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400

        # Create new session
        new_session = Session(
            title=data.get('title'),
            description=data.get('description'),
            trainer_id=data.get('trainer_id'),
            date=datetime.fromisoformat(data.get('date')) if data.get('date') else None,
            time=datetime.strptime(data.get('time'), '%H:%M').time() if data.get('time') else None,
            capacity=data.get('capacity', 10),
            enrolled=0,
            status='active'
        )

        db.session.add(new_session)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Session scheduled successfully',
            'session_id': new_session.id,
            'data': {
                'id': new_session.id,
                'title': new_session.title,
                'trainer_id': new_session.trainer_id,
                'date': new_session.date.isoformat() if new_session.date else None,
                'time': new_session.time.strftime('%H:%M') if new_session.time else None,
                'capacity': new_session.capacity,
                'status': new_session.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to schedule session: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

MODELS.PY REQUIREMENTS:
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import db from app.py
from app import db

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    join_date = db.Column(db.Date, default=datetime.utcnow)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    status = db.Column(db.String(20), default='active')

    # Relationship
    plan = db.relationship('Plan', backref='members')

    def __repr__(self):
        return f'<Member {self.name}>'

class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text, nullable=True)  # Comma-separated features

    def __repr__(self):
        return f'<Plan {self.name}>'

class Trainer(db.Model):
    __tablename__ = 'trainers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='active')

    def __repr__(self):
        return f'<Trainer {self.name}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, default=10)
    enrolled = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')

    # Relationship
    trainer = db.relationship('Trainer', backref='sessions')

    def __repr__(self):
        return f'<Session {self.title}>'
```

INIT_DB.PY REQUIREMENTS:
```python
from app import app, db
from models import Member, Plan, Trainer, Session
from datetime import datetime, date, time
from decimal import Decimal

def init_database():
    """Initialize database with seed data"""
    with app.app_context():
        # Create all tables
        db.create_all()

        # Clear existing data (for development)
        db.session.query(Session).delete()
        db.session.query(Member).delete()
        db.session.query(Trainer).delete()
        db.session.query(Plan).delete()

        # Create membership plans
        plans = [
            Plan(
                name='Basic Plan',
                description='Access to gym equipment and basic facilities',
                price=Decimal('29.99'),
                duration_months=1,
                features='Gym Access,Locker Room,Basic Equipment'
            ),
            Plan(
                name='Premium Plan',
                description='Full access including group classes and personal training',
                price=Decimal('59.99'),
                duration_months=1,
                features='Gym Access,Group Classes,Personal Training,Nutrition Guidance'
            ),
            Plan(
                name='Annual Plan',
                description='Full year membership with all benefits',
                price=Decimal('599.99'),
                duration_months=12,
                features='Gym Access,Group Classes,Personal Training,Nutrition Guidance,Member Events'
            )
        ]

        for plan in plans:
            db.session.add(plan)

        db.session.commit()

        # Create trainers
        trainers = [
            Trainer(
                name='John Smith',
                email='john.smith@fitnessclub.com',
                phone='555-0101',
                specialization='Weight Training',
                experience_years=5,
                bio='Certified personal trainer specializing in strength and conditioning.',
                status='active'
            ),
            Trainer(
                name='Sarah Johnson',
                email='sarah.johnson@fitnessclub.com',
                phone='555-0102',
                specialization='Yoga & Pilates',
                experience_years=8,
                bio='Yoga instructor with expertise in mindfulness and flexibility training.',
                status='active'
            ),
            Trainer(
                name='Mike Wilson',
                email='mike.wilson@fitnessclub.com',
                phone='555-0103',
                specialization='HIIT & Cardio',
                experience_years=3,
                bio='High-intensity training specialist focused on cardiovascular fitness.',
                status='active'
            )
        ]

        for trainer in trainers:
            db.session.add(trainer)

        db.session.commit()

        # Create members
        members = [
            Member(
                name='Alice Brown',
                email='alice.brown@email.com',
                phone='555-1001',
                join_date=date(2024, 1, 15),
                plan_id=2,  # Premium Plan
                status='active'
            ),
            Member(
                name='Bob Davis',
                email='bob.davis@email.com',
                phone='555-1002',
                join_date=date(2024, 2, 20),
                plan_id=1,  # Basic Plan
                status='active'
            ),
            Member(
                name='Carol White',
                email='carol.white@email.com',
                phone='555-1003',
                join_date=date(2024, 3, 10),
                plan_id=3,  # Annual Plan
                status='active'
            ),
            Member(
                name='David Green',
                email='david.green@email.com',
                phone='555-1004',
                join_date=date(2024, 12, 1),
                plan_id=2,  # Premium Plan
                status='active'
            )
        ]

        for member in members:
            db.session.add(member)

        db.session.commit()

        # Create workout sessions
        sessions = [
            Session(
                title='Morning Yoga',
                description='Relaxing morning yoga session for all levels',
                trainer_id=2,  # Sarah Johnson
                date=date(2025, 1, 20),
                time=time(8, 0),
                capacity=15,
                enrolled=8,
                status='active'
            ),
            Session(
                title='HIIT Workout',
                description='High-intensity interval training for maximum results',
                trainer_id=3,  # Mike Wilson
                date=date(2025, 1, 20),
                time=time(18, 0),
                capacity=12,
                enrolled=10,
                status='active'
            ),
            Session(
                title='Strength Training',
                description='Weight training fundamentals with proper form',
                trainer_id=1,  # John Smith
                date=date(2025, 1, 21),
                time=time(19, 0),
                capacity=8,
                enrolled=5,
                status='active'
            ),
            Session(
                title='Evening Pilates',
                description='Core strengthening and flexibility workout',
                trainer_id=2,  # Sarah Johnson
                date=date(2025, 1, 22),
                time=time(17, 30),
                capacity=10,
                enrolled=7,
                status='active'
            )
        ]

        for session in sessions:
            db.session.add(session)

        db.session.commit()

        print("Database initialized successfully!")
        print(f"Created {len(plans)} plans")
        print(f"Created {len(trainers)} trainers")
        print(f"Created {len(members)} members")
        print(f"Created {len(sessions)} sessions")

if __name__ == '__main__':
    init_database()
```

SPRINT 1 API ENDPOINTS SUMMARY:

✅ **Keep Unchanged:**
- GET / - Welcome page from pre-sprint (HTML)

✅ **Add New API Endpoints (Returning Real Database Data):**
- GET /test - Backend verification with database status (JSON)
- GET /api/members - Get all members from database (JSON)
- POST /api/members - Create new member in database (JSON)
- GET /api/plans - Get membership plans from database (JSON)
- GET /api/sessions - Get workout sessions from database (JSON)
- GET /api/trainers - Get trainers list from database (JSON)
- GET /api/stats - Get dashboard statistics from database (JSON)
- POST /api/sessions/schedule - Schedule session in database (JSON)

IMPORTANT: REAL DATABASE IN SPRINT 1
- Sprint 1 = Backend API endpoints with SQLAlchemy models and real data
- Sprint 2 = Frontend templates and UI
- Sprint 3 = Integration and polish

CONFIG.PY REQUIREMENTS:
```python
import os

class Config:
    SECRET_KEY = 'fitness-club-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance", "fitness_club.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

SPRINT 1 DATA STRUCTURE (Real Database Responses):
Each API endpoint returns JSON with real data from SQLAlchemy models:

```json
{
    "status": "success",
    "data": [real_database_records],
    "count": actual_count,
    "message": "Retrieved X records from database"
}
```

For /api/stats endpoint (real statistics):
```json
{
    "status": "success",
    "data": {
        "total_members": actual_member_count,
        "active_sessions": actual_session_count,
        "total_plans": actual_plan_count,
        "total_trainers": actual_trainer_count,
        "monthly_revenue": calculated_revenue,
        "new_members": current_month_member_count
    },
    "message": "Stats retrieved from database"
}
```

DATABASE REQUIRED FOR SPRINT 1:
- Create SQLAlchemy models (Member, Plan, Trainer, Session)
- Initialize database with realistic seed data
- API endpoints query real database data
- Prepare foundation for Sprint 2 frontend

## 🎯 **EXPECTED DELIVERABLES**

✅ **Sprint 1 Backend API Deliverables:**

- **A. src\app.py** - Flask app with API endpoints + SQLAlchemy integration (keeps existing welcome page)
- **B. src\models.py** - SQLAlchemy models (Member, Plan, Trainer, Session) with relationships
- **C. src\config.py** - Flask configuration with database path
- **D. src\init_db.py** - Database initialization script with realistic seed data
- **E. Database** - SQLite database with tables and seed data (src\instance\fitness_club.db)
- **F. API Endpoints** - All endpoints return JSON responses with real database data
- **G. Welcome Page** - Original welcome page unchanged from pre-sprint

✅ **API Endpoints Working (Real Database Data):**

- `GET /` - Welcome page (HTML, unchanged from pre-sprint)
- `GET /test` - Backend verification with database status (JSON)
- `GET /api/members` - Members from database (JSON)
- `POST /api/members` - Create member in database (JSON)
- `GET /api/plans` - Plans from database (JSON)
- `GET /api/sessions` - Sessions from database (JSON)
- `GET /api/trainers` - Trainers from database (JSON)
- `GET /api/stats` - Dashboard stats from database (JSON)
- `POST /api/sessions/schedule` - Schedule session in database (JSON)

## 🧪 **SPRINT 1 VERIFICATION CHECKLIST**

**Manual verification steps for Sprint 1 backend API:**

### **Step 1: Start Flask Application**

```powershell
# Navigate to src folder and start Flask app
Set-Location src
python app.py
```

### **Step 2: Initialize Database (New for Sprint 1)**

```powershell
# Initialize database with seed data
python init_db.py
```

✅ **Expected Output:**
```
Database initialized successfully!
Created 3 plans
Created 3 trainers
Created 4 members
Created 4 sessions
```

### **Step 3: Test Welcome Page (Should Remain Unchanged)**

- Open browser to `http://127.0.0.1:5000`
- ✅ Verify welcome page displays correctly (same as pre-sprint)
- ✅ Confirm TailwindCSS, Font Awesome, and favicon still work

### **Step 4: Test API Endpoints (Real Database Data)**

Open browser or use curl to test these JSON API endpoints:

- `http://127.0.0.1:5000/test` - Should return JSON with database_connected: true
- `http://127.0.0.1:5000/api/members` - Should return 4 real members from database
- `http://127.0.0.1:5000/api/plans` - Should return 3 real plans from database
- `http://127.0.0.1:5000/api/sessions` - Should return 4 real sessions from database
- `http://127.0.0.1:5000/api/trainers` - Should return 3 real trainers from database
- `http://127.0.0.1:5000/api/stats` - Should return real statistics from database

### **Step 5: Verify Database Responses**

Each API endpoint should return JSON with real data like:

```json
{
    "status": "success",
    "data": [array_of_real_records],
    "count": actual_count,
    "message": "Retrieved X records from database"
}
```

Example /api/members response should include real data:
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "name": "Alice Brown",
            "email": "alice.brown@email.com",
            "phone": "555-1001",
            "join_date": "2024-01-15",
            "plan_id": 2,
            "status": "active"
        }
    ],
    "count": 4,
    "message": "Retrieved 4 members from database"
}
```

---

## ✅ **SPRINT 1 COMPLETION CRITERIA**

**✅ ALL CHECKS PASSED?** → **Ready for Sprint 2!**
**❌ ANY FAILURES?** → **Review API endpoints and fix issues**

**Sprint 1 Success Indicators:**
- A. Welcome page unchanged from pre-sprint (HTML with styling)
- B. Database created and populated with seed data (SQLite)
- C. All API endpoints return JSON responses with real database data
- D. SQLAlchemy models working with proper relationships
- E. No HTML templates required (that's Sprint 2)
- F. Backend structure ready for frontend integration in Sprint 2

---

## 🚀 **SPRINT 1 COMPLETE - NEXT STEPS**

Once Sprint 1 verification passes, you're ready for:

**Sprint 2: Frontend Templates** - Create HTML templates that consume these APIs
**Sprint 3: Integration & Polish** - Connect frontend with backend, add validation

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre-Sprint-Setup.md) - 🛠 Environment Setup
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre-Sprint-Setup.md) - 🔧 Setup & Environment
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Frontend Templates
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Integration & Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 🎯 **NEXT STEP**

After completing Sprint 1, proceed to: **[4_Sprint2-Frontend.md](4_Sprint2-Frontend.md)** - Frontend Templates
````
