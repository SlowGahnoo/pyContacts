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

import sqlite3



class Bar(Widget):
    popup = Popup(title='About',
    content=Label(text=' pyContacts \nVersion 0.05'),
    size_hint=(.8, .8))
    
class MainScreen(Screen):
    pass

class AssignScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

BuildKV=Builder.load_file('pycontacts.kv')

class pyContactsApp(App):
    def build(self):
        self.title='pyContacts'
        return BuildKV

pyContactsApp().run()
