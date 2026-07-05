import csv
import io
from urllib.parse import quote_plus
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, or_, func, text

import config

app = Flask(__name__)
app.secret_key = 'super_secret_college_event_key'

# Configure SQLAlchemy to connect to MySQL database
DB_NAME = 'collegedb'
encoded_password = quote_plus('Root@123')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@127.0.0.1/{DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
}

db = SQLAlchemy(app)

@app.context_processor
def inject_college_info():
    return {
        'college_name': config.COLLEGE_NAME,
        'college_full_name': config.COLLEGE_FULL_NAME,
        'college_tagline': config.COLLEGE_TAGLINE,
        'college_email': config.COLLEGE_EMAIL,
        'college_phone': config.COLLEGE_PHONE,
        'college_address': config.COLLEGE_ADDRESS,
    }

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(300), nullable=False)
    max_capacity = db.Column(db.Integer, default=50)
    current_registrations = db.Column(db.Integer, default=0)
    registrations = db.relationship('Registration', backref='event', cascade='all, delete-orphan')


class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    student_name = db.Column(db.String(200), nullable=False)
    student_email = db.Column(db.String(200), nullable=False)
    student_roll = db.Column(db.String(50), nullable=False)
    student_branch = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.DateTime, server_default=func.current_timestamp())

def init_db():
    """Create tables and prepopulate default events if none exist."""
    with app.app_context():
        server_engine = create_engine(f'mysql+pymysql://root:{encoded_password}@127.0.0.1/?charset=utf8mb4')
        with server_engine.begin() as conn:
            conn.execute(text(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}'))

        db.create_all()

        if Event.query.count() == 0:
            sample_events = [
                Event(
                    title="CodeCraft Hackathon",
                    category="Technical",
                    description=(
                        "Showcase your programming and problem-solving skills in this 24-hour national hackathon. "
                        "Build innovative solutions for real-world challenges."
                    ),
                    date="2026-07-15",
                    time="09:00",
                    venue="Computer Lab 3, IT Block",
                    max_capacity=80,
                ),
                Event(
                    title="Inter-College Cricket Cup",
                    category="Sports",
                    description=(
                        "The annual cricket championship where top college teams clash for the ultimate trophy. "
                        "Exciting matches, trophy rewards, and certificates."
                    ),
                    date="2026-07-25",
                    time="08:30",
                    venue="College Main Ground",
                    max_capacity=150,
                ),
                Event(
                    title="Symphony Music & Dance Fest",
                    category="Cultural",
                    description=(
                        "Celebrate art and expression! An evening filled with classical, rock music performances and diverse group dance forms."
                    ),
                    date="2026-07-20",
                    time="17:00",
                    venue="Main Auditorium",
                    max_capacity=200,
                ),
                Event(
                    title="Ideathon: Startup Pitch",
                    category="Competitions",
                    description=(
                        "Got a business idea? Pitch it to top venture capitalists and industry mentors. "
                        "Cash prizes up to $5000 for the winning startup pitch."
                    ),
                    date="2026-07-18",
                    time="11:00",
                    venue="Seminar Hall B, Block A",
                    max_capacity=50,
                ),
            ]
            db.session.add_all(sample_events)
            db.session.commit()
            print("Database initialized and populated with sample events.")

# ----------------- ROUTES -----------------

@app.route('/')
def index():
    """Home page routing: shows all events with optional filters."""
    current_category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'date')
    
    # Build base query
    q = Event.query

    if current_category:
        q = q.filter(Event.category == current_category)

    if search_query:
        search_pattern = f"%{search_query}%"
        q = q.filter(
            or_(
                Event.title.ilike(search_pattern),
                Event.venue.ilike(search_pattern),
                Event.description.ilike(search_pattern),
            )
        )

    order_map = {
        'date': Event.date.asc(),
        'title': Event.title.asc(),
        'category': Event.category.asc(),
    }
    events = q.order_by(order_map.get(sort_by, Event.date.asc())).all()

    total_events = Event.query.count()
    total_categories = db.session.query(func.count(func.distinct(Event.category))).scalar() or 0
    total_registrations = Registration.query.count()

    return render_template(
        'index.html',
        events=events,
        current_category=current_category,
        search_query=search_query,
        sort_by=sort_by,
        total_events=total_events,
        total_categories=total_categories,
        total_registrations=total_registrations,
    )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    """Handles student registration form and DB persistence."""
    event = Event.query.get(event_id)
    if not event:
        flash('Event not found.', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        student_email = request.form.get('student_email', '').strip().lower()
        student_roll = request.form.get('student_roll', '').strip().upper()
        student_branch = request.form.get('student_branch', '').strip()

        if not all([student_name, student_email, student_roll, student_branch]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('register', event_id=event_id))
        
        # 1. Validation: Capacity check
        if event.current_registrations >= event.max_capacity:
            flash('Failed to register. Event capacity is already full!', 'error')
            return redirect(url_for('index'))
            
        # 2. Validation: Duplicate registration check
        duplicate = Registration.query.filter(
            Registration.event_id == event_id,
            or_(Registration.student_email == student_email, Registration.student_roll == student_roll),
        ).first()

        if duplicate:
            flash('You are already registered for this event!', 'error')
            return redirect(url_for('index'))

        # 3. Save registration
        reg = Registration(
            event_id=event_id,
            student_name=student_name,
            student_email=student_email,
            student_roll=student_roll,
            student_branch=student_branch,
        )
        db.session.add(reg)

        # 4. Increment registration count
        event.current_registrations = (event.current_registrations or 0) + 1
        db.session.commit()

        flash(f'Success! You have successfully registered for "{event.title}".', 'success')
        return redirect(url_for('index'))
        
    return render_template('register.html', event=event)


# ----------------- ADMIN ROUTES -----------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin portal login screen."""
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        # Professional standard admin authentication (simple demo credentials)
        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in as administrator.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin session logout."""
    session.pop('admin_logged_in', None)
    flash('You have logged out successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/admin')
def admin_dashboard():
    """Admin control dashboard panel."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    events = Event.query.order_by(Event.date.asc()).all()

    registrations = (
        db.session.query(Registration, Event.title.label('event_title'))
        .join(Event)
        .order_by(Registration.registration_date.desc())
        .all()
    )

    # registrations is list of tuples (Registration, event_title)
    category_count = len({e.category for e in events})

    return render_template(
        'admin.html',
        events=events,
        registrations=registrations,
        category_count=category_count,
    )


@app.route('/admin/add_event', methods=['POST'])
def add_event():
    """Enables admin to append new events into the system."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    venue = request.form.get('venue', '').strip()
    date = request.form.get('date', '').strip()
    time = request.form.get('time', '').strip()

    try:
        max_capacity = int(request.form.get('max_capacity', 0))
    except ValueError:
        max_capacity = 0

    if not all([title, category, description, venue, date, time]) or max_capacity < 1:
        flash('Please provide valid event details. Capacity must be at least 1.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Basic date formatting (YYYY-MM-DD to cleaner layout if needed, we can keep simple input date)
    ev = Event(
        title=title,
        category=category,
        description=description,
        date=date,
        time=time,
        venue=venue,
        max_capacity=max_capacity,
        current_registrations=0,
    )
    db.session.add(ev)
    db.session.commit()

    flash(f'Event "{title}" was successfully created.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    """Enables admin to remove an event and associated registrations."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    event = Event.query.get(event_id)
    if event:
        title = event.title
        db.session.delete(event)
        db.session.commit()
        flash(f'Event "{title}" and its student registrations were deleted.', 'success')
    else:
        flash('Event not found.', 'error')

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/export_csv')
def export_csv():
    """Generates a downloadable CSV of all registrations."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    registrations = (
        db.session.query(Registration, Event.title.label('event_title'))
        .join(Event)
        .order_by(Event.title, Registration.student_name)
        .all()
    )

    # Build CSV in memory
    si = io.StringIO()
    cw = csv.writer(si)

    # CSV Header
    cw.writerow(['Student Name', 'Email Address', 'Roll Number', 'Branch/Department', 'Registered Event', 'Registration Date'])

    # Write Rows
    for reg, event_title in registrations:
        cw.writerow([
            reg.student_name,
            reg.student_email,
            reg.student_roll,
            reg.student_branch,
            event_title,
            reg.registration_date,
        ])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=event_registrations.csv"
    output.headers["Content-Type"] = "text/csv"
    return output

# ------------------------------------------

if __name__ == '__main__':
    init_db()
    # Run the server on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
