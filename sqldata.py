#!/usr/bin/env python3

import sqlite3

connection=sqlite3.connect('database.db')
cursor = connection.cursor()
try: cursor.execute('CREATE TABLE names (name TEXT, surname TEXT)')
except: pass
while True: 
    cursor.execute('SELECT * FROM names')
    rows = cursor.fetchall()
    for row in rows:
        print('name:'+str(row[0])+' surname: '+str(row[1]))
    print('''What would you like to do?
    
       press  1 to add
       press  2 to remove 
       
        ''')
    usrInput=input()
    if usrInput == "1":
        try:
            usrName,usrSurname=input().split(' ')
        except: pass
        cursor.execute('INSERT INTO names VALUES(?, ?)',(usrName, usrSurname))
        connection.commit()
    if usrInput == "2":
        try:
            usrREMOVE=input('who? (Enter first name)')
            cursor.execute('DELETE FROM names WHERE name LIKE "{}"'.format(usrREMOVE))
            connection.commit()
        except: print('Error')




