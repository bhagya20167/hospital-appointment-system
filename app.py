from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'hospital_secret'  # Required for session handling

# ------------------------------------
# DATABASE SETUP
# ------------------------------------
def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            department TEXT,
            date TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ------------------------------------
# PUBLIC ROUTES
# ------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        department = request.form['department']
        date = request.form['date']
        time = request.form['time']

        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("INSERT INTO appointments (name, age, gender, department, date, time) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, age, gender, department, date, time))
        conn.commit()
        conn.close()
        return redirect('/success')
    return render_template('appointment.html')

@app.route('/success')
def success():
    return render_template('success.html')

# ------------------------------------
# ADMIN LOGIN
# ------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', error="Invalid username or password!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

# ------------------------------------
# ADMIN DASHBOARD
# ------------------------------------
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/login')

    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments")
    appointments = c.fetchall()
    conn.close()
    return render_template('admin.html', appointments=appointments)

# ------------------------------------
# DELETE FUNCTIONALITY
# ------------------------------------
@app.route('/delete/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    if not session.get('logged_in'):
        return redirect('/login')

    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ------------------------------------
# MAIN
# ------------------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)


