#A Simple timekeeping app. Helps to keep track of time spent on tasks
from kivy.app import App
from kivy.clock import Clock

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput



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
        self.tasks = []
        with open("tasks.txt", "r") as t:
            raw_tasks = t.readlines()
            for task in raw_tasks:
                self.tasks.append(task.strip())

        self.mainbtn = Button(text="Task", size_hint_y=None, height=60)
        self.mainbtn.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbtn, 'text', x))
        self.dropdown.bind()

        self.update_list()

        self.add_widget(self.mainbtn)
    def update_list(self):
        self.dropdown.clear_widgets()
        for task in self.tasks:
            btn = Button(text=task, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        






class CountDown(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5

        self.timer = 0
        self.open = "0:00:00"

        self.counter = Label(text=self.open)

        self.start_button = Button(text="Start")
        self.start_button.bind(on_press=self.startTimer)

        self.stop_button = Button(text="Stop")
        self.stop_button.bind(on_press=self.stopTimer)
        
        self.taskselector = TaskSelector()

        self.newTaskButton = Button(text="New", size_hint_x=0.3)
        self.newTaskButton.bind(on_press=self.newTask)
        self.delTaskButton = Button(text="Delete", size_hint_x=0.3)
        self.delTaskButton.bind(on_press=self.deleteTask)
        self.new_task_popup_content = GridLayout(cols=1)
        self.new_task_input = TextInput()
        self.new_task_popup_content.add_widget(self.new_task_input)
        self.new_task_button = Button(text="Add")
        self.new_task_button.bind(on_press=self.addNewTask)
        
        self.new_task_popup_content.add_widget(self.new_task_button)
        self.new_task_popup = Popup(title="New Task", content=self.new_task_popup_content, size_hint=(None, None), size=(200, 200))
        
        

        self.add_widget(self.taskselector)
        self.add_widget(self.delTaskButton)
        self.add_widget(self.newTaskButton)
        self.add_widget(self.counter)
        self.add_widget(self.start_button)

    def newTask(self, instance):
        self.new_task_input.text=""
        self.new_task_popup.open()
    
    def deleteTask(self, instance):
        current = self.taskselector.mainbtn.text
        if current == "Task":
            return
        self.taskselector.tasks.pop(self.taskselector.tasks.index(current))
        self.taskselector.mainbtn.text = "Task"
        self.taskselector.update_list()
    
    def addNewTask(self, instance):
        self.taskselector.tasks.append(self.new_task_input.text)
        with open("tasks.txt", "w") as t:
            for task in self.taskselector.tasks:
                t.write(task + "\n")
        self.taskselector.update_list()
        self.new_task_popup.dismiss()

    def startTimer(self, instance):
        if self.taskselector.mainbtn.text == "Task":
            return
        
        self.taskselector.disabled = True
        self.newTaskButton.disabled = True
        self.timerEvent = Clock.schedule_interval(self.incrementTimer, 1)
        self.button = self.stop_button
        self.remove_widget(self.start_button)
        self.add_widget(self.stop_button)


    def stopTimer(self, instance):
        self.timerEvent.cancel()
        self.addEntry()
        self.timer = 0
        self.counter.text = self.open

        self.taskselector.disabled = False
        self.newTaskButton.disabled = False
        
        self.remove_widget(self.stop_button)
        self.add_widget(self.start_button)

    def addEntry(self):
        string = str(self.taskselector.mainbtn.text) + "  " + str(timedelta(seconds=self.timer))
        myApp.main_screen.entries.add_entry(string)
        with open("times.txt", "a") as t:
            t.write(string + "\n")

        
    def incrementTimer(self, instance):
        time = self.timer
        time += 1
        self.timer = time
        self.counter.text = str(timedelta(seconds=self.timer))


class BaseWindow(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        self.entries = ScrollOutput(size_hint_y=0.9)

        self.timer = CountDown(size_hint_y=0.1)

    
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