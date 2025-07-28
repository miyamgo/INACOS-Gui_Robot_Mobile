import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDesktopWidget,
    QVBoxLayout, QPushButton, QSplitter, QFrame, QStackedWidget,
    QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap

# Import tab-tab dari file lain
from tab_camera import CameraTab
from tab_keyboard import KeyboardTab
from tab_control import ControlTab
from tab_connection import ConnectionTab

# Import identity data
from connect_db import get_identity_value, get_device_ping_value


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("INACOS")
        self.setGeometry(0, 0, 1200, 800)
        self.setFixedSize(1200, 800)
        self.setWindowIcon(QIcon("image/icons/icon.jpg"))
        self.center()

        # === Widget utama dan layout ===
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: white;")

        # === Splitter: Sidebar | Konten ===
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        # === Sidebar ===
        self.sidebar = QFrame()
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar.setMinimumWidth(150)
        self.sidebar.setMaximumWidth(200)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #1C1C1C;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #4A4A4A;
                color: white;
            }
        """)

        icon_size = QSize(24, 24)

        # Tombol navigasi
        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedWidth(40)
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        self.btn_camera = QPushButton("  Camera")
        self.btn_camera.setIcon(QIcon("image/icons/camera.png"))
        self.btn_camera.setIconSize(icon_size)

        self.btn_keyboard = QPushButton("  Keyboard")
        self.btn_keyboard.setIcon(QIcon("image/icons/keyboard.png"))
        self.btn_keyboard.setIconSize(icon_size)

        self.btn_control = QPushButton("  Control")
        self.btn_control.setIcon(QIcon("image/icons/control.png"))
        self.btn_control.setIconSize(icon_size)

        self.btn_connection = QPushButton("  Connection")
        self.btn_connection.setIcon(QIcon("image/icons/connection.png"))
        self.btn_connection.setIconSize(icon_size)

        self.btn_camera.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_keyboard.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_control.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_connection.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        # Layout Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.toggle_button, alignment=Qt.AlignLeft)
        sidebar_layout.addWidget(self.btn_camera)
        sidebar_layout.addWidget(self.btn_keyboard)
        sidebar_layout.addWidget(self.btn_control)
        sidebar_layout.addWidget(self.btn_connection)
        sidebar_layout.addStretch()

        # Tombol Exit
        self.btn_exit = QPushButton("  Exit")
        self.btn_exit.setIcon(QIcon("image/icons/exit.png"))
        self.btn_exit.setIconSize(icon_size)
        self.btn_exit.clicked.connect(QApplication.quit)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #d0312d;
                color: white;
                font-weight: bold;
                border: none;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #ff3c6d;
            }
        """)
        sidebar_layout.addWidget(self.btn_exit)
        self.sidebar.setLayout(sidebar_layout)

        # === Konten Kanan ===
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)

        # Bagian atas: Logo + Identity Info
        top_layout = QHBoxLayout()

        # Logo Organisasi
        logo_label = QLabel()
        pixmap = QPixmap()
        if pixmap.load("Main_Logo.jpg"):
            pixmap = pixmap.scaledToHeight(80, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("Logo not found")
            logo_label.setStyleSheet("color: red; font-size: 14px;")
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        # === Identity Info + Status ===
        right_info_layout = QVBoxLayout()
        right_info_layout.setSpacing(0)
        right_info_layout.setContentsMargins(0, 0, 0, 0)

        self.identity_label = QLabel("IP: - | MAC: - | PASS: -")
        self.identity_label.setStyleSheet("""
            font-size: 18px; 
            color: #333333; 
            line-height: 10px;
        """)
        self.identity_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.status_label = QLabel("Status: Offline")
        self.status_label.setStyleSheet("""
            font-size: 20px; 
            color: red; 
            line-height: 10px;
        """)
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        right_info_layout.addWidget(self.identity_label)
        right_info_layout.addWidget(self.status_label)
        top_layout.addLayout(right_info_layout)
        content_layout.addLayout(top_layout)

        # Stack widget (tab area)
        self.stack = QStackedWidget()
        self.stack.addWidget(CameraTab())
        self.stack.addWidget(KeyboardTab())
        self.stack.addWidget(ControlTab())
        self.stack.addWidget(ConnectionTab())
        self.stack.setStyleSheet("""
            QStackedWidget {
                border-radius: 15px;
                background-color: transparent;
                margin: 5px;
            }
        """)
        content_layout.addWidget(self.stack)

        # Tambahkan ke splitter
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(content_widget)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.handle(1).setEnabled(False)

        self.sidebar_expanded = True

        # Timer untuk update identity info setiap detik
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_identity_info)
        self.timer.start(1000)

    def update_identity_info(self):
        # Ambil data identity (IP, MAC, PASS)
        identity, _ = get_identity_value()
        self.identity_label.setText(
            f"IP: {identity['ip address']} | MAC: {identity['mac address']} | PASS: {identity['pass']}"
        )

        # Ambil status koneksi device
        ping_device = get_device_ping_value()
        status = "Online" if ping_device < 800 else "Offline"
        color = "green" if status == "Online" else "red"
        self.status_label.setText(f"<span style='color:{color};'>Status: {status}</span>")

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.setMaximumWidth(100)
            self.sidebar.setMinimumWidth(100)
            self.sidebar_expanded = False
        else:
            self.sidebar.setMaximumWidth(200)
            self.sidebar.setMinimumWidth(150)
            self.sidebar_expanded = True

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(1500, 800)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
