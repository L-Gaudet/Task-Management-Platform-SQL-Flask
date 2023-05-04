# from flask import Flask
# from flask import Flask, request, render_template, 
from flask import Flask, request, render_template, redirect, url_for, flash

from db_api import db_operations


app = Flask(__name__)

db_ops = db_operations()
# print(db_ops.get_all_users())

# Define a route for the root URL
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        email = request.form['email']
        password = request.form['password']
        # Check if the email and password are correct (you would need to implement this logic yourself)
        if email == 'myemail' and password == 'mypassword':
            # Redirect to the dashboard page
            return redirect(url_for('dashboard'))
        else:
            # Show an error message
            error = 'Invalid credentials. Please try again.'
            flash('Invalid credentials. Please try again.')
            return render_template('login.html', error=error)
    else:
        # Display the login page
        return render_template('picoLogin.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        print(first_name, last_name, email, password)

        # check if email exists already
        
        # add to database

        if email == 'myemail' and password == 'mypassword':
            # Redirect to the dashboard page
            return redirect(url_for('dashboard'))
        else:
            # Show an error message
            error = 'Invalid credentials. Please try again.'
            flash('User with this email already exists.')
            return render_template('signup.html', error=error)
    else:
        # Display the login page
        return render_template('signup.html')

# Define a route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Display the dashboard page
    return render_template('dashboard.html')