import sys   # Helps with command line arguments
import os    # Helps with file paths
import json  # Helps save/load tasks to a file
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFrame, QLineEdit, QDateEdit, QTimeEdit, QGraphicsView, QGraphicsScene
)
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtGui import QFontDatabase, QIcon, QPainter, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, QDate, QTime, QPropertyAnimation


class Task:
    """Represents one to-do item. Kept as a plain data class, separate from
    any PyQt widgets, so it's easy to save/load and reason about."""

    def __init__(self, text, date, time, done=False):
        self.text = text
        self.date = date
        self.time = time
        self.done = done

    def to_dict(self):
        return {"text": self.text, "date": self.date, "time": self.time, "done": self.done}

    @staticmethod
    def from_dict(data):
        return Task(data["text"], data["date"], data["time"], data["done"])


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-do List")
        self.setFixedSize(400, 700)

        self.icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

        self.load_fonts()

        self.today_str = QDate.currentDate().toString("d MMMM yyyy")

        all_tasks = self.load_tasks()
        self.today_tasks = [t for t in all_tasks if t.date == self.today_str]
        self.workspace_tasks = [t for t in all_tasks if t.date != self.today_str]

        layout = QVBoxLayout()

        # ---------- Header row (gear, title, search, bell) ----------
        header_row = QHBoxLayout()

        gear_icon = QPushButton()
        gear_icon.setIcon(QIcon(os.path.join(self.icon_dir, "settings.svg")))
        gear_icon.setObjectName("iconButton")

        title = QLabel("To - Do List")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)

        search_icon = QPushButton()
        search_icon.setIcon(QIcon(os.path.join(self.icon_dir, "search.svg")))
        search_icon.setObjectName("iconButton")

        bell_icon = QPushButton()
        bell_icon.setIcon(QIcon(os.path.join(self.icon_dir, "notification.svg")))
        bell_icon.setObjectName("iconButton")

        header_row.addWidget(gear_icon)
        header_row.addWidget(title)
        header_row.addWidget(search_icon)
        header_row.addWidget(bell_icon)

        layout.addLayout(header_row)

        # ---------- Date row ----------
        today_label = QLabel("Today,")
        today_label.setObjectName("todayLabel")
        layout.addWidget(today_label)

        date_label = QLabel(self.today_str)
        date_label.setObjectName("dateLabel")
        layout.addWidget(date_label)

        # ---------- "Today" section header ----------
        section_row = QHBoxLayout()

        section_title = QLabel("Today")
        section_title.setObjectName("sectionTitle")

        self.today_count_label = QLabel(str(len(self.today_tasks)))
        self.today_count_label.setObjectName("countBadge")

        section_row.addWidget(section_title)
        section_row.addWidget(self.today_count_label)
        section_row.addStretch()

        collapse_btn = QPushButton()
        collapse_btn.setIcon(QIcon(os.path.join(self.icon_dir, "arrow.svg")))
        collapse_btn.setIconSize(QSize(24, 25))
        collapse_btn.setObjectName("collapseButton")
        section_row.addWidget(collapse_btn)

        layout.addLayout(section_row)

        self.today_layout = QVBoxLayout()
        for task in self.today_tasks:
            self.today_layout.addWidget(self.create_task_card(task))
        layout.addLayout(self.today_layout)

        collapse_btn.clicked.connect(lambda: self.toggle_section(self.today_layout))

        # ---------- "Workspace" section header ----------
        section_row2 = QHBoxLayout()

        section_title2 = QLabel("Workspace")
        section_title2.setObjectName("sectionTitle")

        self.workspace_count_label = QLabel(str(len(self.workspace_tasks)))
        self.workspace_count_label.setObjectName("countBadge")

        section_row2.addWidget(section_title2)
        section_row2.addWidget(self.workspace_count_label)
        section_row2.addStretch()

        collapse_btn2 = QPushButton()
        collapse_btn2.setIcon(QIcon(os.path.join(self.icon_dir, "arrow.svg")))
        collapse_btn2.setIconSize(QSize(24, 25))
        collapse_btn2.setObjectName("collapseButton")
        section_row2.addWidget(collapse_btn2)

        layout.addLayout(section_row2)

        self.workspace_layout = QVBoxLayout()
        for task in self.workspace_tasks:
            self.workspace_layout.addWidget(self.create_task_card(task))
        layout.addLayout(self.workspace_layout)

        collapse_btn2.clicked.connect(lambda: self.toggle_section(self.workspace_layout))

        # ---------- Add task input row ----------
        self.task_input = QLineEdit()
        self.task_input.setObjectName("taskInput")
        self.task_input.setPlaceholderText("Add a new task...")
        layout.addWidget(self.task_input)

        picker_row = QHBoxLayout()

        self.date_picker = QDateEdit()
        self.date_picker.setObjectName("datePicker")
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)

        self.time_picker = QTimeEdit()
        self.time_picker.setObjectName("timePicker")
        self.time_picker.setTime(QTime.currentTime())

        add_btn = QPushButton("+")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.add_task)
        self.task_input.returnPressed.connect(self.add_task)

        picker_row.addWidget(self.date_picker)
        picker_row.addWidget(self.time_picker)
        picker_row.addWidget(add_btn)

        layout.addLayout(picker_row)

        layout.addStretch()

        self.setLayout(layout)

        # ---------- Spinning flower decorations (small, peeking in at the corners) ----------
       

    # ---------------------------------------------------------------
    # Fonts
    # ---------------------------------------------------------------
    def load_fonts(self):
        font_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
        for font_file in ["Kapakana-Regular.ttf", "IndieFlower-Regular.ttf", "InriaSerif-Regular.ttf"]:
            path = os.path.join(font_dir, font_file)
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id == -1:
                print(f"Failed to load font: {font_file}")

    # ---------------------------------------------------------------
    # Spinning flower decoration (reusable for multiple flowers of different sizes)
    # ---------------------------------------------------------------
    

    # ---------------------------------------------------------------
    # Collapse / expand a section
    # ---------------------------------------------------------------
    def toggle_section(self, section_layout):
        if section_layout.count() == 0:
            return
        first_widget = section_layout.itemAt(0).widget()
        if not first_widget:
            return
        now_visible = not first_widget.isVisible()

        for i in range(section_layout.count()):
            widget = section_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(now_visible)

    # ---------------------------------------------------------------
    # Building one task card widget
    # ---------------------------------------------------------------
    def create_task_card(self, task):
        card = QFrame()
        card.setObjectName("taskCard")

        card_layout = QHBoxLayout()

        checkbox = QCheckBox()
        checkbox.setChecked(task.done)
        checkbox.setObjectName("taskCheckbox")

        text_container = QVBoxLayout()

        task_label = QLabel(task.text)
        task_label.setObjectName("taskText")
        task_label.setWordWrap(True)

        if task.done:
            font = task_label.font()
            font.setStrikeOut(True)
            task_label.setFont(font)

        tags_row = QHBoxLayout()

        date_tag = QLabel(task.date)
        date_tag.setObjectName("dateTag")
        tags_row.addWidget(date_tag)

        if task.time:
            time_tag = QLabel(task.time)
            time_tag.setObjectName("timeTag")
            tags_row.addWidget(time_tag)

        tags_row.addStretch()

        text_container.addWidget(task_label)
        text_container.addLayout(tags_row)

        delete_btn = QPushButton("✕")
        delete_btn.setObjectName("deleteButton")

        card_layout.addWidget(checkbox)
        card_layout.addLayout(text_container)
        card_layout.addWidget(delete_btn)

        card.setLayout(card_layout)

        checkbox.stateChanged.connect(lambda state: self.toggle_task_done(task, task_label, state))
        delete_btn.clicked.connect(lambda: self.delete_task(task, card))

        return card

    # ---------------------------------------------------------------
    # Task actions
    # ---------------------------------------------------------------
    def add_task(self):
        text = self.task_input.text().strip()
        if not text:
            return

        date_str = self.date_picker.date().toString("d MMMM yyyy")
        time_str = self.time_picker.time().toString("hh:mm ap")

        new_task = Task(text, date_str, time_str)
        new_card = self.create_task_card(new_task)

        if date_str == self.today_str:
            self.today_tasks.append(new_task)
            self.today_layout.addWidget(new_card)
            self.today_count_label.setText(str(len(self.today_tasks)))
        else:
            self.workspace_tasks.append(new_task)
            self.workspace_layout.addWidget(new_card)
            self.workspace_count_label.setText(str(len(self.workspace_tasks)))

        self.task_input.clear()
        self.save_tasks()

    def toggle_task_done(self, task, task_label, state):
        task.done = bool(state)
        font = task_label.font()
        font.setStrikeOut(task.done)
        task_label.setFont(font)
        self.save_tasks()

    def delete_task(self, task, card):
        if task in self.today_tasks:
            self.today_tasks.remove(task)
            self.today_count_label.setText(str(len(self.today_tasks)))
        elif task in self.workspace_tasks:
            self.workspace_tasks.remove(task)
            self.workspace_count_label.setText(str(len(self.workspace_tasks)))

        card.setParent(None)
        self.save_tasks()

    # ---------------------------------------------------------------
    # Persistence (save/load tasks.json)
    # ---------------------------------------------------------------
    def save_tasks(self):
        all_tasks = self.today_tasks + self.workspace_tasks
        with open(self.data_file, "w") as f:
            json.dump([task.to_dict() for task in all_tasks], f, indent=2)

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    raw_data = json.load(f)
                return [Task.from_dict(item) for item in raw_data]
            except (json.JSONDecodeError, KeyError):
                pass

        return [
            Task("Application for UN Internship", QDate.currentDate().toString("d MMMM yyyy"), "09:00 am"),
            Task("Research on club work", "6 July 2026", ""),
            Task("Write an email to the class teacher.", "Tomorrow", "09:45 pm"),
        ]

    def closeEvent(self, event):
        self.save_tasks()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())