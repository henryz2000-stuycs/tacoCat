import sqlite3   #enable control of an sqlite database

f="story.db"

db = sqlite3.connect(f, check_same_thread=False) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

create_users = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);"
create_stories = "CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT)"
insert_admin = "INSERT INTO users VALUES ('test', 'test')"

c.execute(create_users)
c.execute(create_stories)
c.execute(insert_admin)

#==========================================================

db.commit() #save changes
db.close()  #close database


