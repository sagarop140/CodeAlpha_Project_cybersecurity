from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Vulnerable SQL query
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()
        
        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    
    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome {session['user']}"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
