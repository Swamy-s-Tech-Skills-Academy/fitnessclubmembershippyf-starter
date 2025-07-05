from decimal import Decimal
from datetime import datetime, date, time
from app import app, db, Member, Plan, Trainer, Session, SessionEnrollment
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def init_database():
    """Initialize database with seed data"""
    with app.app_context():
        # Create all tables
        db.create_all()

        # Clear existing data (for development)
        db.session.query(SessionEnrollment).delete()
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
                enrolled=4,
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
                enrolled=4,
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
                enrolled=3,
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
                enrolled=3,
                status='active'
            )
        ]

        for session in sessions:
            db.session.add(session)

        db.session.commit()

        # Create session enrollments (matching the enrolled counts in sessions)
        enrollments = [
            # Morning Yoga (session_id=1, enrolled=4)
            SessionEnrollment(session_id=1, member_id=1, status='enrolled'),
            SessionEnrollment(session_id=1, member_id=2, status='enrolled'),
            SessionEnrollment(session_id=1, member_id=3, status='enrolled'),
            SessionEnrollment(session_id=1, member_id=4, status='enrolled'),

            # HIIT Workout (session_id=2, enrolled=4)
            SessionEnrollment(session_id=2, member_id=1, status='enrolled'),
            SessionEnrollment(session_id=2, member_id=2, status='enrolled'),
            SessionEnrollment(session_id=2, member_id=3, status='enrolled'),
            SessionEnrollment(session_id=2, member_id=4, status='enrolled'),

            # Strength Training (session_id=3, enrolled=3)
            SessionEnrollment(session_id=3, member_id=1, status='enrolled'),
            SessionEnrollment(session_id=3, member_id=2, status='enrolled'),
            SessionEnrollment(session_id=3, member_id=3, status='enrolled'),

            # Evening Pilates (session_id=4, enrolled=3)
            SessionEnrollment(session_id=4, member_id=1, status='enrolled'),
            SessionEnrollment(session_id=4, member_id=2, status='enrolled'),
            SessionEnrollment(session_id=4, member_id=4, status='enrolled'),
        ]

        for enrollment in enrollments:
            db.session.add(enrollment)

        db.session.commit()

        print("Database initialized successfully!")
        print(f"Created {len(plans)} plans")
        print(f"Created {len(trainers)} trainers")
        print(f"Created {len(members)} members")
        print(f"Created {len(sessions)} sessions")
        print(f"Created {len(enrollments)} session enrollments")


if __name__ == '__main__':
    init_database()
