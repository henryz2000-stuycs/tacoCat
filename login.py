from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import sqlite3

#USER = 'DW'
#PASS = 'n00b'

SUCCESS = 1
BAD_PASS = -1
BAD_USER = -2

form_site = Flask(__name__)
form_site.secret_key = os.urandom(64)

try:
    execfile("db_builder.py")
except:
    pass

users = {}
user_data = c.execute("SELECT * FROM users;")

for data in user_data:
    users[data[0]] = data[1]

def authenticate(username, password):
    if username in users.keys():
        if password == users[username]:
            return SUCCESS
        else:
            return BAD_PASS
    else:
        return BAD_USER

def check_newuser(username):
    if username in users.keys():
        return BAD_USER
    return SUCCESS
    
@form_site.route('/')
def root():
    if 'user' not in session:
        return render_template('login.html', title="Login")
    else:
        return redirect( url_for('welcome') )

@form_site.route('/register')
def register():
    if 'user' not in session:
        return render_template('register.html', title="Register")
    else:
        return redirect( url_for('welcome') )

@form_site.route('/createaccount', methods=['POST'])
def create_account():
    username = request.form['user']
    password = request.form['pw']

    result = check_newuser(username)

    if result == SUCCESS:
        insert_user = "INSERT INTO users VALUES ('%s', '%s')" %(username, password)
        c.execute(insert_user)
        db.commit()
        users[username] = password
        flash(username + " registered.")
        return redirect( url_for('root') )
    elif result == BAD_USER:
        flash("Bad Username. Try another one")
        return redirect(url_for('register'))
    return redirect(url_for('root'))
    
@form_site.route('/auth', methods=['POST'])
def auth():
    username = request.form['user']
    password = request.form['pw']
    
    result = authenticate(username, password)

    if result == SUCCESS:
        session['user'] = username
        flash(session['user'] + " logged in.")
        return redirect( url_for('welcome') )
    if result == BAD_PASS:
        flash("Bad password.")
    elif result == BAD_USER:
        flash("Incorrect Username.")
    return redirect(url_for('root'))

@form_site.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect( url_for('root') )
    else:
        return render_template('welcome.html', user=session['user'], title='Welcome')

@form_site.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        flash(session['user'] + " logged out.")
        session.pop('user')
    return redirect( url_for('root') )
                               

if __name__ == '__main__':
    form_site.debug = True
    form_site.run()

db.commit()
db.close()
