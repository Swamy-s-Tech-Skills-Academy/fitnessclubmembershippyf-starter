from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from decimal import Decimal
import os
import csv
from io import StringIO

app = Flask(__name__)

# Configuration (inline to avoid se@app.route('/api/sessions', methods=['GET'])arate config file)
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
    capacity = db.Column(db.Integer, default=10)
    enrolled = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')

    # Relationship
    trainer = db.relationship('Trainer', backref='sessions')

    def __repr__(self):
        return f'<Session {self.title}>'


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


# Sprint 2: Members Management UI Routes

@app.route('/members')
def members_list():
    """Members list page with search and filtering"""
    try:
        # Get search parameters
        search = request.args.get('search', '')
        status_filter = request.args.get('status', '')
        plan_filter = request.args.get('plan', '')

        # Build query
        query = Member.query

        if search:
            query = query.filter(Member.name.contains(
                search) | Member.email.contains(search))
        if status_filter:
            query = query.filter(Member.status == status_filter)
        if plan_filter:
            query = query.filter(Member.plan_id == plan_filter)

        members = query.order_by(Member.join_date.desc()).all()
        plans = Plan.query.all()

        return render_template('members/list.html',
                               members=members,
                               plans=plans,
                               search=search,
                               status_filter=status_filter,
                               plan_filter=plan_filter)
    except Exception as e:
        return render_template('members/list.html',
                               members=[],
                               plans=[],
                               error=str(e))


@app.route('/members/create', methods=['GET', 'POST'])
def members_create():
    """Create new member page"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            plan_id = request.form.get(
                'plan_id') if request.form.get('plan_id') else None

            # Validate required fields
            if not name or not email:
                raise ValueError("Name and email are required")

            # Create new member
            new_member = Member(
                name=name,
                email=email,
                phone=phone,
                plan_id=int(plan_id) if plan_id else None,
                status='active'
            )

            db.session.add(new_member)
            db.session.commit()

            return render_template('members/create.html',
                                   plans=Plan.query.all(),
                                   success="Member created successfully!")
        except Exception as e:
            return render_template('members/create.html',
                                   plans=Plan.query.all(),
                                   error=str(e))

    # GET request
    plans = Plan.query.all()
    return render_template('members/create.html', plans=plans)


@app.route('/members/<int:member_id>')
def members_detail(member_id):
    """Member detail page"""
    try:
        member = Member.query.get_or_404(member_id)
        return render_template('members/detail.html', member=member)
    except Exception as e:
        return render_template('members/detail.html', member=None, error=str(e))


@app.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def members_edit(member_id):
    """Edit member page"""
    member = Member.query.get_or_404(member_id)

    if request.method == 'POST':
        try:
            # Update member data
            member.name = request.form.get('name')
            member.email = request.form.get('email')
            member.phone = request.form.get('phone')
            member.plan_id = int(request.form.get(
                'plan_id')) if request.form.get('plan_id') else None
            member.status = request.form.get('status')

            db.session.commit()

            return render_template('members/edit.html',
                                   member=member,
                                   plans=Plan.query.all(),
                                   success="Member updated successfully!")
        except Exception as e:
            return render_template('members/edit.html',
                                   member=member,
                                   plans=Plan.query.all(),
                                   error=str(e))

    # GET request
    plans = Plan.query.all()
    return render_template('members/edit.html', member=member, plans=plans)

# Sprint 2: Plans Management UI Routes


@app.route('/plans')
def plans_list():
    """Plans list page"""
    try:
        plans = Plan.query.all()
        print(f"DEBUG: Found {len(plans)} plans in database")

        # Add member count for each plan
        for plan in plans:
            print(f"DEBUG: Processing plan {plan.name}")
            print(f"DEBUG: Plan members: {plan.members}")
            plan.member_count = len(
                [m for m in plan.members if m.status == 'active'])
            plan.monthly_revenue = plan.member_count * float(plan.price)
            print(
                f"DEBUG: Plan {plan.name} has {plan.member_count} active members")

        print(f"DEBUG: Passing {len(plans)} plans to template")
        return render_template('plans/list.html', plans=plans)
    except Exception as e:
        print(f"DEBUG: Error in plans_list: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('plans/list.html', plans=[], error=str(e))


@app.route('/plans/create', methods=['GET', 'POST'])
def plans_create():
    """Create new plan page"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            duration_months = request.form.get('duration_months')
            features = request.form.get('features')

            # Validate required fields
            if not name or not price or not duration_months:
                raise ValueError("Name, price, and duration are required")

            # Create new plan
            new_plan = Plan(
                name=name,
                description=description,
                price=Decimal(price),
                duration_months=int(duration_months),
                features=features
            )

            db.session.add(new_plan)
            db.session.commit()

            return render_template('plans/create.html',
                                   success="Plan created successfully!")
        except Exception as e:
            return render_template('plans/create.html', error=str(e))

    # GET request
    return render_template('plans/create.html')


