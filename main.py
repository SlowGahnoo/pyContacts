#!/usr/bin/env python3

import kivy
import os
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button

def connect_database(path):
    try:
        connection=sqlite3.connect(path)
        cursor=connection.cursor()
        create_data_table(cursor)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)

def create_data_table(cursor):
    cursor.execute('''

    CREATE TABLE Contacts(
    Name           TEXT NOT NULL,
    Surname        TEXT NOT NULL,
    PhoneNumber1   INT NOT NULL,
    PhoneNumber2   INT NOT NULL,
    PhoneNumber3   INT NOT NULL

    
    
    
    
    
    )   '''     
               )

class MainScreen(ScreenManager):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__()
        self.APP_PATH=os.getcwd()
        self.DB_PATH=self.APP_PATH+'/data.db'
        self.InitialScreen=InitialScreen(self)
        self.ContactScreen=ContactScreen(self)
        self.AssignContactScreen=BoxLayout()
        
        screen=Screen(name='init')
        screen.add_widget(self.InitialScreen)
        self.add_widget(screen)
        
        screen=Screen(name='menu')
        screen.add_widget(self.ContactScreen)
        self.add_widget(screen)

        screen=Screen(name='assign_contact')
        screen.add_widget(self.AssignContactScreen)
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

    def check_memory(self):
        self.ids.container.clear_widgets()  # refreshes container by refering it from kv file
        self.ids.button_bar.clear_widgets() # and prevents duplicates from spawining 
        connection=sqlite3.connect(self.mainscreen.DB_PATH)
        cursor=connection.cursor()
        cursor.execute('SELECT Name, Surname, PhoneNumber1, PhoneNumber2, PhoneNumber3 from Contacts ')
        for i in cursor:
            widget=DataWidget(self.mainscreen)
            r1= 'Name: '+i[0]+'\n'
            r2='Surname: '+i[1]+'\n'
            r3='Phone Number 1: '+str(i[2])+'\n'
            r4='Phone Number 2: '+str(i[3])+'\n'
            r5='Phone Number 3: '+str(i[4])+'\n'
            widget.data= r1+r2+r3+r4+r5
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
        insertion='INSERT INTO Contacts(Name,Surname,PhoneNumber1,PhoneNumber2,PhoneNumber3)'
        values='VALUES("%s","%s",%s,%s,%s)'%(usrName,usrSurname,usrPhone1,usrPhone2,usrPhone3)
        try:
            cursor.execute(insertion+' '+values)
            connection.commit()
            connection.close()
            self.mainscreen.return_to_menu()
        except Exception as error:
            print(error)



    def return_back(self):
        self.mainscreen.return_to_menu()

class DataWidget(BoxLayout):
    def __init__(self,mainscreen,**kwargs):
        super(DataWidget,self).__init__()
        self.mainscreen=mainscreen

    def update_data(self,data_id):
        pass


class pyContactsApp(App):
    Builder.load_file('GUI.kv')
    def build(self):
        self.title='pyContacts'
        return MainScreen()

if __name__=='__main__':
    pyContactsApp().run()
