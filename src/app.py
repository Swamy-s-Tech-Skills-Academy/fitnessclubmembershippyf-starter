from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from decimal import Decimal
import os
import csv
import io

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
    trainer_id = db.Column(db.Integer, db.ForeignKey(
        'trainers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    # Session duration in minutes
    duration_minutes = db.Column(db.Integer, default=60)
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
    session_id = db.Column(db.Integer, db.ForeignKey(
        'sessions.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    # enrolled, cancelled, completed
    status = db.Column(db.String(20), default='enrolled')

    # Relationships
    session = db.relationship('Session', backref='enrollments')
    member = db.relationship('Member', backref='session_enrollments')

    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint(
        'session_id', 'member_id', name='unique_session_member'),)

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
        recent_members = Member.query.order_by(
            Member.join_date.desc()).limit(5).all()

        # Get upcoming sessions
        upcoming_sessions = Session.query.filter_by(status='active').order_by(
            Session.date, Session.time).limit(5).all()

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
            date=datetime.fromisoformat(
                data.get('date')) if data.get('date') else None,
            time=datetime.strptime(data.get('time'), '%H:%M').time(
            ) if data.get('time') else None,
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


# SPRINT 2: MEMBERS MANAGEMENT UI ROUTES

@app.route('/members')
def members_list():
    """Members list page with search and filter capabilities"""
    try:
        # Get search and filter parameters
        search = request.args.get('search', '').strip()
        status_filter = request.args.get('status', '')
        plan_filter = request.args.get('plan_id', '')

        # Base query
        query = Member.query

        # Apply search filter
        if search:
            query = query.filter(
                db.or_(
                    Member.name.contains(search),
                    Member.email.contains(search),
                    Member.phone.contains(search)
                )
            )

        # Apply status filter
        if status_filter:
            query = query.filter(Member.status == status_filter)

        # Apply plan filter
        if plan_filter:
            query = query.filter(Member.plan_id == plan_filter)

        # Get members with pagination support
        members = query.order_by(Member.join_date.desc()).all()

        # Get all plans for filter dropdown
        plans = Plan.query.all()

        return render_template('members/list.html',
                               members=members,
                               plans=plans,
                               search=search,
                               status_filter=status_filter,
                               plan_filter=plan_filter)

    except Exception as e:
        flash(f'Error loading members: {str(e)}', 'error')
        return render_template('members/list.html', members=[], plans=[])


@app.route('/members/create', methods=['GET', 'POST'])
def members_create():
    """Member creation form"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            plan_id = request.form.get('plan_id')
            status = request.form.get('status', 'active')

            # Basic validation
            if not name or not email:
                flash('Name and email are required', 'error')
                return redirect(url_for('members_create'))

            # Check if email already exists
            existing_member = Member.query.filter_by(email=email).first()
            if existing_member:
                flash('A member with this email already exists', 'error')
                return redirect(url_for('members_create'))

            # Create new member
            new_member = Member(
                name=name,
                email=email,
                phone=phone if phone else None,
                plan_id=int(plan_id) if plan_id else None,
                status=status,
                join_date=datetime.now().date()
            )

            db.session.add(new_member)
            db.session.commit()

            flash(f'Member {name} created successfully!', 'success')
            return redirect(url_for('members_detail', id=new_member.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating member: {str(e)}', 'error')
            return redirect(url_for('members_create'))

    # GET request - show form
    plans = Plan.query.all()
    return render_template('members/create.html', plans=plans)


@app.route('/members/<int:id>')
def members_detail(id):
    """Member detail page"""
    try:
        member = Member.query.get_or_404(id)
        return render_template('members/detail.html', member=member)
    except Exception as e:
        flash(f'Error loading member details: {str(e)}', 'error')
        return redirect(url_for('members_list'))


@app.route('/members/<int:id>/edit', methods=['GET', 'POST'])
def edit_member(id):
    """Member edit form"""
    try:
        member = Member.query.get_or_404(id)

        if request.method == 'POST':
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            plan_id = request.form.get('plan_id')
            status = request.form.get('status', 'active')

            # Basic validation
            if not name or not email:
                flash('Name and email are required', 'error')
                return redirect(url_for('edit_member', id=id))

            # Check if email already exists (excluding current member)
            existing_member = Member.query.filter(
                Member.email == email,
                Member.id != id
            ).first()
            if existing_member:
                flash('A member with this email already exists', 'error')
                return redirect(url_for('edit_member', id=id))

            # Update member
            member.name = name
            member.email = email
            member.phone = phone if phone else None
            member.plan_id = int(plan_id) if plan_id else None
            member.status = status

            db.session.commit()

            flash(f'Member {name} updated successfully!', 'success')
            return redirect(url_for('members_detail', id=id))

        # GET request - show form
        plans = Plan.query.all()
        return render_template('members/edit.html', member=member, plans=plans)

    except Exception as e:
        db.session.rollback()
        flash(f'Error updating member: {str(e)}', 'error')
        return redirect(url_for('members_list'))


@app.route('/members/export')
def export_members():
    """Export members data to CSV"""
    try:
        members = Member.query.all()

        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['ID', 'Name', 'Email', 'Phone',
                        'Join Date', 'Plan', 'Status'])

        # Write member data
        for member in members:
            writer.writerow([
                member.id,
                member.name,
                member.email,
                member.phone or '',
                member.join_date.strftime(
                    '%Y-%m-%d') if member.join_date else '',
                member.plan.name if member.plan else '',
                member.status
            ])

        # Create response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers[
            'Content-Disposition'] = f'attachment; filename=members_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

        return response

    except Exception as e:
        flash(f'Error exporting members: {str(e)}', 'error')
        return redirect(url_for('members_list'))


# SPRINT 2: PLANS MANAGEMENT UI ROUTES

@app.route('/plans')
def plans_list():
    """Plans list page"""
    try:
        plans = Plan.query.all()
        return render_template('plans/list.html', plans=plans)
    except Exception as e:
        flash(f'Error loading plans: {str(e)}', 'error')
        return render_template('plans/list.html', plans=[])


@app.route('/plans/create', methods=['GET', 'POST'])
def plans_create():
    """Plan creation form"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', '').strip()
            duration_months = request.form.get('duration_months', '').strip()
            features = request.form.get('features', '').strip()

            # Basic validation
            if not name or not price or not duration_months:
                flash('Name, price, and duration are required', 'error')
                return redirect(url_for('plans_create'))

            try:
                price = float(price)
                duration_months = int(duration_months)
            except ValueError:
                flash('Invalid price or duration format', 'error')
                return redirect(url_for('plans_create'))

            # Create new plan
            new_plan = Plan(
                name=name,
                description=description if description else None,
                price=Decimal(str(price)),
                duration_months=duration_months,
                features=features if features else None
            )

            db.session.add(new_plan)
            db.session.commit()

            flash(f'Plan "{name}" created successfully!', 'success')
            return redirect(url_for('plans_detail', id=new_plan.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating plan: {str(e)}', 'error')
            return redirect(url_for('plans_create'))

    # GET request - show form
    return render_template('plans/create.html')


@app.route('/plans/<int:id>')
def plans_detail(id):
    """Plan detail page"""
    try:
        plan = Plan.query.get_or_404(id)
        return render_template('plans/detail.html', plan=plan)
    except Exception as e:
        flash(f'Error loading plan details: {str(e)}', 'error')
        return redirect(url_for('plans_list'))


@app.route('/plans/<int:id>/edit', methods=['GET', 'POST'])
def edit_plan(id):
    """Plan edit form"""
    try:
        plan = Plan.query.get_or_404(id)

        if request.method == 'POST':
            # Get form data
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', '').strip()
            duration_months = request.form.get('duration_months', '').strip()
            features = request.form.get('features', '').strip()

            # Basic validation
            if not name or not price or not duration_months:
                flash('Name, price, and duration are required', 'error')
                return redirect(url_for('edit_plan', id=id))

            try:
                price = float(price)
                duration_months = int(duration_months)
            except ValueError:
                flash('Invalid price or duration format', 'error')
                return redirect(url_for('edit_plan', id=id))

            # Update plan
            plan.name = name
            plan.description = description if description else None
            plan.price = Decimal(str(price))
            plan.duration_months = duration_months
            plan.features = features if features else None

            db.session.commit()

            flash(f'Plan "{name}" updated successfully!', 'success')
            return redirect(url_for('plans_detail', id=id))

        # GET request - show form
        return render_template('plans/edit.html', plan=plan)

    except Exception as e:
        db.session.rollback()
        flash(f'Error updating plan: {str(e)}', 'error')
        return redirect(url_for('plans_list'))


@app.route('/plans/export')
def export_plans():
    """Export plans data to CSV"""
    try:
        plans = Plan.query.all()

        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['ID', 'Name', 'Description', 'Price',
                        'Duration (Months)', 'Features', 'Member Count'])

        # Write plan data
        for plan in plans:
            writer.writerow([
                plan.id,
                plan.name,
                plan.description or '',
                float(plan.price),
                plan.duration_months,
                plan.features or '',
                plan.member_count
            ])

        # Create response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers[
            'Content-Disposition'] = f'attachment; filename=plans_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

        return response

    except Exception as e:
        flash(f'Error exporting plans: {str(e)}', 'error')
        return redirect(url_for('plans_list'))


# Sprint 1: Backend API endpoints returning real database data

if __name__ == '__main__':
    # Ensure instance directory exists
    instance_dir = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000)
