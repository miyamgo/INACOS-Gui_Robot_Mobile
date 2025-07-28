import keyboard
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton,
    QGridLayout, QSizePolicy, QLabel
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from temp_sending import shared_data


class KeyboardTab(QWidget):
    def __init__(self):
        super().__init__()

        self.pressed_keys = set()

        # === Layout Horizontal Utama ===
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignTop)

        # === Frame Tombol W A S D ===
        self.control_frame = QFrame()
        self.control_frame.setFixedSize(600, 450)
        self.control_frame.setStyleSheet("background-color: #444444; border-radius: 20px;")

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        self.btn_w = QPushButton("W")
        self.btn_a = QPushButton("A")
        self.btn_s = QPushButton("S")
        self.btn_d = QPushButton("D")

        for btn in (self.btn_w, self.btn_a, self.btn_s, self.btn_d):
            btn.setFixedSize(100, 100)
            btn.setStyleSheet("font-size: 28px; font-weight: bold; background-color: #dddddd; border-radius: 10px;")

        grid.addWidget(self.btn_w, 0, 1)
        grid.addWidget(self.btn_a, 1, 0)
        grid.addWidget(self.btn_s, 1, 1)
        grid.addWidget(self.btn_d, 1, 2)

        self.control_frame.setLayout(grid)

        # === Frame Informasi ===
        self.info_frame = QFrame()
        self.info_frame.setFixedSize(600, 150)
        self.info_frame.setStyleSheet("background-color: #444444; border-radius: 15px;")

        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(25)

        self.label_keys_pressed = QLabel("-")
        self.label_output = QLabel("-")
        self.label_status = QLabel("-")

        def create_info_block(icon_path, caption_text, label_value):
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignTop)

            icon = QLabel()
            icon.setPixmap(QPixmap(icon_path).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.setAlignment(Qt.AlignCenter)

            caption = QLabel(caption_text)
            caption.setStyleSheet("color: white; font-size: 13px;")
            caption.setAlignment(Qt.AlignCenter)

            label_value.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
            label_value.setAlignment(Qt.AlignCenter)

            layout.addWidget(icon)
            layout.addWidget(caption)
            layout.addWidget(label_value)
            return layout

        info_layout.addLayout(create_info_block("image/icons/keyhit.png", "Keys Pressed", self.label_keys_pressed))
        info_layout.addLayout(create_info_block("image/icons/out.png", "Output", self.label_output))
        info_layout.addLayout(create_info_block("image/icons/tokey.png", "Pressed Keys", self.label_status))

        self.info_frame.setLayout(info_layout)

        # === Gabungkan Kedua Frame ke Layout Utama
        main_layout.addWidget(self.control_frame, alignment=Qt.AlignTop)
        main_layout.addWidget(self.info_frame, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

        # Timer untuk update status tombol global
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_keys)
        self.timer.start(100)

    def update_keys(self):
        keys = []
        for k in ['w', 'a', 's', 'd']:
            if keyboard.is_pressed(k):
                keys.append(k.upper())

        # Update informasi tampilan
        self.label_keys_pressed.setText(str(len(keys)))
        self.label_output.setText(self.get_output(keys))
        self.label_status.setText(" + ".join(keys) if keys else "-")

        self.btn_w.setStyleSheet(self.get_btn_style("W" in keys))
        self.btn_a.setStyleSheet(self.get_btn_style("A" in keys))
        self.btn_s.setStyleSheet(self.get_btn_style("S" in keys))
        self.btn_d.setStyleSheet(self.get_btn_style("D" in keys))

        # === Update shared_data motor keyboard ===
        shared_data["left_motor_keyboard"] = self.get_left_motor_value(keys)
        shared_data["right_motor_keyboard"] = self.get_right_motor_value(keys)

    def get_btn_style(self, pressed):
        if pressed:
            return "color: black; font-size: 32px; font-weight: bold; background-color: #dddddd; border-radius: 10px;"
        else:
            return "color: white; font-size: 32px; font-weight: bold; background-color: #1C1C1C; border-radius: 10px;"

    def get_output(self, keys):
        k = set(keys)
        if not k: return "-"
        if k == {"W"}: return "Forward"
        if k == {"S"}: return "Backward"
        if k == {"A"}: return "Left"
        if k == {"D"}: return "Right"
        if k == {"W", "A"}: return "Forward Left"
        if k == {"W", "D"}: return "Forward Right"
        if k == {"S", "A"}: return "Backward Left"
        if k == {"S", "D"}: return "Backward Right"
        return "Mixed"

    def get_left_motor_value(self, keys):
        if "A" in keys: return -1
        if "D" in keys: return 1
        if "W" in keys: return 1
        if "S" in keys: return -1
        return 0

    def get_right_motor_value(self, keys):
        if "D" in keys: return -1
        if "A" in keys: return 1
        if "W" in keys: return 1
        if "S" in keys: return -1
        return 0
