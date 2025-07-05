# 🏗️ Sprint 1: Backend API + Dashboard UI (15 minutes)

## 🎯 **COPY-PASTE PROMPT FOR SPRINT 1**

````text
Build Flask backend API endpoints + Dashboard UI for a fitness club membership system with the following requirements:

IMPORTANT: Navigation Component Update Required
Before starting backend development, update the navigation component:
1. Open src\templates\_navbar.html
2. Change Dashboard link from href="#" to href="{{ url_for('dashboard') }}"
3. Add proper active state highlighting for Dashboard page
This ensures navigation works properly when Dashboard is created.

PYTHON VERSION REQUIREMENT:
- Python 3.13.5 (ensure compatibility with Flask 3.0.0 and SQLAlchemy 2.0.41 features)

SPRINT 1 FOCUS: BACKEND API + REAL DATABASE + DASHBOARD UI
- A. Keep the existing welcome page (/) unchanged from pre-sprint setup
- B. Update navigation component to include Dashboard link
- C. Create database models and initialize with seed data (real database)
- D. Add JSON API endpoints that return real data from database
- E. Create Dashboard UI that displays real statistics and data
- Focus on backend functionality, data structure, and dashboard visualization

APPROACH (FIXED TO AVOID CIRCULAR IMPORTS):
1. Keep existing src\app.py welcome page route (/) unchanged
2. Update _navbar.html component to add active Dashboard link
3. Create a simple, single-file approach with all models in app.py to avoid circular imports
4. Initialize database with realistic seed data (not mock data)
5. Add API routes that return JSON responses with real database data
6. Create Dashboard UI template that extends base.html
7. Prepare data structure for Sprint 2 (Members & Plans management)

FILES TO CREATE/UPDATE:
- src\templates\_navbar.html (UPDATE: Add Dashboard link to navigation)
- src\init_db.py (NEW: Database initialization with realistic seed data)
- src\app.py (UPDATE: Add models, API routes + Dashboard route + database setup, keep welcome page unchanged)
- src\templates\dashboard.html (NEW: Dashboard UI template extending base.html)

IMPORTANT: SINGLE FILE APPROACH (NO CIRCULAR IMPORTS)
- All SQLAlchemy models will be defined directly in app.py
- No separate models.py or config.py files to avoid import issues
- Clean, simple structure that works reliably

REQUIRED ROUTES:
- GET / - Keep existing welcome page (pre-sprint, unchanged)
- GET /dashboard - Dashboard UI with real statistics and data visualization
- GET /test - Backend verification endpoint (JSON)
- GET /api/members - Get all members (JSON)
- POST /api/members - Create new member (JSON)
- GET /api/plans - Get membership plans (JSON)
- GET /api/sessions - Get workout sessions (JSON)
- GET /api/trainers - Get trainers list (JSON)
- GET /api/stats - Get dashboard statistics (JSON)
- POST /api/sessions/schedule - Schedule session (JSON)

