from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# MySQL DB configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',
    'db': 'your_database',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Decorator to require login
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check user role
def roles_required(*roles):
    from functools import wraps
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] not in roles:
                flash("You are not authorized to access this page.")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def index():
    return redirect(url_for('login'))

# Registration route - new users are created with the "viewer" role by default.
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, hashed_password, 'viewer'))
            connection.commit()
            flash("Registration successful. Please login.")
            return redirect(url_for('login'))
        finally:
            connection.close()
    return render_template('register.html')

# Login route with password verification.
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_role'] = user['role']
                flash("Logged in successfully!")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials.")
                return redirect(url_for('login'))
        finally:
            connection.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# Dashboard accessible to all logged in users.
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', role=session.get('user_role'))

# Admin panel to assign roles - accessible only by admin.
@app.route('/admin', methods=['GET','POST'])
@login_required
@roles_required('admin')
def admin_panel():
    connection = pymysql.connect(**db_config)
    if request.method == 'POST':
        user_id = request.form['user_id']
        role = request.form['role']
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET role = %s WHERE id = %s"
                cursor.execute(sql, (role, user_id))
            connection.commit()
            flash("User role updated successfully.")
        finally:
            connection.close()
        return redirect(url_for('admin_panel'))
    else:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, username, role FROM users"
                cursor.execute(sql)
                users = cursor.fetchall()
        finally:
            connection.close()
        return render_template('admin_panel.html', users=users)

# stud_info route for viewing/updating student records.
@app.route('/stud_info', methods=['GET','POST'])
@login_required
def stud_info():
    connection = pymysql.connect(**db_config)
    if request.method == 'POST':
        # Only admin and editor roles can update records.
        if session['user_role'] not in ['admin', 'editor']:
            flash("You are not authorized to run SQL queries.")
            return redirect(url_for('stud_info'))
        roll = request.form['roll']
        name = request.form['name']
        age = request.form['age']
        branch = request.form['branch']
        hometown = request.form['hometown']
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE stud_info SET name=%s, age=%s, branch=%s, hometown=%s WHERE roll=%s"
                cursor.execute(sql, (name, age, branch, hometown, roll))
            connection.commit()
            flash("Record updated successfully.")
        finally:
            connection.close()
        return redirect(url_for('stud_info'))
    else:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM stud_info"
                cursor.execute(sql)
                records = cursor.fetchall()
        finally:
            connection.close()
        return render_template('stud_info.html', records=records, role=session.get('user_role'))

if __name__ == '__main__':
    app.run(debug=True)
