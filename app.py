# from flask import Flask
# from flask import Flask, request, render_template, 
from flask import Flask, request, render_template, redirect, url_for, session

from db_api import db_operations


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Qfdz\n\xec]/'

db_ops = db_operations()
# print(db_ops.get_all_users())

# Define a route for the root URL
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        # Check if the email and password are correct (you would need to implement this logic yourself)
        if db_ops.check_email(email) == 1:
            if db_ops.check_password(email, password) == 1:
                session['currentUserID'] = db_ops.get_user_id(email)
                return redirect(url_for('dashboard'))
            else:
                # Show an error message
                error = 'Invalid email or password. Please try again.'
                return render_template('picoLogin.html', error=error)
        else:
            # Show an error message
            error = 'Invalid email or password. Please try again.'
            return render_template('picoLogin.html', error=error)
    else:
        # Display the login page
        return render_template('picoLogin.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        print(name, email, password)

        # check if email exists already
        
        # add to database

        if email == 'email@email.com' and password == 'password123':
            # Redirect to the dashboard page
            return redirect(url_for('dashboard'))
        else:
            # Show an error message
            error = 'User with this email already exists.'
            return render_template('signup.html', error=error)
    else:
        # Display the login page
        return render_template('signup.html')
    
@app.route('/logout', methods=['GET'])
def logout():
    session['currentUserID'] = -1
    return redirect(url_for('login'))

# Define a route for the dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        pass
    else:
        # get username and groups and tasks
        userInfo = {}
        userGroupIDs = db_ops.get_groups(session['currentUserID'])
        print(userGroupIDs)
        groupTasks = {}

        # get names of each group
        groupNames = [db_ops.get_group_names(id) for id in userGroupIDs ] 

        # get tasks for each group
        for i in range(len(groupNames)):
            groupTasks[groupNames[i]] = db_ops.get_group_tasks(userGroupIDs[i])

        # dictionary with keys as group names, tasks and values
        userInfo['groups'] = groupTasks

        userInfo['id'] = session['currentUserID']
        userInfo['name'] = db_ops.get_user_name(session['currentUserID'])

        print(userInfo)
        # Display the dashboard page
        return render_template('dashboard.html', userInfo=userInfo)
    

# @app.route('/add_task')
# def add_task():
#     group_id = request.args.get('group_id')
#     # render the add_task.html template with the group_id passed as a parameter
#     return render_template('add_task.html', group_id=group_id)
