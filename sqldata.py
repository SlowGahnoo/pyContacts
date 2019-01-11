#!/usr/bin/env python3
import Epafes_importable as Ep
import sqlite3

connection=sqlite3.connect('Contacts.db')
cursor = connection.cursor()
try: cursor.execute('CREATE TABLE IF NOT EXISTS Contacts (name TEXT, surname TEXT, Mobile INTEGER, Home INTEGER, Office INTEGER)')
except: pass
while True: 
    cursor.execute('SELECT * FROM Contacts')
    rows = cursor.fetchall()
    for row in rows:
        print('name:'+str(row[0])+' surname: '+str(row[1]))
    print('What would you like to do?\n\n1->Add a contact\n2->Remove a contact\n3->Add or change something to a contact\n4->exit')
    usrInput=input()
    
    if usrInput == "1":
        try:
            
            usrName=input('Name:')
            usrSurname=input('Surname:')
            usrMobile=input('Mobile:')
            usrHome=input('Home:')
            usrOffice=input('Office:')
                
            if usrName=='':
                print('Your contact has to have a Name')
            else:
                cursor.execute('SELECT * FROM Contacts WHERE name="{}" AND surname="{}"'.format(usrName,usrSurname))
                matrix=cursor.fetchall()
                
                if matrix!=[]:
                    print('There is already a contact with this name')
                
                else:
                    cursor.execute('INSERT INTO Contacts VALUES(?,?,?,?,?)',(usrName, usrSurname,usrMobile,usrHome,usrOffice))
                    connection.commit()
                    
        except: pass
        
    if usrInput == "2":
        try:
            usrName=input('Type the fist name of the contact you want to delete\n')
            usrSurname=input('Type the surname of the contact you want to delete\n')
            cursor.execute('DELETE FROM Contacts WHERE name LIKE "{}" AND surname LIKE "{}"'.format(usrName,usrSurname))
            connection.commit()
        except: print('Error')
        
    if usrInput == "3":
        usrName=input('What is the name of the contact?\n')
        usrSurname=input('What is the surname of the contact?\n')
        cursor.execute('SELECT * FROM Contacts WHERE name="{}" AND surname="{}"'.format(usrName,usrSurname))
        matrix=cursor.fetchall()
        if matrix == []:
            print('This contact does not exist')
            
        else:
            usrKind=input('What do you want to add or change?(Mobile,Home,Office)\n')
            if not (usrKind=='Mobile' or usrKind=='Home' or usrKind=='Office'):
                print('This is not a valid kind of number\n')
            else:
                usrNumber=input('Type the number you want to add\n')
                
                if usrKind=='Home':
                    cursor.execute('UPDATE Contacts SET Home=? WHERE name=? AND surname=?',(usrNumber,usrName,usrSurname))
                elif usrKind=='Mobile':
                    cursor.execute('UPDATE Contacts SET Mobile=? WHERE name=? AND surname=?',(usrNumber,usrName,usrSurname))
                elif usrKind=='Office':
                    cursor.execute('UPDATE Contacts SET Office=? WHERE name=? AND surname=?',(usrNumber,usrName,usrSurname))
                connection.commit()
        
    if usrInput=="4":
        break

