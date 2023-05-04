import mysql.connector

class db_operations: 
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='cpsc408!',
                                                auth_plugin='mysql_native_password',
                                                database='TaskApp')

        # create cursor object
        self.cursor = self.connection.cursor()
        print('connection made...')

    def destroy(self):
        self.connection.close()
        self.cursor.close()

    # def get_all_users(self):
    #     query = '''
    #     SELECT * 
    #     FROM users;
    #     '''
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()

    #checking if the email already exists
    def check_email(self, emailToCheck):
        query = '''
        SELECT userID
        FROM users
        WHERE email = '%s';
        ''' %emailToCheck
        try:
            #find the userID
            if self.cursor.execute(query):
                print(self.cursor.fetchone()[0])
                print("this email is already being used")
                return 1
        except:
            print("this is a unique email")
            return 0
    
    #checking if the given password matches
    def check_password(self, emailToCheck, passwordToCheck):
        query = '''
        SELECT password
        FROM users
        WHERE email = '%s';
        ''' %emailToCheck
        
        self.cursor.execute(query)
        passwordFound = self.cursor.fetchone()[0]
        if passwordToCheck == passwordFound:
            #return 1 if the passwords match
            print("the passwords match")
            return 1
        else:
            print("the passwords don't match")
            return 0
    
    #insert a new user
    def new_user(self, nameToAdd, emailToAdd, passwordToAdd):
        print("Adding new user")
        print("name:", nameToAdd, '\nemail:', emailToAdd, '\npassword:', passwordToAdd)
        query = '''
        INSERT INTO users (name, email, password)
        VALUES ('%s','%s','%s');
        ''' %(nameToAdd, emailToAdd, passwordToAdd)
        self.cursor.execute(query)
        self.connection.commit()
        print("New User added!")
        
    #get group membership given an email
    def get_groups(self, lookUpEmail):
        print("Finding groups for:", lookUpEmail)
        query = '''
        SELECT g.groupID
        FROM groupMembers g
            INNER JOIN users u
            ON g.userID = u.userID
        WHERE g.userID = (
            SELECT userID
            FROM users
            WHERE email = '%s');
        ''' %lookUpEmail
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        group_list = []
        for i in results:
            group_list.append(i[0])
        print("group list is:", group_list)
        return group_list
        
    #get all the tasks for each group user is in       
    def get_group_tasks(self, groupLookUp):
        print("getting tasks for group:", groupLookUp)
        query = '''
        SELECT t.title, t.dueDate, t.status, c.name AS category
        FROM tasks t
            INNER JOIN category c
            ON t.categoryID = c.categoryID
        WHERE groupID = '%s'
        ORDER BY t.status ASC;
        ''' %groupLookUp
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        print(results)
    
    #get the subtasks for a given task  
    def get_subtasks(self, taskID):
        print("getting subtasks for task:", taskID)
        query = '''
        SELECT title, dueDate, status
        FROM subtasks
        WHERE taskID = '%s'
        ORDER BY status ASC;
        ''' %taskID
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        print(results)
        
    
    #edit groups functionality
    #change user group or task group
    def change_group(self, email, group):
        #change user group
        print("moving user to group:", group)
        query = '''
        SELECT userID
        FROM users
        WHERE email = '%s'
        ''' %email
        self.cursor.execute(query)
        userID = self.cursor.fetchone()[0]
        query = '''
        UPDATE groupMembers
        SET groupID = '%s'
        WHERE userID = '%s';
        ''' % (group, userID)
        self.cursor.execute(query)
        self.connection.commit()
        #change task group?
        #print("moving task to group:", group)
        
    
db_ops = db_operations()
# EMAIL CHECK
emailToCheck = input("enter the email ")
# passwordToCheck = input("enter the password ")
# db_ops.check_password(emailToCheck, passwordToCheck)

# NEW USER
# name = input("enter new name: ")
# email = input("enter new email: ")
# password = input("enter new password: ")
# db_ops.new_user(name, email, password)

# group_list = db_ops.get_groups(emailToCheck)
# for i in group_list:
#     db_ops.get_group_tasks(i)
    
# db_ops.get_subtasks(1)
group = input("what group is user moving to:")
db_ops.change_group(emailToCheck, group)