from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = 'enterprise_reporting_key_2026'

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees 
                 (emp_id TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- LOGIN & SECURITY ROUTES ---

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    emp_id = request.form.get('username')
    pwd = request.form.get('password')
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO employees VALUES (?, ?)", (emp_id, pwd))
        conn.commit()
        conn.close()
        return "<h1>Success! <a href='/'>Click here to Login</a></h1>"
    except Exception as e:
        return f"<h1>Error: {e} <a href='/signup_page'>Try again</a></h1>"

@app.route('/login', methods=['POST'])
def login():
    emp_id = request.form.get('username')
    pwd = request.form.get('password')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE emp_id=? AND password=?", (emp_id, pwd))
    user = c.fetchone()
    conn.close()
    if user:
        session['user'] = emp_id
        return redirect(url_for('dashboard'))
    return "<h1>Invalid Login! <a href='/'>Try again</a></h1>"

@app.route('/logout')
def logout():
    session.pop('user', None) # Securely clears the session
    return redirect(url_for('index'))

# --- DASHBOARD & REPORTING ---

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if not file:
        return "No file uploaded!"
    
    df = pd.read_csv(file)
    
    # Automated Risk Prediction Logic
    df['Status'] = df['MonthlyCharges'].apply(lambda x: '⚠️ High Risk' if x > 80 else '✅ Stable')
    
    # Calculate Business Metrics
    high_risk_count = len(df[df['Status'] == '⚠️ High Risk'])
    low_risk_count = len(df[df['Status'] == '✅ Stable'])
    total = len(df)
    rate = round((high_risk_count / total) * 100, 1) if total > 0 else 0
    
    table_html = df.to_html(classes='table table-hover table-borderless align-middle', index=False)
    
    return render_template('report.html', 
                           tables=[table_html], 
                           high=high_risk_count, 
                           low=low_risk_count,
                           rate=rate)

if __name__ == '__main__':
    app.run(debug=True)