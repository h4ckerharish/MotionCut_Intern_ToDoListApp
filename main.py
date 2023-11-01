import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QFormLayout, QTableWidget, QTableWidgetItem, QSizePolicy, QHBoxLayout, QDateEdit, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate

class Task:
    def __init__(self, description, due_date, priority):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, due_date, priority):
        task = Task(description, due_date, priority)
        self.tasks.append(task)

    def display_tasks(self):
        return self.tasks

    def mark_as_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = True

    def update_task(self, task_index, description, due_date, priority):
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            task.description = description
            task.due_date = due_date
            task.priority = priority

    def remove_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]

class UpdateTaskDialog(QDialog):
    def __init__(self, task):
        super(UpdateTaskDialog, self).__init__()
        self.task = task
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Update Task")
        self.layout = QFormLayout()

        self.description_input = QLineEdit()
        self.description_input.setText(self.task.description)
        self.layout.addRow("Description:", self.description_input)

        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.fromString(self.task.due_date, "yyyy-MM-dd"))
        self.layout.addRow("Due Date:", self.due_date_input)

        # Create a combo box for priority levels (1 to 10)
        self.priority_input = QComboBox()
        priority_levels = list(map(str, range(1, 11)))
        self.priority_input.addItems(priority_levels)
        self.priority_input.setCurrentText(self.task.priority)
        self.layout.addRow("Priority:", self.priority_input)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_task)
        self.layout.addRow(self.update_button)

        self.setLayout(self.layout)

    def update_task(self):
        description = self.description_input.text()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        priority = self.priority_input.currentText()

        self.task.description = description
        self.task.due_date = due_date
        self.task.priority = priority

        self.accept()

class ToDoListApp(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.initUI()
        self.todo_list = ToDoList()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.task_list_label = QLabel("Task List:")
        self.layout.addWidget(self.task_list_label)

        self.task_list_table = QTableWidget()
        self.task_list_table.setColumnCount(6)
        self.task_list_table.setHorizontalHeaderLabels(["Task No", "Description", "Due Date", "Priority", "Status", "Actions"])
        self.task_list_table.setColumnWidth(5, 500)
        self.task_list_table.verticalHeader().setDefaultSectionSize(50)
        self.layout.addWidget(self.task_list_table)

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_task_button)

        self.description_input = QLineEdit()
        self.due_date_input = QDateEdit()
        self.priority_input = QComboBox()
        priority_levels = list(map(str, range(1, 11)))
        self.priority_input.addItems(priority_levels)
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Description:", self.description_input)
        self.form_layout.addRow("Due Date:", self.due_date_input)
        self.form_layout.addRow("Priority:", self.priority_input)
        self.layout.addLayout(self.form_layout)

        self.central_widget.setLayout(self.layout)

    def add_task(self):
        description = self.description_input.text()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        priority = self.priority_input.currentText()
        if description:
            self.todo_list.add_task(description, due_date, priority)
            self.update_task_list()
            self.clear_input_fields()

    def mark_as_completed(self, task_index):
        if 0 <= task_index < len(self.todo_list.tasks):
            self.todo_list.mark_as_completed(task_index)
            self.update_task_list()

    def update_task(self, task_index):
        if 0 <= task_index < len(self.todo_list.tasks):
            task = self.todo_list.tasks[task_index]
            dialog = UpdateTaskDialog(task)
            if dialog.exec_():
                self.todo_list.update_task(task_index, task.description, task.due_date, task.priority)
                self.update_task_list()

    def remove_task(self, task_index):
        if 0 <= task_index < len(self.todo_list.tasks):
            self.todo_list.remove_task(task_index)
            self.update_task_list()

    def update_task_list(self):
        self.task_list_table.setRowCount(len(self.todo_list.tasks))
        for i, task in enumerate(self.todo_list.tasks):
            status = "Completed" if task.completed else "Incomplete"
            task_num_item = QTableWidgetItem(str(i + 1))
            task_desc_item = QTableWidgetItem(task.description)
            task_due_item = QTableWidgetItem(task.due_date)
            task_priority_item = QTableWidgetItem(task.priority)
            status_item = QTableWidgetItem(status)
            
            # Create buttons for actions
            mark_completed_button = QPushButton("Mark as Completed")
            mark_completed_button.clicked.connect(lambda _, i=i: self.mark_as_completed(i))
            update_button = QPushButton("Update")
            update_button.clicked.connect(lambda _, i=i: self.update_task(i))
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, i=i: self.remove_task(i))
            
            # Adjust the button size
            button_size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            mark_completed_button.setSizePolicy(button_size_policy)
            update_button.setSizePolicy(button_size_policy)
            remove_button.setSizePolicy(button_size_policy)
            
            # Set icons to buttons (you can provide icon paths)
            mark_completed_button.setIcon(QIcon("res/MarkasComplete.png"))  
            update_button.setIcon(QIcon("res/modifyicon.png"))  
            remove_button.setIcon(QIcon("res/removetask.png"))  
            
            # Add buttons to a container widget
            buttons_container = QWidget()
            buttons_layout = QHBoxLayout()
            buttons_layout.addWidget(mark_completed_button)
            buttons_layout.addWidget(update_button)
            buttons_layout.addWidget(remove_button)
            buttons_container.setLayout(buttons_layout)
            
            # Set items and widgets in the table
            self.task_list_table.setItem(i, 0, task_num_item)
            self.task_list_table.setItem(i, 1, task_desc_item)
            self.task_list_table.setItem(i, 2, task_due_item)
            self.task_list_table.setItem(i, 3, task_priority_item)
            self.task_list_table.setItem(i, 4, status_item)
            self.task_list_table.setCellWidget(i, 5, buttons_container)

    def clear_input_fields(self):
        self.description_input.clear()
        self.due_date_input.setDate(QDate.currentDate())
        self.priority_input.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    window = ToDoListApp()
    window.setWindowTitle("To-Do List App")
    window.setGeometry(100, 100, 1150, 720)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