@app.route('/plans/<int:plan_id>')
def plans_detail(plan_id):
    """Plan detail page"""
    try:
        plan = Plan.query.get_or_404(plan_id)

        # Get additional data for the template
        total_members = Member.query.count()
        other_plans = Plan.query.filter(Plan.id != plan_id).all()

        # Calculate analytics data
        active_members = [m for m in plan.members if m.status == 'active']
        plan.member_count = len(active_members)
        plan.monthly_revenue = plan.member_count * float(plan.price)

        return render_template('plans/detail.html',
                               plan=plan,
                               active_members=active_members,
                               total_members=total_members,
                               other_plans=other_plans)
    except Exception as e:
        return render_template('plans/detail.html', plan=None, error=str(e))


@app.route('/plans/<int:plan_id>/edit', methods=['GET', 'POST'])
def plans_edit(plan_id):
    """Edit plan page"""
    plan = Plan.query.get_or_404(plan_id)

    if request.method == 'POST':
        try:
            # Update plan data
            plan.name = request.form.get('name')
            plan.description = request.form.get('description')
            plan.price = Decimal(request.form.get('price'))
            plan.duration_months = int(request.form.get('duration_months'))
            plan.features = request.form.get('features')

            db.session.commit()

            return render_template('plans/edit.html',
                                   plan=plan,
                                   success="Plan updated successfully!")
        except Exception as e:
            return render_template('plans/edit.html',
                                   plan=plan,
                                   error=str(e))

    # GET request
    return render_template('plans/edit.html', plan=plan)

# Sprint 2: Export functionality


@app.route('/members/export')
def members_export():
    """Export members to CSV"""
    try:
        members = Member.query.all()

        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['ID', 'Name', 'Email', 'Phone',
                        'Join Date', 'Plan', 'Status'])

        # Write data
        for member in members:
            plan_name = member.plan.name if member.plan else 'No Plan'
            writer.writerow([
                member.id,
                member.name,
                member.email,
                member.phone or '',
                member.join_date.strftime(
                    '%Y-%m-%d') if member.join_date else '',
                plan_name,
                member.status
            ])

        output.seek(0)

        response = make_response(output.getvalue())
        response.headers[
            "Content-Disposition"] = f"attachment; filename=members_{datetime.now().strftime('%Y%m%d')}.csv"
        response.headers["Content-type"] = "text/csv"

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/plans/export')
def plans_export():
    """Export plans to CSV"""
    try:
        plans = Plan.query.all()

        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['ID', 'Name', 'Description', 'Price',
                        'Duration (Months)', 'Features', 'Active Members'])

        # Write data
        for plan in plans:
            member_count = len(
                [m for m in plan.members if m.status == 'active'])
            writer.writerow([
                plan.id,
                plan.name,
                plan.description or '',
                float(plan.price),
                plan.duration_months,
                plan.features or '',
                member_count
            ])

        output.seek(0)

        response = make_response(output.getvalue())
        response.headers[
            "Content-Disposition"] = f"attachment; filename=plans_{datetime.now().strftime('%Y%m%d')}.csv"
        response.headers["Content-type"] = "text/csv"

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete routes for members and plans


@app.route('/members/<int:id>/delete', methods=['POST'])
def delete_member(id):
    """Delete a member"""
    try:
        member = Member.query.get_or_404(id)
        member_name = member.full_name

        # Delete the member
        db.session.delete(member)
        db.session.commit()

        flash(
            f'Member "{member_name}" has been deleted successfully.', 'success')
        return redirect(url_for('members_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting member: {str(e)}', 'error')
        return redirect(url_for('members_detail', member_id=id))


@app.route('/plans/<int:id>/delete', methods=['POST'])
def delete_plan(id):
    """Delete a plan (only if no members are using it)"""
    try:
        plan = Plan.query.get_or_404(id)

        # Check if any members are using this plan
        if plan.members:
            flash(
                f'Cannot delete plan "{plan.name}" because {len(plan.members)} member(s) are currently using it.', 'error')
            return redirect(url_for('plans_detail', plan_id=id))

        plan_name = plan.name

        # Delete the plan
        db.session.delete(plan)
        db.session.commit()

        flash(f'Plan "{plan_name}" has been deleted successfully.', 'success')
        return redirect(url_for('plans_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting plan: {str(e)}', 'error')
        return redirect(url_for('plans_detail', plan_id=id))


if __name__ == '__main__':
    app.run(debug=True)
