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

execfile("db_builder.py")

users = {} #{username: password}
user_data = c.execute("SELECT * FROM users;")

for data in user_data:
    users[data[0]] = data[1]

#print users

history = {} #{id: {username: contribution}}
history_data = c.execute("SELECT * FROM history;")

for data in history_data:
    try:
        history[data[1]][data[0]] = data[2]
    except:
        history[data[1]] = {data[0]: data[2]}

#print history


stories = {} #{id: {title: title, fullstory: fullstory, previousupdate: previousupdate}}
stories_data = c.execute("SELECT * FROM stories;")

for data in stories_data:
    try:
        stories[data[0]]["title"] = data[1]
        stories[data[0]]["fullstory"] = data[2]
        stories[data[0]]["previousupdate"] = data[3]
    except:
        stories[data[0]] = {"title": data[1], "fullstory": data[2], "previousupdate": data[3]}

#print stories

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

@form_site.route('/editstory', methods=['POST'])
def edit_story():
    #print request.form
    #print "TTTTTTTTT"
    #print request.form['id']
    #c.execute("DELETE FROM history WHERE contribution='hello';")
    c.execute("INSERT INTO history VALUES ('%s', %s, '%s');" %(session['user'], request.form['id'], request.form['contribution']))
    #c.execute("DELETE FROM
    print "##########################################################"
    print stories[int(request.form['id'])]["fullstory"]
    print request.form['contribution']
    print stories[int(request.form['id'])]["fullstory"] + request.form['contribution']
    print "##########################################################"
    c.execute("UPDATE stories SET fullstory='%s' WHERE id=%s;" %(stories[int(request.form['id'])]["fullstory"] + request.form['contribution'], request.form['id']))
    c.execute("UPDATE stories SET previousupdate='%s' WHERE id=%s;" %(request.form['contribution'], request.form['id']))
    db.commit()
    flash("Story edited.")
    #INSERT FLASH HERE***************************************
    return redirect( url_for('welcome') )

@form_site.route('/choseneditstory', methods=['POST'])
def chosen_edit_story():
    '''
    print request.form.keys()
    print request.form.values()
    print request.form.keys()[0]
    print request.form.values()[0]
    print stories
    print stories[request.form.keys()[0]]
    '''
    previous = stories[int(request.form.values()[0])]["previousupdate"]
    print previous
    id = int(request.form.values()[0])
    print "----------"
    print id
    print "----------"
    return render_template("edit_story.html", id=id, title="Edit %s" %stories[int(request.form.values()[0])]["title"], previous=previous)

@form_site.route('/chooseeditstory', methods=['POST'])
def choose_edit_story():
    new = {}
    #print history
    for story in stories.keys():
        '''
        print "===================="
        print story
        print session['user']
        print history[story].keys()
        print "===================="
        '''
        if session['user'] not in history[story].keys():
            #new[story] = stories[story]["title"].replace(" ", "_")
            new[story] = stories[story]["title"]
    print new
    return render_template('list.html', title="Edit Stories!", new=new)

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

@form_site.route('/createstoryhome', methods=['POST', 'GET'])
def newstory():
    return render_template('create_story.html')

@form_site.route('/createstory', methods=['POST', 'GET'])
def create():
    if 'user' not in session:
        flash("You must log in to create a story")
    else:
        title = request.form["title"]
        line = request.form["firstline"]
        last_entry = c.execute("SELECT * FROM stories WHERE ID = (SELECT MAX(ID) FROM stories);")
        for value in last_entry:
            id = value[0] + 1;
            #print id
            #successfully updates stories database
        with db:
            new_entry = c.execute("INSERT into stories VALUES ('%s','%s', '%s', '%s');" %(id, title, line, line))
            update_history = c.execute("INSERT into history VALUES ('%s', '%s', '%s');" %(session['user'], id, line))
            flash("Your story was succesfully created!")
    return redirect(url_for('welcome'))


@form_site.route('/viewstories', methods = ['POST', 'GET'])
def viewstory():
    story_dict = {}
    all_stories = c.execute("SELECT * FROM stories;")
    for story in all_stories:
        story_dict[story[0]] = story[1]
    #print story_dict
    return render_template("view_stories.html", new = story_dict)

@form_site.route('/display', methods = ['POST', 'GET'])
def displaypage():
    idnum = request.form.get('storyid')
    storyinfo = c.execute("SELECT * FROM stories where ID = %s;" %(idnum)).fetchall()
    title = storyinfo[0][1]
    fullstory = storyinfo[0][2]
    return render_template("display.html", title = title, story = fullstory) 
    #return render_template("display.html", story = fullstory)

if __name__ == '__main__':
    form_site.debug = True
    form_site.run()

db.commit()
db.close()
