import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

#command = ""          #put SQL statement in this string
#c.execute(command)    #run SQL statement

create_courses = "CREATE TABLE courses (code TEXT, mark INTEGER, id INTEGER);"
create_peeps = "CREATE TABLE peeps (name TEXT, age INTEGER, id PRIMARY KEY);"

courses_csv = csv.DictReader(open("courses.csv"))
peeps_csv = csv.DictReader(open("peeps.csv"))

c.execute(create_courses)
c.execute(create_peeps)

for row in courses_csv:
    #print row
    insert_courses = "INSERT INTO courses VALUES (\"%s\", %d, %d)" % (row['code'], int(row['mark']), int(row['id']))
    #print insert_courses
    c.execute(insert_courses)

for row in peeps_csv:
    #print row
    insert_peeps = "INSERT INTO peeps VALUES (\"%s\", %d, %d)" % (row['name'], int(row['age']), int(row['id']))
    #print insert_peeps
    c.execute(insert_peeps)

    
#==========================================================

db.commit() #save changes
db.close()  #close database


