#A Simple timekeeping app. Helps to keep track of time spent on tasks
from kivy.app import App
from kivy.lang import builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.clock import Clock

import time as t
from datetime import timedelta


class ScrollOutput(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_y = True
        self.do_scroll_x = False
        
        self.layout = GridLayout(size_hint_y = None)
        self.layout.spacing = 5
        self.layout.padding = 20
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.layout.cols = 1
        self.layout.width = 300

        self.add_widget(self.layout)

    def add_entry(self, time):
        time = time
        

        button = Button(text=str(time), size_hint_y=None, height=40)
        self.layout.add_widget(button)

class TaskSelector(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task = ""
        self.dropdown = DropDown()
        self.cols = 1
        for i in range(10):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.mainbtn = Button(text="Select", size_hint=(None, None))
        self.mainbtn.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbtn, 'text', x))

        self.add_widget(self.mainbtn)

class CountDown(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        self.timer = 0
        self.open = "0"

        self.counter = Label(text=self.open)

        self.button = Button(text="Add")
        self.button.bind(on_press=self.addEntry)

        self.add_widget(self.counter)
        self.add_widget(self.button)
        Clock.schedule_interval(self.incrementTimer, 1)


    def addEntry(self, instance):
        myApp.main_screen.entries.add_entry(str(timedelta(seconds=self.timer)))
        self.timer = 0
    def incrementTimer(self, instance):
        time = self.timer
        time += 1
        self.timer = time
        self.counter.text = str(timedelta(seconds=self.timer))


class BaseWindow(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        self.selector = TaskSelector(size_hint_y=0.1)
        
        self.entries = ScrollOutput(size_hint_y=0.7)

        self.timer = CountDown(size_hint_y=0.1)

    
      
        self.add_widget(self.selector)
        self.add_widget(self.timer)
        self.add_widget(self.entries)

class TimeApp(App):
    def build(self):
       self.screen_manager = ScreenManager()

       self.main_screen = BaseWindow()
       screen = Screen(name="Main")
       screen.add_widget(self.main_screen)
       self.screen_manager.add_widget(screen)

       return self.screen_manager


if __name__ == "__main__":
    myApp = TimeApp()
    myApp.run()