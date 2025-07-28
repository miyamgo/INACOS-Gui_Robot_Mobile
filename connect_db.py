import time
import firebase_admin
from firebase_admin import credentials, db

# --- Firebase Init ---
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://imp-inacos-default-rtdb.asia-southeast1.firebasedatabase.app"
    })

# --- Variabel Ping ---
ping = None

# --- Variabel Identity ---
_last_connection_value = 0
_connection_zero_counter = 0
_last_identity_data = {
    "ip address": "-",
    "mac address": "-",
    "pass": "-"
}

# --- Timer reset connection ---
_last_reset_time = 0
RESET_INTERVAL = 10  # detik

def update_outputs(mode, speed, light, sound, left_camera, right_camera, left_keyboard, right_keyboard):
    """Mengirim data ke Firebase + hitung ping"""
    global ping
    start_time = time.time()

    db.reference("/IMPv1/system").update({
        "mode": mode,
        "speed": speed,
        "light": light,
        "sound": sound
    })

    db.reference("/IMPv1/control").update({
        "left_camera": left_camera,
        "right_camera": right_camera,
        "left_keyboard": left_keyboard,
        "right_keyboard": right_keyboard
    })

    # Hitung ping server
    get_identity_value()
    ping = (time.time() - start_time) * 1000


def get_connection_value():
    """Ping ke server (ms), default 800 jika tidak ada"""
    global ping
    return ping if ping is not None else 800


def get_identity_value():
    """
    Ambil data identity (ip, mac, pass, connection)
    Reset connection ke 0 hanya setiap 10 detik.
    """
    global _last_connection_value, _connection_zero_counter, _last_identity_data, _last_reset_time
    try:
        ref = db.reference("/IMPv1/identity")
        data = ref.get() or {}

        # Simpan IP, MAC, PASS
        _last_identity_data["ip address"] = data.get("ip_address", "-")
        _last_identity_data["mac address"] = data.get("mac_address", "-")
        _last_identity_data["pass"] = data.get("pass", "-")

        # Logic connection
        conn = data.get("connection", 0)
        if conn and conn > 0:
            _last_connection_value = conn
            _connection_zero_counter = 0
        else:
            _connection_zero_counter += 1
            if _connection_zero_counter >= 5:
                _last_connection_value = 800

        # --- Reset connection hanya per 10 detik ---
        now = time.time()
        if now - _last_reset_time >= RESET_INTERVAL:
            ref.update({"connection": 0})
            _last_reset_time = now

    except Exception as e:
        print(f"[!] Gagal ambil identity: {e}")
        _last_connection_value = 800

    return _last_identity_data, _last_connection_value


def get_device_ping_value():
    """Device ping = ping server + connection (identity)"""
    server_ping = get_connection_value()
    _, connection = get_identity_value()
    return server_ping + connection
