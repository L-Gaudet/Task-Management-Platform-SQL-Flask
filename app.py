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
        if db_ops.check_email(email) == 1:
            error = 'User with this email already exists.' 
            return render_template('signup.html', error=error)
        else:
            db_ops.new_user(name, email, password)
            session['currentUserID'] = db_ops.get_user_id(email)
            return redirect(url_for('dashboard'))
    else:
        # Display the login page
        return render_template('signup.html')
    
@app.route('/logout', methods=['GET'])
def logout():
    session['currentUserID'] = -1
    session['name'] = None
    session['curFocusedTaskID'] = None # ? maybe idk
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
        session['name'] = userInfo['name']
        # session['categories'] = db_ops.get_categories()

        print(userInfo)
        # Display the dashboard page
        return render_template('dashboard.html', userInfo=userInfo)


@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        dueDate = request.form['duedate']
        categoryName = request.form['category']
        groupName = request.form['group']
        userID = session['currentUserID']

        db_ops.insert_new_task(title, dueDate, categoryName, groupName, userID)
        return redirect(url_for('dashboard'))
    else:
        return render_template('create_task.html')
    

# CHANGE TO SUBTASK STUFF STIL
@app.route('/create_subtask', methods=['GET', 'POST'])
def create_subtask():
    if request.method == 'POST':
        title = request.form['title']
        dueDate = request.form['duedate']
        categoryName = request.form['category']
        groupName = request.form['group']
        userID = session['currentUserID']

        db_ops.insert_new_task(title, dueDate, categoryName, groupName, userID)
        return redirect(url_for('dashboard'))
    else:
        return render_template('create_task.html')


@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form['task_id']
    db_ops.delete_task(task_id)
    return redirect(url_for('dashboard'))
    # delete the task with the given ID from the database
    # return a response indicating success or failure

@app.route('/subtasks', methods=['GET', 'POST'])
def subtasks():
    if request.method == 'POST':
        print(request.form['task_id'])
        info = {}
        info['task_name'] = request.form['task_name']
        info['subtasks'] = db_ops.get_subtasks(request.form['task_id'])
        if len(info['subtasks']) == 0:
            info['empty'] = 1
        else:
            info['empty'] = 0
        print(info['subtasks'])
        return render_template('subtasks.html', info=info)
    else:
        print(request.form['task_id'])
        # taskInfo = {}



        return render_template('subtasks.html')

@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    task_id = request.form.get('taskId')
    newStatus = 1 if request.form.get('completed')=='true' else 0
    
    print(task_id, newStatus)
    
    db_ops.set_task_status(taskID=task_id, newStatus=newStatus)

    return "updated status"

@app.route('/update_subtask_status', methods=['POST'])
def update_subtask_status():
    task_id = request.form.get('taskId')
    newStatus = 1 if request.form.get('completed')=='true' else 0
    
    print(task_id, newStatus)
    
    db_ops.set_subtask_status(taskID=task_id, newStatus=newStatus)

    return "updated status"
