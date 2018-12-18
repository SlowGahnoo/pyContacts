#!/usr/bin/env python3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

class TopBar(Widget):
    pass

class BottomBar(Widget):
    pass

class ReturnBar(Widget):
    pass

class ScreenManager(ScreenManager):
    pass

class MenuScreen(Screen):
    pass

class AddContactScreen(Screen):
    pass

class ContactList(Widget):
    pass

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
