from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Detectivemillie' 
MYSQL_DB = 'college_event_db'

# Initialize Flask-Login
app.secret_key = 'your_secret_key'  # Update this for security
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin):
    def __init__(self, reg_id, username, role):
        self.id = reg_id
        self.username = username
        self.role = role

# User loader
@login_manager.user_loader
def load_user(user_id):
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE reg_id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if user:
        return User(user['reg_id'], user['username'], user['role'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if user and check_password_hash(user['password'], password):
            login_user(User(user['reg_id'], user['username'], user['role']))
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
       
        password = request.form['password']
        role = request.form['role']

        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )

        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, password, role) VALUES (%s,%s, %s)',
                       (username, generate_password_hash(password), role))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('login'))
    
    return render_template('signup.html')


# Database connection details
MYSQL_HOST = 'localhost'
MYSQL_USER = 'your_username'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'your_database_name'


@app.route('/edashboard')
@login_required
def edashboard():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    
    cursor = connection.cursor(dictionary=True)
    if current_user.role == 'head':
        cursor.execute('SELECT * FROM events WHERE added_by = %s', (current_user.id,))
    else:
        cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('edashboard.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if current_user.role != 'eventhead':
        return 'Only event heads can add events', 403
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_venue = request.form['event_venue']

        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        
        cursor = connection.cursor()
        cursor.execute('INSERT INTO events (event_name, event_date, event_venue, added_by) VALUES (%s, %s, %s, %s)', 
                       (event_name, event_date, event_venue, current_user.id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('dashboard'))
    return render_template('add_event.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/events')
def events():
    connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
    cursor = connection.cursor()
    cursor.execute('SELECT event_name, event_date, event_time, event_venue FROM event')
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('events.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
