from datetime import datetime
from tabulate import tabulate

class Task:
    priorities = ("low", "medium", "high")
    _id_counter = 1

    def __init__(self, title, description, deadline, priority, completed = False):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.completed = completed

    def to_row(self):
        status = "\u2714 Completed" if self.completed else "\u274C In the process"
        return [
                self.id,
                self.title,
                self.description,
                self.priority,
                self.deadline.strftime('%d.%m.%Y'),
                status
                ]

    def mark_completed(self):
        self.completed = True

    @classmethod
    def from_input(cls):
        print("\nCreate a new task")

        title = input("Task name: ")

        print("Task Description (Type 'END' on a new line to complete): ")
        description = cls._input_multiline()
        deadline = cls._input_deadline()
        priority = cls._input_priority()
        task = cls(title, description, deadline, priority)
        return task

    @staticmethod
    def _input_multiline():
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _input_deadline():
        while True:
            date_str = input("Deadline (дд.мм.гггг): ")
            try:
                return datetime.strptime(date_str, "%d.%m.%Y")
            except ValueError:
                print("\u274C Invalid date format")

    @classmethod
    def _input_priority(cls):
        while True:
            priority = input(
                "Priority (low / medium / high): "
            ).lower()
            if priority in cls.priorities:
                return priority
            print("\u274C Wrong priority")

def add_task_menu():
    tasks_created = []
    while True:
        choice = input("Add a new task? (Yes/No): ").strip().lower()
        if choice == "yes":
            task = Task.from_input()
            tasks_created.append(task)
            print("\nCreated task:")
            print(tabulate(
                [task.to_row()],
                headers=["ID", "Title", "Description", "Priority", "Deadline", "Status"],
                tablefmt="grid"
            ))
        elif choice == "no":
            print("Returning to main menu...")
            return tasks_created
        else: print("Please enter Yes or No")
