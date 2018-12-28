#!/usr/bin/env python3

import sqlite3

connection =sqlite3.connect('database.db')
cursor = connection.cursor()
try:
    cursor.execute('CREATE TABLE names (id INTEGER PRIMARY KEY, name TEXT, surname TEXT)')
except: pass
total=1
while True: 
    cursor.execute('SELECT * FROM names')
    rows = cursor.fetchall()
    for row in rows:
        total=len(rows)+1
        print('id: '+str(row[0])+'  name:'+str(row[1])+' surname: '+str(row[2]))
    print('''What would you like to do?
    
       press  1 to add
       press  2 to remove 
       
        ''')
    usr=input()
    if usr == "1":
        try:
            usr1,usr2=input().split(' ')
        except: pass
        cursor.execute('INSERT INTO names VALUES(?, ?, ?)',(total, usr1, usr2))
        connection.commit()
    if usr == "2":
        try:
            usr=input('which id?')
            cursor.execute('DELETE FROM names WHERE id LIKE "{}"'.format(usr))
            connection.commit()
        except: print('Error')




