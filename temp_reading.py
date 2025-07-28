import threading
import os
from connect_db import get_device_ping_value  # ✅ ambil device ping dari connect_db
from connect_db import get_identity_value

identity_data = {
    "pass": "-",
    "ip_address": "-",
    "mac_address": "-",
    "connection": 800  # default awal (ms)
}

last_valid_connection = 800
zero_count = 0  # hitung berapa kali berturut-turut dapat 0

def get_identity_data():
    """
    Ambil hanya data ip address, mac address, dan pass
    untuk ditampilkan di GUI.
    """
    identity, _ = get_identity_value()
    return {
        "ip address": identity.get("ip address", "-"),
        "mac address": identity.get("mac address", "-"),
        "pass": identity.get("pass", "-")
    }

def print_identity_data():
    os.system("cls" if os.name == "nt" else "clear")
    print("=== Identity Data Monitor ===")
    for key, value in identity_data.items():
        print(f"{key:<12}: {value}")
    print("==============================")


def update_identity_loop():
    global last_valid_connection, zero_count

    while True:
        current_device_ping = get_device_ping_value()

        if current_device_ping == 0 or current_device_ping is None:
            zero_count += 1
            if zero_count >= 5:
                identity_data["connection"] = 800
                last_valid_connection = 800
            else:
                identity_data["connection"] = last_valid_connection
        else:
            identity_data["connection"] = current_device_ping
            last_valid_connection = current_device_ping
            zero_count = 0  # reset karena sudah dapat nilai valid

        print_identity_data()


threading.Thread(target=update_identity_loop, daemon=True).start()
