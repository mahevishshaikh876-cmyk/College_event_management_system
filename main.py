import sqlite3
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import config

app = Flask(__name__)
app.secret_key = 'super_secret_college_event_key'

DATABASE = 'events.db'

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

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    """Initialize the database schema and add default events if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            venue TEXT NOT NULL,
            max_capacity INTEGER DEFAULT 50,
            current_registrations INTEGER DEFAULT 0
        )
    ''')
    
    # Create registrations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL,
            student_roll TEXT NOT NULL,
            student_branch TEXT NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

    # Prepopulate default events if table is empty
    cursor.execute('SELECT COUNT(*) FROM events')
    if cursor.fetchone()[0] == 0:
        sample_events = [
            (
                "CodeCraft Hackathon", 
                "Technical", 
                "Showcase your programming and problem-solving skills in this 24-hour national hackathon. Build innovative solutions for real-world challenges.",
                "2026-07-15", 
                "09:00", 
                "Computer Lab 3, IT Block",
                80, 
                0
            ),
            (
                "Inter-College Cricket Cup", 
                "Sports", 
                "The annual cricket championship where top college teams clash for the ultimate trophy. Exciting matches, trophy rewards, and certificates.",
                "2026-07-25", 
                "08:30", 
                "College Main Ground",
                150, 
                0
            ),
            (
                "Symphony Music & Dance Fest", 
                "Cultural", 
                "Celebrate art and expression! An evening filled with classical, rock music performances and diverse group dance forms.",
                "2026-07-20", 
                "17:00", 
                "Main Auditorium",
                200, 
                0
            ),
            (
                "Ideathon: Startup Pitch", 
                "Competitions", 
                "Got a business idea? Pitch it to top venture capitalists and industry mentors. Cash prizes up to $5000 for the winning startup pitch.",
                "2026-07-18", 
                "11:00", 
                "Seminar Hall B, Block A",
                50, 
                0
            )
        ]
        cursor.executemany('''
            INSERT INTO events (title, category, description, date, time, venue, max_capacity, current_registrations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_events)
        conn.commit()
        print("Database initialized and populated with sample events.")
        
    conn.close()

# ----------------- ROUTES -----------------

@app.route('/')
def index():
    """Home page routing: shows all events with optional filters."""
    current_category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM events WHERE 1=1"
    params = []
    
    if current_category:
        query += " AND category = ?"
        params.append(current_category)
        
    if search_query:
        query += " AND (title LIKE ? OR venue LIKE ? OR description LIKE ?)"
        search_pattern = f"%{search_query}%"
        params.extend([search_pattern, search_pattern, search_pattern])

    order_map = {'date': 'date ASC', 'title': 'title ASC', 'category': 'category ASC'}
    query += f" ORDER BY {order_map.get(sort_by, 'date ASC')}"
    
    events = cursor.execute(query, params).fetchall()
    total_events = cursor.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    total_categories = cursor.execute('SELECT COUNT(DISTINCT category) FROM events').fetchone()[0]
    total_registrations = cursor.execute('SELECT COUNT(*) FROM registrations').fetchone()[0]
    conn.close()
    
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    event = cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    
    if not event:
        conn.close()
        flash('Event not found.', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        student_email = request.form.get('student_email', '').strip().lower()
        student_roll = request.form.get('student_roll', '').strip().upper()
        student_branch = request.form.get('student_branch', '').strip()

        if not all([student_name, student_email, student_roll, student_branch]):
            conn.close()
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('register', event_id=event_id))
        
        # 1. Validation: Capacity check
        if event['current_registrations'] >= event['max_capacity']:
            conn.close()
            flash('Failed to register. Event capacity is already full!', 'error')
            return redirect(url_for('index'))
            
        # 2. Validation: Duplicate registration check
        duplicate = cursor.execute('''
            SELECT * FROM registrations 
            WHERE event_id = ? AND (student_email = ? OR student_roll = ?)
        ''', (event_id, student_email, student_roll)).fetchone()
        
        if duplicate:
            conn.close()
            flash('You are already registered for this event!', 'error')
            return redirect(url_for('index'))
            
        # 3. Save registration
        cursor.execute('''
            INSERT INTO registrations (event_id, student_name, student_email, student_roll, student_branch)
            VALUES (?, ?, ?, ?, ?)
        ''', (event_id, student_name, student_email, student_roll, student_branch))
        
        # 4. Increment registration count
        cursor.execute('''
            UPDATE events 
            SET current_registrations = current_registrations + 1 
            WHERE id = ?
        ''', (event_id,))
        
        conn.commit()
        conn.close()
        
        flash(f'Success! You have successfully registered for "{event["title"]}".', 'success')
        return redirect(url_for('index'))
        
    conn.close()
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
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    events = cursor.execute('SELECT * FROM events ORDER BY date ASC').fetchall()
    
    # Retrieve student registrations with matching event information
    registrations = cursor.execute('''
        SELECT r.*, e.title as event_title 
        FROM registrations r
        JOIN events e ON r.event_id = e.id
        ORDER BY r.registration_date DESC
    ''').fetchall()

    category_count = len({event['category'] for event in events})
    
    conn.close()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (title, category, description, date, time, venue, max_capacity, current_registrations)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
    ''', (title, category, description, date, time, venue, max_capacity))
    
    conn.commit()
    conn.close()
    
    flash(f'Event "{title}" was successfully created.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    """Enables admin to remove an event and associated registrations."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Retrieve title for flash notification
    event = cursor.execute('SELECT title FROM events WHERE id = ?', (event_id,)).fetchone()
    if event:
        # SQLite Foreign Key cascading setup or manual deleting of registrations first
        cursor.execute('DELETE FROM registrations WHERE event_id = ?', (event_id,))
        cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
        conn.commit()
        flash(f'Event "{event["title"]}" and its student registrations were deleted.', 'success')
    else:
        flash('Event not found.', 'error')
        
    conn.close()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/export_csv')
def export_csv():
    """Generates a downloadable CSV of all registrations."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    registrations = cursor.execute('''
        SELECT r.student_name, r.student_email, r.student_roll, r.student_branch, e.title as event_title, r.registration_date 
        FROM registrations r
        JOIN events e ON r.event_id = e.id
        ORDER BY e.title, r.student_name
    ''').fetchall()
    conn.close()
    
    # Build CSV in memory
    si = io.StringIO()
    cw = csv.writer(si)
    
    # CSV Header
    cw.writerow(['Student Name', 'Email Address', 'Roll Number', 'Branch/Department', 'Registered Event', 'Registration Date'])
    
    # Write Rows
    for reg in registrations:
        cw.writerow([
            reg['student_name'], 
            reg['student_email'], 
            reg['student_roll'], 
            reg['student_branch'], 
            reg['event_title'], 
            reg['registration_date']
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