REQUIRED APP.PY STRUCTURE (SINGLE FILE, NO CIRCULAR IMPORTS):
```python
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from decimal import Decimal
import os

app = Flask(__name__)

# Configuration (inline to avoid separate config file)
app.config['SECRET_KEY'] = 'fitness-club-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance", "fitness_club.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db = SQLAlchemy(app)

# SQLAlchemy Models (defined in same file to avoid circular imports)
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

    @property
    def full_name(self):
        return self.name

    @property
    def member_count(self):
        """For template compatibility - returns 1 for individual member"""
        return 1

    def __repr__(self):
        return f'<Member {self.name}>'

class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text, nullable=True)  # Comma-separated features

    @property
    def member_count(self):
        """Count of active members with this plan"""
        return len([m for m in self.members if m.status == 'active'])

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
    duration_minutes = db.Column(db.Integer, default=60)  # Session duration in minutes
    capacity = db.Column(db.Integer, default=10)
    enrolled = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')

    # Relationship
    trainer = db.relationship('Trainer', backref='sessions')

    def __repr__(self):
        return f'<Session {self.title}>'

class SessionEnrollment(db.Model):
    __tablename__ = 'session_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='enrolled')  # enrolled, cancelled, completed

    # Relationships
    session = db.relationship('Session', backref='enrollments')
    member = db.relationship('Member', backref='session_enrollments')

    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint('session_id', 'member_id', name='unique_session_member'),)

    def __repr__(self):
        return f'<SessionEnrollment {self.member_id} -> {self.session_id}>'

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Keep the original welcome page from pre-sprint (no changes)
@app.route('/')
def home():
    return render_template('index.html')

# Sprint 1: Dashboard UI route (NEW)
@app.route('/dashboard')
def dashboard():
    """Dashboard UI displaying real data from database"""
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

        # Get recent members
        recent_members = Member.query.order_by(Member.join_date.desc()).limit(5).all()

        # Get upcoming sessions
        upcoming_sessions = Session.query.filter_by(status='active').order_by(Session.date, Session.time).limit(5).all()

        # Pass data to template
        return render_template('dashboard.html',
            total_members=total_members,
            active_sessions=active_sessions,
            total_plans=total_plans,
            total_trainers=total_trainers,
            monthly_revenue=monthly_revenue,
            recent_members=recent_members,
            upcoming_sessions=upcoming_sessions
        )
    except Exception as e:
        # Fallback with empty data if database issues
        return render_template('dashboard.html',
            total_members=0,
            active_sessions=0,
            total_plans=0,
            total_trainers=0,
            monthly_revenue=0,
            recent_members=[],
            upcoming_sessions=[],
            error=str(e)
        )

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
                'duration_minutes': session.duration_minutes,
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
            duration_minutes=data.get('duration_minutes', 60),
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
                'duration_minutes': new_session.duration_minutes,
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

MODELS ARE INCLUDED IN APP.PY (NO SEPARATE MODELS.PY FILE):
All SQLAlchemy models are defined directly in app.py to avoid circular import issues.
This is the recommended approach for this sprint.

The models (Member, Plan, Trainer, Session) are already included in the app.py structure above.
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

    @property
    def full_name(self):
        return self.name

    @property
    def member_count(self):
        """For template compatibility - returns 1 for individual member"""
        return 1

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
    duration_minutes = db.Column(db.Integer, default=60)  # Session duration in minutes
    capacity = db.Column(db.Integer, default=10)
    enrolled = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')

    # Relationship
    trainer = db.relationship('Trainer', backref='sessions')

    def __repr__(self):
        return f'<Session {self.title}>'
```

