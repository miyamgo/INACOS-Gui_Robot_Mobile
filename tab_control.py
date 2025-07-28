from PyQt5.QtWidgets import (
    QWidget, QSlider, QLabel, QFrame, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from temp_sending import shared_data  # Pastikan path ini sesuai

class ControlTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1250, 520)

        # === Frame kiri: Slider ===
        slider_frame = QFrame(self)
        slider_frame.setFixedSize(170, 500)
        slider_frame.move(0, 20)
        slider_frame.setStyleSheet("background-color: #444444; border-radius: 12px;")

        icon_label = QLabel(slider_frame)
        icon_pixmap = QPixmap("image/icons/speed.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setGeometry(65, 10, 40, 40)

        caption_label = QLabel("Speed", slider_frame)
        caption_label.setStyleSheet("color: white; font-size: 14px;")
        caption_label.setAlignment(Qt.AlignCenter)
        caption_label.setGeometry(35, 50, 100, 20)

        self.slider = QSlider(Qt.Vertical, slider_frame)
        self.slider.setGeometry(50, 80, 20, 380)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)
        self.slider.setStyleSheet("""
            QSlider::groove:vertical {
                background: #888;
                width: 10px;
                border-radius: 5px;
            }
            QSlider::handle:vertical {
                background: white;
                width: 32px;
                height: 32px;
                margin: 0 -7px;
                border-radius: 16px;
            }
        """)
        self.slider.valueChanged.connect(self.on_slider_change)

        self.value_label = QLabel("0", slider_frame)
        self.value_label.setStyleSheet("color: white; font-size: 26px; background: transparent;")
        self.value_label.setFixedWidth(50)
        self.value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.update_label_position(self.slider.value())

        # === Frame Mode ===
        mode_frame = QFrame(self)
        mode_frame.setFixedSize(250, 350)
        mode_frame.move(185, 20)
        mode_frame.setStyleSheet("background-color: #444444; border-radius: 12px;")

        self.mode_index = 0
        self.mode_icons = ["image/icons/key.png", "image/icons/ges.png"]

        self.mode_icon_label = QLabel(mode_frame)
        self.mode_icon_label.setAlignment(Qt.AlignCenter)
        self.mode_icon_label.setGeometry(50, 20, 150, 150)

        self.mode_caption = QLabel("Control Mode", mode_frame)
        self.mode_caption.setStyleSheet("color: white; font-size: 16px;")
        self.mode_caption.setAlignment(Qt.AlignCenter)
        self.mode_caption.setGeometry(50, 180, 150, 30)

        self.mode_button = QPushButton("Change", mode_frame)
        self.mode_button.setGeometry(75, 240, 100, 40)
        self.mode_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        self.mode_button.clicked.connect(self.change_mode_icon)
        self.update_mode_icon()

        # === Frame Light ===
        light_frame = QFrame(self)
        light_frame.setFixedSize(250, 350)
        light_frame.move(185 + 250 + 15, 20)
        light_frame.setStyleSheet("background-color: #444444; border-radius: 12px;")

        self.light_index = 1  # Mulai dari OFF
        self.light_icons = ["image/icons/on.png", "image/icons/off.png"]

        self.light_icon_label = QLabel(light_frame)
        self.light_icon_label.setAlignment(Qt.AlignCenter)
        self.light_icon_label.setGeometry(50, 20, 150, 150)

        self.light_caption = QLabel("Light Mode", light_frame)
        self.light_caption.setStyleSheet("color: white; font-size: 16px;")
        self.light_caption.setAlignment(Qt.AlignCenter)
        self.light_caption.setGeometry(50, 180, 150, 30)

        self.light_button = QPushButton("Change", light_frame)
        self.light_button.setGeometry(75, 240, 100, 40)
        self.light_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        self.light_button.clicked.connect(self.change_light_icon)
        self.update_light_icon()

        # === Frame Sound ===
        sound_frame = QFrame(self)
        sound_frame.setFixedSize(250, 350)
        sound_frame.move(185 + 250*2 + 15*2, 20)
        sound_frame.setStyleSheet("background-color: #444444; border-radius: 12px;")

        self.sound_index = 1  # Mulai dari OFF
        self.sound_icons = ["image/icons/sound_on.png", "image/icons/sound_off.png"]

        self.sound_icon_label = QLabel(sound_frame)
        self.sound_icon_label.setAlignment(Qt.AlignCenter)
        self.sound_icon_label.setGeometry(50, 20, 150, 150)

        self.sound_caption = QLabel("Sound Mode", sound_frame)
        self.sound_caption.setStyleSheet("color: white; font-size: 16px;")
        self.sound_caption.setAlignment(Qt.AlignCenter)
        self.sound_caption.setGeometry(50, 180, 150, 30)

        self.sound_button = QPushButton("Change", sound_frame)
        self.sound_button.setGeometry(75, 240, 100, 40)
        self.sound_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        self.sound_button.clicked.connect(self.change_sound_icon)
        self.update_sound_icon()

    def update_label_position(self, value):
        self.value_label.setText(str(value))
        slider_height = self.slider.height()
        slider_range = self.slider.maximum() - self.slider.minimum()
        handle_height = 32
        usable_height = slider_height - handle_height
        relative_pos = (value - self.slider.minimum()) / slider_range
        handle_y = int(usable_height * (1 - relative_pos)) + self.slider.y()
        self.value_label.move(self.slider.x() + 30, handle_y - 10)

    def on_slider_change(self, value):
        self.update_label_position(value)
        shared_data["speed"] = value

    def update_mode_icon(self):
        pixmap = QPixmap(self.mode_icons[self.mode_index]).scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.mode_icon_label.setPixmap(pixmap)
        shared_data["mode"] = self.mode_index

    def change_mode_icon(self):
        self.mode_index = (self.mode_index + 1) % len(self.mode_icons)
        self.update_mode_icon()

    def update_light_icon(self):
        pixmap = QPixmap(self.light_icons[self.light_index]).scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.light_icon_label.setPixmap(pixmap)
        shared_data["light"] = 0 if self.light_index == 1 else 1

    def change_light_icon(self):
        self.light_index = (self.light_index + 1) % len(self.light_icons)
        self.update_light_icon()

    def update_sound_icon(self):
        pixmap = QPixmap(self.sound_icons[self.sound_index]).scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.sound_icon_label.setPixmap(pixmap)
        shared_data["sound"] = 0 if self.sound_index == 1 else 1

    def change_sound_icon(self):
        self.sound_index = (self.sound_index + 1) % len(self.sound_icons)
        self.update_sound_icon()
