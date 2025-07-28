import threading
import time
import os
from connect_db import update_outputs

shared_data = {
    "mode": 0,
    "light": 0,
    "sound": 0,
    "speed": 0,
    "left_motor_camera": 0,
    "right_motor_camera": 0,
    "left_motor_keyboard": 0,
    "right_motor_keyboard": 0
}

def print_shared_data():
    os.system("cls" if os.name == "nt" else "clear")
    print("=== Shared Data Monitor ===")
    for key, value in shared_data.items():
        print(f"{key:<25}: {value if value is not None else '[waiting]'}")
    print("============================")

def send_to_firebase_if_ready():
    # ✅ SELALU KIRIM (tanpa cek perbedaan)
    update_outputs(
        mode=shared_data.get("mode"),
        speed=shared_data.get("speed"),
        light=shared_data.get("light"),
        sound=shared_data.get("sound"),
        left_camera=shared_data.get("left_motor_camera"),
        right_camera=shared_data.get("right_motor_camera"),
        left_keyboard=shared_data.get("left_motor_keyboard"),
        right_keyboard=shared_data.get("right_motor_keyboard")
    )
    print("\n[✓] Data dikirim ke Firebase!")

def loop_monitor():
    while True:
        print_shared_data()
        send_to_firebase_if_ready()
        time.sleep(0.1)  # ✅ update tiap detik

threading.Thread(target=loop_monitor, daemon=True).start()
