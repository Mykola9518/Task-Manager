import database
database.init_db()
import AddTask
from tabulate import tabulate

tasks = []

def main_menu():
    while True:
        print ("TASK MANAGER")
        try:
            print(
            'Select action:\n'
            '1 - Add a task \n'
            '2 - Show all tasks\n'
            '3 - Find a task\n'
            '4 - Task filter\n'
            '5 - Edit task\n'
            '6 - Delete task\n'
            '7 - Mark as done or Mark as not done\n'
            '8 - Export to CSV\n'
            '9 - Export to PDF\n'
            '10 - Quit\n'
            '11 - Clear all tasks\n'
            )
            select_action = input("Enter operation: ").strip()
            if select_action == '1':
                new_tasks = AddTask.add_task_menu()
                for task in new_tasks:
                    database.insert_task(task)
                print("Tasks saved to database!")

            elif select_action == '2':
                rows = database.get_all_tasks()
                if not rows:
                    print("No tasks yet")
                else:
                    table = []
                    for row in rows:
                        task_id, title, description, deadline, priority, completed = row
                        status = "\u2714 Completed" if completed else "\u274C In the process"
                        table.append([task_id, title, description, priority, deadline, status])
                    print(tabulate(
                        table,
                        headers=["ID", "Title", "Description", "Priority", "Deadline", "Status"],
                        tablefmt="grid"
                    ))
            elif select_action == '3':
                print('Find a task')
                keyword = input("Enter part of the title: ").strip()

                rows = database.search_by_title(keyword)

                if not rows:
                    print("No tasks found")
                else:
                    table = []
                    for row in rows:
                        task_id, title, description, deadline, priority, completed = row
                        status = "\u2714 Completed" if completed else "\u274C In the process"
                        table.append([task_id, title, description, priority, deadline, status])

                    print(tabulate(
                        table,
                        headers=["ID", "Title", "Description", "Priority", "Deadline", "Status"],
                        tablefmt="grid"
                    ))


            elif select_action == '4':
                print("\nTask filter:")
                print("1 - By priority")
                print("2 - By status")
                print("3 - By deadline (before date)")

                f = input("Choose filter: ").strip()

                if f == "1":
                    priority = input("Enter priority (low/medium/high): ").strip().lower()
                    rows = database.filter_by_priority(priority)

                elif f == "2":
                    status = input("Enter status (done / process): ").strip().lower()
                    completed = 1 if status == "done" else 0
                    rows = database.filter_by_status(completed)

                elif f == "3":
                    date_str = input("Enter date (dd.mm.yyyy): ").strip()
                    rows = database.filter_by_deadline_before(date_str)

                else:
                    print("Wrong filter")
                    continue

                if not rows:
                    print("No tasks found")
                else:
                    table = []
                    for row in rows:
                        task_id, title, description, deadline, priority, completed = row
                        status = "\u2714 Completed" if completed else "\u274C In the process"
                        table.append([task_id, title, description, priority, deadline, status])

                    print(tabulate(
                        table,
                        headers=["ID", "Title", "Description", "Priority", "Deadline", "Status"],
                        tablefmt="grid"
                    ))

            elif select_action == '5':
                print("\nEdit task")

                rows = database.get_all_tasks()
                if not rows:
                    print("No tasks to edit")
                    continue

                table = []
                for row in rows:
                    task_id, title, description, deadline, priority, completed = row
                    status = "\u2714 Completed" if completed else "\u274C In process"
                    table.append([task_id, title, description, priority, deadline, status])

                print(tabulate(
                    table,
                    headers=["ID", "Title", "Description", "Priority", "Deadline", "Status"],
                    tablefmt="grid"
                ))

                try:
                    task_id = int(input("Enter task ID to edit: ").strip())
                except ValueError:
                    print("Invalid ID")
                    continue

                print("\nLeave field empty to keep current value.")

                new_title = input("New title: ").strip()
                new_description = []

                print("New description (Type 'END' to finish, leave empty to keep current):")
                while True:
                    line = input()
                    if line.lower() == "end":
                        break
                    if line == "":
                        new_description = None
                        break
                    new_description.append(line)

                if new_description:
                    new_description = "\n".join(new_description)

                new_deadline = input("New deadline (dd.mm.yyyy): ").strip()
                new_priority = input("New priority (low/medium/high): ").strip()

                new_title = new_title if new_title else None
                new_deadline = new_deadline if new_deadline else None
                new_priority = new_priority if new_priority else None

                if database.update_task(task_id, new_title, new_description, new_deadline, new_priority):
                    print("Task updated successfully")
                else:
                    print("Task not found")

            elif select_action == '6':
                print('Delete task')

                rows = database.get_all_tasks()
                if not rows:
                    print("No tasks to delete")
                    continue

                table = []
                for row in rows:
                    task_id, title, description, deadline, priority, completed = row
                    status = "\u2714 Completed" if completed else "\u274C In the process"
                    table.append([task_id, title, description, priority, deadline, status])

                print(tabulate(
                    table,
                    headers=["ID", "Title", "Description", "Priority", "Deadline", "Status"],
                    tablefmt="grid"
                ))

                try:
                    task_id = int(input("Enter task ID to delete: ").strip())
                except ValueError:
                    print("Invalid ID")
                    continue

                if database.delete_task(task_id):
                    print(f"Task {task_id} deleted successfully")
                else:
                    print("Task not found")

            elif select_action == '7':
                print('Mark as done or Mark as not done')
                print("1 - Mark as done")
                print("2 - Mark as NOT done")

                sub = input("Choose option: ").strip()

                rows = database.get_all_tasks()
                if not rows:
                    print("No tasks available")
                    continue

                table = []
                for row in rows:
                    task_id, title, description, deadline, priority, completed = row
                    status = "\u2714 Completed" if completed else "\u274C In the process"
                    table.append([task_id, title, description, priority, deadline, status])

                print(tabulate(
                    table,
                    headers=["ID", "Title", "Description", "Priority", "Deadline", "Status"],
                    tablefmt="grid"
                ))

                try:
                    task_id = int(input("Enter task ID: ").strip())
                except ValueError:
                    print("Invalid ID")
                    continue

                if sub == "1":
                    if database.mark_task_done(task_id):
                        print(f"Task {task_id} marked as completed")
                    else:
                        print("Task not found")

                elif sub == "2":
                    if database.mark_task_not_done(task_id):
                        print(f"Task {task_id} marked as NOT completed")
                    else:
                        print("Task not found")

                else:
                    print("Wrong option")

            elif select_action == '8':
                if database.export_to_csv():
                    print("Tasks exported to tasks.csv")

            elif select_action == '9':
                if database.export_to_pdf():
                    print("Tasks exported to tasks.pdf")

            elif select_action == '10':
                print('Quit the program')
                break

            elif select_action == '11':
                confirm = input("Are you sure you want to delete ALL tasks? (yes/no): ").strip().lower()
                if confirm == "yes":
                    database.clear_all_tasks()
                    print("All tasks deleted.")
                else:
                    print("Cancelled.")

            else:
                raise ValueError('Not corrected operation')
        except:
            print('Error, not corrected operation')
if __name__ == "__main__":
    main_menu()


