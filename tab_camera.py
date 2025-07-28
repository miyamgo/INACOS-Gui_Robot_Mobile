from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
import cv2
import mediapipe as mp
import time

# Import shared_data
from temp_sending import shared_data


class CameraTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #444444;")
        self.paused = False

        # === Video Display ===
        self.video_label = QLabel()
        self.video_label.setStyleSheet("background-color: black; border-radius: 12px;")
        self.video_label.setFixedSize(640, 480)

        # === Pause Button ===
        self.pause_button = QPushButton()
        self.pause_button.setFixedSize(640, 60)
        self.pause_button.setCheckable(True)
        self.pause_icon = QIcon("image/icons/pause.png")
        self.play_icon = QIcon("image/icons/play.png")
        self.pause_button.setIconSize(self.pause_button.size())
        self.update_pause_button_style()
        self.pause_button.clicked.connect(self.toggle_pause)

        # === Indicators ===
        self.fps_widget, self.fps_value = self.create_indicator("image/icons/fps.png", "FPS")
        self.hand_widget, self.hand_value = self.create_indicator("image/icons/hands.png", "Hands")
        self.conf_widget, self.conf_value = self.create_indicator("image/icons/conf.png", "Confidence")
        self.output_widget, self.output_value = self.create_indicator("image/icons/output.png", "Output")

        self.output_value.setFixedWidth(120)
        
        indicators_layout = QHBoxLayout()
        indicators_layout.setSpacing(20)
        indicators_layout.setContentsMargins(10, 10, 10, 10)
        indicators_layout.addWidget(self.fps_widget)
        indicators_layout.addWidget(self.hand_widget)
        indicators_layout.addWidget(self.conf_widget)
        indicators_layout.addWidget(self.output_widget)

        indicators_frame = QFrame()
        indicators_frame.setStyleSheet("background-color: #444444; border-radius: 12px;")
        indicators_frame.setLayout(indicators_layout)

        # === Layout Kiri: Kamera + Pause
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        left_layout.addWidget(self.video_label)
        left_layout.addWidget(self.pause_button)

        # === Main Layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(40)
        main_layout.addLayout(left_layout)
        main_layout.addWidget(indicators_frame, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

        # === MediaPipe Init ===
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.prev_time = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_pause_button_style(self):
        icon = self.play_icon if self.paused else self.pause_icon
        self.pause_button.setStyleSheet("QPushButton { background-color: #1C1C1C; border-radius: 8px; }")
        self.pause_button.setIcon(icon)

    def create_indicator(self, icon_path, label_text):
        icon = QLabel()
        icon.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(icon_path).scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 13px; color: white;")

        value = QLabel("-")
        value.setAlignment(Qt.AlignCenter)
        value.setStyleSheet("font-size: 15px; font-weight: bold; color: white;")

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addWidget(value)

        frame = QFrame()
        frame.setLayout(layout)
        frame.setStyleSheet("background-color: transparent; border-radius: 10px;")
        return frame, value

    def toggle_pause(self):
        self.paused = not self.paused
        self.update_pause_button_style()

    def check_fingers(self, handLms, handedness_label):
        fingers = []
        if handedness_label == "Right":
            fingers.append(1 if handLms.landmark[4].x < handLms.landmark[3].x else 0)
        else:
            fingers.append(1 if handLms.landmark[4].x > handLms.landmark[3].x else 0)

        tips_ids = [8, 12, 16, 20]
        for tip in tips_ids:
            fingers.append(1 if handLms.landmark[tip].y < handLms.landmark[tip - 2].y else 0)

        if sum(fingers) == 1:
            return "Index"
        elif sum(fingers) == 5:
            return "Open"
        elif sum(fingers) == 0:
            return "Fist"
        return "None"  # ✅ ganti Unknown → None

    def update_frame(self):
        success, frame = self.cap.read()
        if not success:
            return

        frame = cv2.flip(frame, 1)

        if self.paused:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.show_frame(frame)
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        h, w, _ = frame.shape

        # ✅ Default jadi None jika tidak terdeteksi
        left_gesture = "None"
        right_gesture = "None"
        confidence = 0.0
        hand_count = 0

        if results.multi_hand_landmarks and results.multi_handedness:
            for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = handedness.classification[0].label
                gesture = self.check_fingers(handLms, label)

                if label == "Left":
                    left_gesture = gesture
                elif label == "Right":
                    right_gesture = gesture

                confidence = handedness.classification[0].score
                hand_count += 1

                # Status di layar kamera
                cx = int(handLms.landmark[0].x * w)
                cy = int(handLms.landmark[0].y * h)
                cv2.putText(frame, f"{label} - {gesture}", (cx - 50, cy - 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                self.mp_draw.draw_landmarks(
                    frame, handLms, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)
                )

        curr_time = time.time()
        fps = int(1 / (curr_time - self.prev_time)) if self.prev_time else 0
        self.prev_time = curr_time

        self.fps_value.setText(str(fps))
        self.hand_value.setText(str(hand_count))
        self.conf_value.setText(f"{confidence:.2f}")
        self.output_value.setText(f"{left_gesture} | {right_gesture}")

        # === Update shared_data ===
        shared_data["left_motor_camera"] = self.gesture_to_motor_value(left_gesture)
        shared_data["right_motor_camera"] = self.gesture_to_motor_value(right_gesture)

        self.show_frame(frame)

    def gesture_to_motor_value(self, gesture):
        if gesture == "Index":
            return 1
        elif gesture == "Fist":
            return -1
        elif gesture in ["Open", "None"]:  # ✅ None sama seperti stop
            return 0
        return 0

    def show_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()
