import datetime
class Task:
    def __init__(self, title = None, description = None, deadline = None, priority = None):
        self.title_task = title
        self.description = description
        self.deadline = deadline
        self.priority = priority

    def add_title(self):
        title = [input("Enter a task name: ")]
        title.append({"title": "title", "done": False})
        print("Task added")

    def add_description(self):
        description = {}

add_task = Task('title', 'description', 'deadline', 'priority')
add_task.title_task = {"ID":"title"}
add_task.description = []
add_task.deadline = datetime
add_task.priority = 'Hight' or 'Middle' or 'Low'
add_task.add_title()