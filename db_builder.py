import sqlite3   #enable control of an sqlite database

f="story.db"

db = sqlite3.connect(f, check_same_thread=False) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

create_users = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);"
create_history = "CREATE TABLE history (username TEXT NOT NULL, id INTEGER NOT NULL, contribution TEXT);"
create_stories = "CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT, fullstory TEXT NOT NULL, previousupdate TEXT NOT NULL);"

insert_admin = "INSERT INTO users VALUES ('test', 'test');"
insert_admin0 = "INSERT INTO users VALUES ('test0', 'test0');"
insert_history = "INSERT INTO history VALUES ('test', 0, 'hi');"
insert_history0 = "INSERT INTO history VALUES ('test0', 0, 'hi0');"
insert_stories = "INSERT INTO stories VALUES (0, 'blah', 'hi\nhi0', 'hi0');"

insert_newstory = "INSERT INTO stories VALUES (1, 'new title', 'new', '')"

try:
    c.execute(create_users)
    c.execute(create_history)
    c.execute(create_stories)
    c.execute(insert_admin)
    c.execute(insert_history)
    c.execute(insert_stories)

    c.execute(insert_admin0)
    c.execute(insert_history0)

    c.execute(insert_newstory)
except:
    pass

#==========================================================

db.commit() #save changes
#db.close()  #close database


