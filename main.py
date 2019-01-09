#!/usr/bin/env python3

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os #needed to get paths of database
import sqlite3


def connect_database(path):
    try:
        connection=sqlite3.connect(path)
        cursor=connection.cursor()
        create_table(cursor)
        connection.commit()
        connection.close()
    except Exception as error:
        print(error)

def create_table(cursor):
    cursor.execute(
            '''
            CREATE TABLE Contacts(
            ID           INT   PRIMARY KEY NOT NULL,
            Name         TEXT              NOT NULL,
            Surname      TEXT              NOT NULL,
            PhoneNumber1 INT               NOT NULL,
            PhoneNumber2 INT               NOT NULL,
            PhoneNumber3 INT               NOT NULL)
            ''')

class ScreenManagement(ScreenManager):
    def __init__(self,**kwarg):
        super(ScreenManagement,self).__init__()
        self.APP_PATH=os.getcwd()
        self.DB_PATH=self.APP_PATH+'/contact_data.db'
        self.InitialWindow=InitialWindow(self)
        InitialScreen=Screen(name='Initial')
        InitialScreen.add_widget(self.InitialWindow)
        self.add_widget(InitialScreen)

class MainScreen(Screen):
    pass

class AssignScreen(Screen):
    pass


class InitialWindow(BoxLayout):
    def __init__(self,ScreenManagement,**kwargs):
        super(InitialWindow,self).__init__()
        self.ScreenManagement=ScreenManagement

    def create_database(self):
        connect_database(self.ScreenManagement.DB_PATH)

class ContactsWindow(BoxLayout):
    popup = Popup(title='About',
    content=Label(text='''
                  pyContacts
                 Version 0.25
       
   Help poor Children in Uganda!
                 www.iccf.nl'''),
    size_hint=(.8, .8))



BuildKV=Builder.load_file('pycontacts.kv')

class pyContactsApp(App):
    def build(self):
        self.title='pyContacts'
        return BuildKV

if __name__=='__main__':
    pyContactsApp().run()
