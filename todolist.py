import json
from datetime import datetime, date

class Task:
    def __init__(self, description, due_date=None, priority=1, completed=False):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["description"])
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date() if data["due_date"] else None
        task.priority = data["priority"]
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, description, due_date=None, priority=1):
        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        task = Task(description, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return

        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task.completed else "✗"
            due = f"Due: {task.due_date}" if task.due_date else "No due date"
            print(f"{i}. [{status}] {task.description} (Priority: {task.priority}) - {due}")

    def mark_complete(self, index):
        if 1 <= index <= len(self.tasks):
            self.tasks[index-1].completed = True
            self.save_tasks()
            print("Task marked as complete!")
        else:
            print("Invalid task index.")

    def remove_task(self, index):
        if 1 <= index <= len(self.tasks):
            del self.tasks[index-1]
            self.save_tasks()
            print("Task removed successfully!")
        else:
            print("Invalid task index.")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            self.tasks = []

def main():
    todo_list = ToDoList()

    while True:
        print("\n--- To-Do List Application ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Remove Task")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            priority = int(input("Enter priority (1-5): "))
            todo_list.add_task(description, due_date if due_date else None, priority)
        elif choice == "2":
            todo_list.view_tasks()
        elif choice == "3":
            index = int(input("Enter the task number to mark as complete: "))
            todo_list.mark_complete(index)
        elif choice == "4":
            index = int(input("Enter the task number to remove: "))
            todo_list.remove_task(index)
        elif choice == "5":
            print("Thank you for using the To-Do List application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()