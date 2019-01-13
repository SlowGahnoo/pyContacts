#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import kivy
import os
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.config import Config
Config.set('kivy','window_icon','icon.png')



def connect_database(path):
    try:
        connection=sqlite3.connect(path)
        cursor=connection.cursor()
        create_data_table(cursor)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
#change names
def create_data_table(cursor):
    cursor.execute('''
    CREATE TABLE Contacts(
    Name           TEXT NOT NULL,
    Surname        TEXT NOT NULL,
    Mobile         INT NOT NULL,
    Home           INT NOT NULL,
    Office         INT NOT NULL
    )   '''     
               )

class Message(Popup):
    pass 

class MainScreen(ScreenManager):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__()
        self.APP_PATH=os.getcwd()
        self.DB_PATH=self.APP_PATH+'/Contacts.db'
        self.InitialScreen=InitialScreen(self)
        self.ContactScreen=ContactScreen(self)
        self.AssignContactScreen=BoxLayout()
        self.EditContactScreen=BoxLayout()
        self.Popup=Message()
        
        screen=Screen(name='init')
        screen.add_widget(self.InitialScreen)
        self.add_widget(screen)
        
        screen=Screen(name='menu')
        screen.add_widget(self.ContactScreen)
        self.add_widget(screen)

        screen=Screen(name='assign_contact')
        screen.add_widget(self.AssignContactScreen)
        self.add_widget(screen)

        screen=Screen(name='edit_contact')
        screen.add_widget(self.EditContactScreen)
        self.add_widget(screen)
        
        self.initialize()

    def initialize(self):
        self.current='init'
    
    def return_to_menu(self):
        self.ContactScreen.check_memory()
        self.current='menu'

    def goto_assign_contact(self):
        self.AssignContactScreen.clear_widgets()
        widget=AssignContactScreen(self)
        self.AssignContactScreen.add_widget(widget)
        self.current='assign_contact'
    
    def goto_edit_contact(self,data_id1,data_id2):
        self.EditContactScreen.clear_widgets()
        widget=EditContactScreen(self,data_id1,data_id2)
        self.EditContactScreen.add_widget(widget)
        self.current='edit_contact'

class InitialScreen(BoxLayout):
    def __init__(self,mainscreen,**kwargs):
        super(InitialScreen,self).__init__()
        self.mainscreen=mainscreen

    def create_database(self):
        connect_database(self.mainscreen.DB_PATH)
        self.mainscreen.return_to_menu()

class ContactScreen(BoxLayout):
    def __init__(self,mainscreen,**kwargs):
        super(ContactScreen,self).__init__()
        self.mainscreen=mainscreen

    def AboutPopup(self):
        message=self.mainscreen.Popup.ids.message
        self.mainscreen.Popup.open()
        self.mainscreen.Popup.title='About'
        message.text=''' 
        
        
                     
                     
                     
                pyContacts
               version 0.95
        
       
       
       
       

        
        '''
#delete this
#change names
    def check_memory(self):
        self.ids.container.clear_widgets()  # refreshes container and
        self.ids.button_bar.clear_widgets() # prevents duplicates from spawining 
        connection=sqlite3.connect(self.mainscreen.DB_PATH)
        cursor=connection.cursor()
        cursor.execute('SELECT Name, Surname, Mobile, Home, Office from Contacts ')
        for i in cursor:
            widget=DataWidget(self.mainscreen)
            row1='Name: '+i[0]+'\n'
            row2='Surname: '+i[1]+'\n'
            row3='Mobile: '+str(i[2])+'\n'
            row4='Home: '+str(i[3])+'\n'
            row5='Office: '+str(i[4])+'\n'
            widget.data= row1+row2+row3+row4+row5
            widget.data_id1=i[0]
            widget.data_id2=i[1]
            self.ids.container.add_widget(widget)
        widget=AssignContactButton(self.mainscreen)
        self.ids.button_bar.add_widget(widget)
        connection.close()

class AssignContactButton(Button):
    def __init__(self,mainscreen,**kwargs):
        super(AssignContactButton,self).__init__()
        self.mainscreen=mainscreen

    def create_new_contact(self):
        self.mainscreen.goto_assign_contact()