INIT_DB.PY REQUIREMENTS (SIMPLIFIED - NO CIRCULAR IMPORTS):
```python
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Member, Plan, Trainer, Session
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
                duration_minutes=60,
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
                duration_minutes=45,
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
                duration_minutes=60,
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
                duration_minutes=60,
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

DASHBOARD.HTML TEMPLATE REQUIREMENTS:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fitness Club Dashboard</title>

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Font Awesome CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">

    <style>
        body { font-family: 'Inter', sans-serif; }
        h1, h2, h3, h4, h5, h6 { font-family: 'Poppins', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <i class="fas fa-dumbbell text-blue-600 text-2xl mr-3"></i>
                    <h1 class="text-xl font-bold text-gray-900">Fitness Club Dashboard</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <a href="/" class="text-gray-600 hover:text-blue-600 transition-colors">
                        <i class="fas fa-home mr-1"></i> Home
                    </a>
                    <span class="text-gray-400">|</span>
                    <span class="text-blue-600 font-medium">
                        <i class="fas fa-chart-line mr-1"></i> Dashboard
                    </span>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Page Header -->
        <div class="mb-8">
            <h2 class="text-3xl font-bold text-gray-900">Club Overview</h2>
            <p class="mt-2 text-gray-600">Real-time statistics from your fitness club database</p>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Total Members Card -->
            <div class="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200">
                <div class="p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            <i class="fas fa-users text-blue-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Total Members</p>
                            <p class="text-2xl font-bold text-gray-900">{{ total_members }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Active Sessions Card -->
            <div class="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200">
                <div class="p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            <i class="fas fa-calendar-check text-green-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Active Sessions</p>
                            <p class="text-2xl font-bold text-gray-900">{{ active_sessions }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Total Trainers Card -->
            <div class="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200">
                <div class="p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            <i class="fas fa-user-tie text-purple-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Active Trainers</p>
                            <p class="text-2xl font-bold text-gray-900">{{ total_trainers }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Monthly Revenue Card -->
            <div class="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200">
                <div class="p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            <i class="fas fa-dollar-sign text-yellow-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-600">Monthly Revenue</p>
                            <p class="text-2xl font-bold text-gray-900">${{ "%.2f"|format(monthly_revenue) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Two Column Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Recent Members -->
            <div class="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">
                        <i class="fas fa-user-plus text-blue-600 mr-2"></i>Recent Members
                    </h3>
                </div>
                <div class="p-6">
                    {% if recent_members %}
                        <div class="space-y-4">
                            {% for member in recent_members %}
                            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div>
                                    <p class="font-medium text-gray-900">{{ member.name }}</p>
                                    <p class="text-sm text-gray-600">{{ member.email }}</p>
                                </div>
                                <div class="text-right">
                                    <p class="text-sm text-gray-500">Joined</p>
                                    <p class="text-sm font-medium text-gray-900">{{ member.join_date.strftime('%m/%d/%Y') if member.join_date else 'N/A' }}</p>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-gray-500 text-center py-4">No recent members found</p>
                    {% endif %}
                </div>
            </div>

            <!-- Upcoming Sessions -->
            <div class="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">
                        <i class="fas fa-calendar-alt text-green-600 mr-2"></i>Upcoming Sessions
                    </h3>
                </div>
                <div class="p-6">
                    {% if upcoming_sessions %}
                        <div class="space-y-4">
                            {% for session in upcoming_sessions %}
                            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div>
                                    <p class="font-medium text-gray-900">{{ session.title }}</p>
                                    <p class="text-sm text-gray-600">{{ session.description[:50] }}{% if session.description|length > 50 %}...{% endif %}</p>
                                </div>
                                <div class="text-right">
                                    <p class="text-sm text-gray-500">{{ session.date.strftime('%m/%d') if session.date else 'N/A' }}</p>
                                    <p class="text-sm font-medium text-gray-900">{{ session.time.strftime('%H:%M') if session.time else 'N/A' }}</p>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-gray-500 text-center py-4">No upcoming sessions found</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Plans Overview -->
        <div class="mt-6">
            <div class="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">
                        <i class="fas fa-credit-card text-purple-600 mr-2"></i>Available Plans
                        <span class="text-sm font-normal text-gray-500 ml-2">({{ total_plans }} plans available)</span>
                    </h3>
                </div>
                <div class="p-6">
                    <div class="text-center py-4">
                        <p class="text-gray-600">Sprint 2 will add Members & Plans management interface</p>
                        <div class="mt-4 space-x-4">
                            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                                <i class="fas fa-users mr-1"></i> Members → Sprint 2
                            </span>
                            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                                <i class="fas fa-credit-card mr-1"></i> Plans → Sprint 2
                            </span>
                            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                                <i class="fas fa-user-tie mr-1"></i> Trainers → Sprint 3
                            </span>
                            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                                <i class="fas fa-calendar-alt mr-1"></i> Sessions → Sprint 3
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Error Display (if any) -->
        {% if error %}
        <div class="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex">
                <i class="fas fa-exclamation-triangle text-red-400 mt-1 mr-3"></i>
                <div>
                    <h3 class="text-sm font-medium text-red-800">Database Connection Issue</h3>
                    <p class="text-sm text-red-700 mt-1">{{ error }}</p>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-12">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <div class="text-center">
                <p class="text-gray-600">
                    <i class="fas fa-dumbbell text-blue-600 mr-2"></i>
                    Fitness Club Management System - Sprint 1: Backend + Dashboard
                </p>
                <p class="text-sm text-gray-500 mt-2">
                    Powered by Flask, SQLAlchemy, Tailwind CSS, Font Awesome & Google Fonts
                </p>
            </div>
        </div>
    </footer>
</body>
</html>
```

SPRINT 1 API ENDPOINTS SUMMARY:

✅ **Keep Unchanged:**
- GET / - Welcome page from pre-sprint (HTML)

✅ **Add New Dashboard UI:**
- GET /dashboard - Dashboard UI displaying real statistics and data visualization (HTML)

✅ **Add New API Endpoints (Returning Real Database Data):**
- GET /test - Backend verification with database status (JSON)
- GET /api/stats - Get dashboard statistics from database (JSON)
- GET /api/members - Get all members from database (JSON)
- POST /api/members - Create new member in database (JSON)
- GET /api/plans - Get membership plans from database (JSON)
- GET /api/trainers - Get trainers list from database (JSON)
- GET /api/sessions - Get workout sessions from database (JSON)
- POST /api/sessions/schedule - Schedule session in database (JSON)

IMPORTANT: REAL DATABASE + DASHBOARD UI IN SPRINT 1
- Sprint 1 = Backend API endpoints + Dashboard UI with SQLAlchemy models and real data
- Sprint 2 = Members & Plans Management UI
- Sprint 3 = Trainers & Sessions Management UI + Polish

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
- Prepare foundation for Sprint 2 (Members & Plans Management)

