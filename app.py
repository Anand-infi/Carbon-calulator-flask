# app.py (Updated)
from flask import Flask, render_template, request, redirect, url_for, session, abort

# --- Setup and Secret Key ---
app = Flask(__name__)
app.secret_key = 'your_super_secret_key' 

# --- Mock Data (Temporary Database Stand-in) ---
# 1 = Admin, 2 = Client
MOCK_USERS = {
    'adminuser': {'password': 'adminpassword', 'role': 1},
    'clientcompanyA': {'password': 'clientpassword', 'role': 2},
}

# This list holds the categories added by the admin.
# In a real app, this would be a database connection (Firebase/PostgreSQL).
emission_categories = [
    {'id': 1, 'name': 'Purchased Electricity', 'unit': 'kWh', 'factor': 0.45},
    {'id': 2, 'name': 'Company Fleet Diesel', 'unit': 'Liters (L)', 'factor': 2.68},
    # The IDs will auto-increment from 3 for new additions
]
# ---------------------------------------------------


# --- Authentication and Utility Functions ---

def is_admin():
    """Checks if the currently logged-in user is an Admin."""
    return session.get('logged_in') and session.get('user_role') == 1

def requires_admin_login(f):
    """Decorator to protect admin routes."""
    def decorated_function(*args, **kwargs):
        if not is_admin():
            # If not admin, redirect to login page
            return redirect(url_for('login_route')) 
        return f(*args, **kwargs)
    return decorated_function

# --- Login Route (as before) ---
@app.route('/login', methods=['GET', 'POST'])
def login_route():
    # ... (Login logic remains the same as provided previously)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in MOCK_USERS and MOCK_USERS[username]['password'] == password:
            user_role = MOCK_USERS[username]['role']
            session['logged_in'] = True
            session['username'] = username
            session['user_role'] = user_role
            
            if user_role == 1:
                return redirect(url_for('admin_dashboard'))
            elif user_role == 2:
                return redirect(url_for('client_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials.')
            
    return render_template('login.html')

@app.route('/admin/dashboard')
@requires_admin_login
def admin_dashboard():
    return render_template('admin_dashboard.html') # Need to create this file later

@app.route('/client/dashboard')
def client_dashboard():
    if session.get('logged_in') and session.get('user_role') == 2:
        return render_template('client_dashboard.html') # Need to create this file later
    return redirect(url_for('login_route'))

# ---------------------------------------------------
# --- 1. ADMIN CATEGORY MANAGEMENT (GET: Display Page) ---
# ---------------------------------------------------

@app.route('/admin/categories', methods=['GET'])
@requires_admin_login
def manage_categories():
    """Renders the Category Management page with current data."""
    # Pass the mock data to the HTML template for display in the table
    return render_template(
        'admin_categories.html', 
        categories=emission_categories
    )

# ---------------------------------------------------
# --- 2. ADMIN CATEGORY MANAGEMENT (POST: Handle Form) ---
# ---------------------------------------------------

@app.route('/admin/add-category', methods=['POST'])
@requires_admin_login
def add_category():
    """Handles the form submission for adding a new category."""
    try:
        # 1. Get data from the submitted form
        name = request.form['name']
        unit = request.form['unit']
        # Convert factor to a float for calculation purposes
        factor = float(request.form['factor'])
        
        # 2. Generate a new ID (simulating database primary key)
        if emission_categories:
            new_id = max(c['id'] for c in emission_categories) + 1
        else:
            new_id = 1
            
        # 3. Create the new category dictionary
        new_category = {
            'id': new_id,
            'name': name,
            'unit': unit,
            'factor': factor
        }
        
        # 4. Save to the mock database (list)
        emission_categories.append(new_category)
        
        # 5. Redirect back to the categories page to see the new addition
        # In a real app, you'd add a success message here.
        return redirect(url_for('manage_categories'))

    except ValueError:
        # Handle cases where the factor input is not a valid number
        # In a real app, you'd show a user-friendly error message on the page.
        print("Error: Emission factor must be a valid number.")
        return redirect(url_for('manage_categories'))
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Use HTTP 500 for server errors
        abort(500) 


if __name__ == '__main__':
    # Running in debug=True means the server automatically restarts when you save app.py
    app.run(debug=True)
