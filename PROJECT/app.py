from flask import Flask, render_template, request, redirect, url_for, session 

from flask_mysqldb import MySQL 

import MySQLdb.cursors 

import re 

  

  

app = Flask(__name__) 

  

  

app.secret_key = 'your secret key'

  

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'root'

app.config['MYSQL_DB'] = 'school'

  

mysql = MySQL(app) 

  

@app.route('/') 
def home():
    return render_template('home.html')

@app.route('/login', methods =['GET', 'POST'])
def login(): 

    msg = '' 

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 

        username = request.form['username'] 

        password = request.form['password'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 

        cursor.execute('SELECT * FROM teacher WHERE username = % s AND password = % s', (username, password, )) 

        account = cursor.fetchone() 

        if account: 

            session['loggedin'] = True

            session['id'] = account['id'] 

            session['username'] = account['username'] 

            msg="user logged in"
            return render_template('index.html', msg = msg) 
            

        else: 

            msg = 'Incorrect username / password !'

    return render_template('login.html', msg = msg) 

  
@app.route('/index',methods =['GET', 'POST'])
def index():
    msg = '' 

    if request.method == 'POST' and 'subject' in request.form and 'mark' in request.form and 'attendence' in request.form : 

        subject = request.form['subject'] 

        mark = request.form['mark'] 

        attendence = request.form['attendence'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('INSERT INTO data VALUES (NULL, % s, % s, % s)', (subject, mark, attendence, )) 

        mysql.connection.commit() 

        msg = 'You have entered data successfully !'
        return subject,mark,attendence
        
       
    return render_template('index.html',msg=msg)

@app.route('/logout') 

def logout(): 

    session.pop('loggedin', None) 

    session.pop('id', None) 

    session.pop('username', None) 

    return redirect(url_for('home')) 

  

@app.route('/register', methods =['GET', 'POST']) 

def register(): 

    msg = '' 

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : 

        username = request.form['username'] 

        password = request.form['password'] 

        email = request.form['email'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 

        cursor.execute('SELECT * FROM teacher WHERE username = % s', (username, )) 

        account = cursor.fetchone() 

        if account: 

            msg = 'Account already exists !'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 

            msg = 'Invalid email address !'

        elif not re.match(r'[A-Za-z0-9]+', username): 

            msg = 'Username must contain only characters and numbers !'

        elif not username or not password or not email: 

            msg = 'Please fill out the form !'

        else: 

            cursor.execute('INSERT INTO teacher VALUES (NULL, % s, % s, % s)', (username, password, email, )) 

            mysql.connection.commit() 

            msg = 'You have successfully registered !'

    elif request.method == 'POST': 

        msg = 'Please fill out the form !'

    return render_template('register.html', msg = msg) 
@app.route('/student', methods =['GET', 'POST'])
def student(): 

    msg = '' 

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 

        username = request.form['username'] 

        password = request.form['password'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 

        cursor.execute('SELECT * FROM student WHERE username = % s  AND password = % s', (username, password, )) 

        account = cursor.fetchone() 

        if account: 

            session['loggedin'] = True

            session['id'] = account['id'] 

            session['username'] = account['username'] 
            

            msg="user logged in"
            return render_template('studentdata.html', msg = msg) 
            

        else: 

            msg = 'Incorrect username / password !'

    return render_template('student.html', msg = msg) 
@app.route('/studentdata') 
def studentdata():

     return render_template('studentdata.html')

  

if __name__ == "__main__":
    app.run()