## 🎯 **EXPECTED DELIVERABLES**

✅ **Sprint 1 Backend API + Dashboard Deliverables:**

- **A. src\app.py** - Flask app with API endpoints + Dashboard route + SQLAlchemy integration (keeps existing welcome page)
- **B. src\models.py** - SQLAlchemy models (Member, Plan, Trainer, Session) with relationships
- **C. src\config.py** - Flask configuration with database path
- **D. src\init_db.py** - Database initialization script with realistic seed data
- **E. src\templates\dashboard.html** - Dashboard UI template displaying real statistics and data
- **F. Database** - SQLite database with tables and seed data (src\instance\fitness_club.db)
- **G. API Endpoints** - All endpoints return JSON responses with real database data
- **H. Welcome Page** - Original welcome page unchanged from pre-sprint

✅ **Routes Working (Real Database Data):**

- `GET /` - Welcome page (HTML, unchanged from pre-sprint)
- `GET /dashboard` - Dashboard UI with real statistics and data visualization (HTML)
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

### **Step 4: Test Dashboard UI (NEW for Sprint 1)**

- Open browser to `http://127.0.0.1:5000/dashboard`
- ✅ Verify dashboard displays with real statistics from database
- ✅ Check that all stat cards show actual numbers (not zeros)
- ✅ Confirm recent members and upcoming sessions are displayed
- ✅ Verify professional styling with Tailwind CSS, Font Awesome icons, and Google Fonts

### **Step 5: Test API Endpoints (Real Database Data)**

Open browser or use curl to test these JSON API endpoints:

- `http://127.0.0.1:5000/test` - Should return JSON with database_connected: true
- `http://127.0.0.1:5000/api/members` - Should return 4 real members from database
- `http://127.0.0.1:5000/api/plans` - Should return 3 real plans from database
- `http://127.0.0.1:5000/api/sessions` - Should return 4 real sessions from database
- `http://127.0.0.1:5000/api/trainers` - Should return 3 real trainers from database
- `http://127.0.0.1:5000/api/stats` - Should return real statistics from database

### **Step 6: Verify Dashboard Data and API Responses**

**Dashboard UI should display:**
- Total Members: 4 (from seed data)
- Active Sessions: 4 (from seed data)
- Active Trainers: 3 (from seed data)
- Monthly Revenue: Real calculated amount
- Recent Members: List of actual members
- Upcoming Sessions: List of actual sessions

**API endpoints should return real data like:**

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

**✅ ALL CHECKS PASSED?** → **Ready for Sprint 2: Members & Plans Management!**
**❌ ANY FAILURES?** → **Review API endpoints and fix issues**

**Sprint 1 Success Indicators:**
- A. Welcome page unchanged from pre-sprint (HTML with styling)
- B. Dashboard UI displays real statistics and data from database
- C. Database created and populated with seed data (SQLite)
- D. All API endpoints return JSON responses with real database data
- E. SQLAlchemy models working with proper relationships
- F. Professional dashboard styling with Tailwind CSS, Font Awesome icons, and Google Fonts
- G. Backend structure ready for Sprint 2 (Members & Plans Management UI)

---

## 🚀 **SPRINT 1 COMPLETE - NEXT STEPS**

Once Sprint 1 verification passes, you're ready for:

**Sprint 2: Members & Plans Management UI** - Create full CRUD interfaces for members and membership plans with forms, validation, and data tables
**Sprint 3: Trainers & Sessions Management UI + Polish** - Add trainer management, session scheduling UI, and final integration polish

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre-Sprint-Setup.md) - 🛠 Environment Setup
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Members & Plans Management UI
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Trainers & Sessions UI + Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 📚 **QUICK ACCESS TO OTHER PROMPTS**

- [2_Pre-Sprint-Setup.md](2_Pre_Sprint-Setup.md) - 🔧 Setup & Environment
- [4_Sprint2-Frontend.md](4_Sprint2-Frontend.md) - 🎨 Members & Plans Management UI
- [5_Sprint3-Integration.md](5_Sprint3-Integration.md) - 🔗 Trainers & Sessions UI + Polish
- [45-minute-live-coding-guide.md](45-minute-live-coding-guide.md) - 🎬 Live Demo Guide

## 🎯 **NEXT STEP**

After completing Sprint 1, proceed to: **[4_Sprint2-Frontend.md](4_Sprint2-Frontend.md)** - Members & Plans Management UI
````
