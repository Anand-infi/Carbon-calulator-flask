# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from your_db_module import authenticate_user # Placeholder for your DB check

app = Flask(__name__)
app.secret_key = 'your_super_secret_key' # Needed for session management

# --- Temporary/Mock User Database (In reality, this is Firebase/Postgres) ---
# 1 = Admin, 2 = Client
MOCK_USERS = {
    'adminuser': {'password': 'adminpassword', 'role': 1},
    'clientcompanyA': {'password': 'clientpassword', 'role': 2},
}
# --------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # **STEP 1: Authenticate and get role (Connect to Firebase Auth here!)**
        # In a real app: You would check credentials against Firebase Authentication
        
        # --- Mock Authentication ---
        if username in MOCK_USERS and MOCK_USERS[username]['password'] == password:
            user_role = MOCK_USERS[username]['role']
            session['logged_in'] = True
            session['username'] = username
            session['user_role'] = user_role
            
            # **STEP 2: Role-Based Redirection**
            if user_role == 1:
                return redirect(url_for('admin_dashboard'))
            elif user_role == 2:
                return redirect(url_for('client_dashboard'))
        else:
            # Failed login (You would use a flash message here)
            return render_template('login.html', error='Invalid credentials.')
            
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # **STEP 3: Check Role for Access Control**
    if session.get('logged_in') and session.get('user_role') == 1:
        return render_template('admin_dashboard.html')
    return redirect(url_for('login_route'))

@app.route('/client/dashboard')
def client_dashboard():
    if session.get('logged_in') and session.get('user_role') == 2:
        return render_template('client_dashboard.html')
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(debug=True) # Runs the app locally