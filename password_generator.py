import sys
import random
import string
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QRadioButton, QButtonGroup, QSlider, QLabel,
    QLineEdit, QPushButton, QProgressBar
)
from PyQt5.QtGui import QFont, QFontDatabase, QMovie
from PyQt5.QtCore import Qt

STRENGTH_CAPTIONS = {
    1: "This password couldn't scare a mouse.",
    2: "Baa-sic at best.",
    3: "Getting fierce... sort of.",
    4: "Bear-ly anyone's cracking this.",
    5: "An unstoppable password. Respect the trunk.",
}


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")
        self.setFixedSize(500, 680)

        font_path = "assets/Mochibop-Demo.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Failed to load font at {font_path} — check filename/extension.")
            self.caption_font_family = "Arial"
        else:
            self.caption_font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- Mode toggle ---
        mode_layout = QHBoxLayout()
        self.characters_radio = QRadioButton("Characters")
        self.words_radio = QRadioButton("Words")
        self.characters_radio.setChecked(True)

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.characters_radio)
        self.mode_group.addButton(self.words_radio)

        mode_layout.addWidget(self.characters_radio)
        mode_layout.addWidget(self.words_radio)
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)

        # --- Sliders ---
        length_row, self.length_slider = self.create_slider_row("Length", 4, 32, 6)
        digits_row, self.digits_slider = self.create_slider_row("Digits", 0, 10, 4)
        capitals_row, self.capitals_slider = self.create_slider_row("Capitals", 0, 10, 2)
        symbols_row, self.symbols_slider = self.create_slider_row("Symbols", 0, 10, 2)

        main_layout.addLayout(length_row)
        main_layout.addLayout(digits_row)
        main_layout.addLayout(capitals_row)
        main_layout.addLayout(symbols_row)

        # --- Animal display ---
        self.animal_label = QLabel()
        self.animal_label.setAlignment(Qt.AlignCenter)
        self.animal_label.setFixedHeight(180)

        self.caption_label = QLabel()
        self.caption_label.setAlignment(Qt.AlignCenter)
        self.caption_label.setWordWrap(True)
        caption_font = QFont(self.caption_font_family)
        caption_font.setPointSize(24)
        self.caption_label.setFont(caption_font)

        main_layout.addWidget(self.animal_label)
        main_layout.addWidget(self.caption_label)

        # --- Password display ---
        password_row = QHBoxLayout()
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setAlignment(Qt.AlignLeft)

        self.refresh_button = QPushButton("↻")
        self.refresh_button.setFixedWidth(40)
        self.refresh_button.clicked.connect(self.generate_password)

        password_row.addWidget(self.password_display)
        password_row.addWidget(self.refresh_button)
        main_layout.addLayout(password_row)

        # --- Strength bar ---
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(100)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(6)
        main_layout.addWidget(self.strength_bar)

        self.strength_animation = QPropertyAnimation(self.strength_bar, b"value")
        self.strength_animation.setDuration(300)
        self.strength_animation.setEasingCurve(QEasingCurve.OutCubic)

        # --- Copy / Use buttons ---
        button_row = QHBoxLayout()
        button_row.setSpacing(12)
        self.copy_button = QPushButton("📋 Copy")
        self.use_button = QPushButton("Use Password")
        self.copy_button.setObjectName("copyButton")
        self.use_button.setObjectName("useButton")

        self.copy_button.clicked.connect(self.copy_password)

        button_row.addWidget(self.copy_button, stretch=1)
        button_row.addWidget(self.use_button, stretch=1)
        main_layout.addLayout(button_row)

        self.setLayout(main_layout)

        # --- Wire up live updates ---
        self.length_slider.valueChanged.connect(self.generate_password)
        self.digits_slider.valueChanged.connect(self.generate_password)
        self.capitals_slider.valueChanged.connect(self.generate_password)
        self.symbols_slider.valueChanged.connect(self.generate_password)
        self.characters_radio.toggled.connect(self.on_mode_changed)
        self.password_display.textChanged.connect(self.on_manual_password_typed)

        self.generate_password()

    def create_slider_row(self, label_text, min_val, max_val, default_val):
        label = QLabel(label_text)
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        value_label = QLabel(str(default_val))

        slider.valueChanged.connect(lambda val: value_label.setText(str(val)))

        row = QHBoxLayout()
        row.addWidget(label)
        row.addWidget(slider)
        row.addWidget(value_label)
        return row, slider

    def update_animal(self, tier):
        movie = QMovie(f"assets/strength{tier}.gif")
        movie.setScaledSize(self.animal_label.size())
        self.animal_label.setMovie(movie)
        movie.start()
        self.current_movie = movie

        self.caption_label.setText(STRENGTH_CAPTIONS.get(tier, ""))

    def generate_password(self):
        if self.words_radio.isChecked():
            return

        length = self.length_slider.value()
        digits = self.digits_slider.value()
        capitals = self.capitals_slider.value()
        symbols = self.symbols_slider.value()

        lowercase_count = max(length - digits - capitals - symbols, 0)

        password_chars = (
            random.choices(string.ascii_lowercase, k=lowercase_count) +
            random.choices(string.digits, k=digits) +
            random.choices(string.ascii_uppercase, k=capitals) +
            random.choices(string.punctuation, k=symbols)
        )
        random.shuffle(password_chars)
        password = "".join(password_chars)[:length]

        self.password_display.setText(password)
        self.update_strength(password)

    def update_strength(self, password):
        score = 0
        if len(password) >= 8:
            score += 25
        if any(c.isdigit() for c in password):
            score += 25
        if any(c.isupper() for c in password):
            score += 25
        if any(c in string.punctuation for c in password):
            score += 25

        self.strength_animation.stop()
        self.strength_animation.setStartValue(self.strength_bar.value())
        self.strength_animation.setEndValue(score)
        self.strength_animation.start()

        if score <= 20:
            color, tier = "#e74c3c", 1
        elif score <= 40:
            color, tier = "#e67e22", 2
        elif score <= 60:
            color, tier = "#f1c40f", 3
        elif score <= 80:
            color, tier = "#3498db", 4
        else:
            color, tier = "#2ecc71", 5

        self.strength_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
        self.update_animal(tier)

    def on_mode_changed(self):
        if self.words_radio.isChecked():
            self.password_display.setReadOnly(False)
            self.password_display.clear()
            self.password_display.setPlaceholderText("Type your own password...")
        else:
            self.password_display.setReadOnly(True)
            self.generate_password()

    def on_manual_password_typed(self, text):
        if self.words_radio.isChecked():
            self.update_strength(text)

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())


app = QApplication(sys.argv)

with open("Style-calculator.qss", "r") as f:
    app.setStyleSheet(f.read())

window = PasswordGenerator()
window.show()
sys.exit(app.exec_())