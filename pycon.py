#!/usr/bin/env python3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton


class TopBar(Widget):
    pass

class ReturnBar(Widget):
    pass

class ScreenManager(ScreenManager):
    pass

class MenuScreen(Screen):
    pass

class AddContactScreen(Screen):
    
    first_name_text_input=ObjectProperty()
    last_name_text_input=ObjectProperty()
    
    def add_contact(self):
        contact_name = self.first_name_text_input.text+" "+self.last_name_text_input.text
        ContactList.contact_list.data.extend([contact_name])

        ContactList.contact_list._trigger_reset_populate()

class ContactListButton(ListItemButton):
    pass

class ContactList(Widget):
    contact_list=ObjectProperty()

class SettingsScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

buildKV = Builder.load_file("my.kv")


class MyApp(App):
    def build(self):
        return buildKV 
    
if __name__=='__main__':
    pycon=MyApp()
    pycon.run()