class AssignContactScreen(BoxLayout):
    def __init__(self,mainscreen,**kwargs):
        super(AssignContactScreen,self).__init__()
        self.mainscreen=mainscreen

    def insert_data(self):
        connection=sqlite3.connect(self.mainscreen.DB_PATH)
        cursor=connection.cursor()
        usrName=self.ids.name_input.text
        usrSurname=self.ids.surname_input.text
        usrPhone1=self.ids.num1_input.text
        usrPhone2=self.ids.num2_input.text
        usrPhone3=self.ids.num3_input.text
        usrInput=(usrName,usrSurname,usrPhone1,usrPhone2,usrPhone3)
        insertion='INSERT INTO Contacts(Name,Surname,Mobile,Home,Office)'
        values="""VALUES('{}',"{}","{}","{}","{}")""".format(usrName,usrSurname,usrPhone1,usrPhone2,usrPhone3)
        try:
            cursor.execute('SELECT * FROM Contacts WHERE Name="{}" AND Surname="{}"'.format(usrName,usrSurname))
            matrix=cursor.fetchall()
            if matrix!=[]:
                message=self.mainscreen.Popup.ids.message
                self.mainscreen.Popup.open()
                self.mainscreen.Popup.title='Database error'
                message.text='Contact already exists'
            else:
                cursor.execute(insertion+' '+values)
                connection.commit()
                connection.close()
                self.mainscreen.return_to_menu()
        except Exception as error:
            print(error)
            message=self.mainscreen.Popup.ids.message
            self.mainscreen.Popup.open()
            self.mainscreen.Popup.title='Data base error'
            message.text=str(error)



    def return_back(self):
        self.mainscreen.return_to_menu()

class EditContactScreen(BoxLayout):
    def __init__(self,mainscreen,data_id1,data_id2,**kwargs):
        super(EditContactScreen,self).__init__()
        self.mainscreen=mainscreen
        self.data_id1=data_id1
        self.data_id2=data_id2
        self.check_memory()

    def check_memory(self):
        connection=sqlite3.connect(self.mainscreen.DB_PATH)
        cursor=connection.cursor()
        selection="""SELECT Mobile,Home,Office from Contacts WHERE Name='{}' AND Surname="{}" """.format(self.data_id1,self.data_id2)
        cursor.execute(selection)
        for i in cursor:
            self.ids.num1_input.text=str(i[0])
            self.ids.num2_input.text=str(i[1])
            self.ids.num3_input.text=str(i[2])
        connection.close()

    def update_data(self):
        connection=sqlite3.connect(self.mainscreen.DB_PATH)
        cursor=connection.cursor()
        usrName=self.data_id1
        usrSurname=self.data_id2
        usrPhone1=self.ids.num1_input.text
        usrPhone2=self.ids.num2_input.text
        usrPhone3=self.ids.num3_input.text
        usrInput=(usrName,usrSurname,usrPhone1,usrPhone2,usrPhone3)
        query1='UPDATE Contacts SET'
        query2="""Mobile="{}", Home="{}", Office="{}" """.format(usrPhone1,usrPhone2,usrPhone3)
        query3="""WHERE Name='{}' AND Surname="{}" """.format(usrName,usrSurname)
        try:
            cursor.execute(query1+' '+query2+' '+query3)
            connection.commit()
            connection.close()
            self.mainscreen.return_to_menu()
        except Exception as error:
            print(error)
            message=self.mainscreen.Popup.ids.message
            self.mainscreen.Popup.open()
            self.mainscreen.Popup.title='Data base error'
            message.text=str(error)

    def delete_data(self):
        connection=sqlite3.connect(self.mainscreen.DB_PATH)
        cursor=connection.cursor()
        query1="""DELETE from Contacts where Name='{}' AND Surname="{}" """.format(self.data_id1,self.data_id2)
        cursor.execute(query1)
        connection.commit()
        connection.close()
        self.return_back()



    def return_back(self):
        self.mainscreen.return_to_menu()


class DataWidget(BoxLayout):
    def __init__(self,mainscreen,**kwargs):
        super(DataWidget,self).__init__()
        self.mainscreen=mainscreen

    def edit_data(self,data_id1,data_id2):
        self.mainscreen.goto_edit_contact(data_id1,data_id2)

class pyContactsApp(App):
    Builder.load_file('GUI.kv')
    def build(self):
        self.title='pyContacts'
        return MainScreen()

if __name__=='__main__':
    pyContactsApp().run()
