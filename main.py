import time
import win32gui
from collections import defaultdict
import json
from datetime import datetime

def save_to_file(data):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'app_usage_{date_str}.json'
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def get_foreground_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

def convert_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return {"seconds": seconds, "minutes": minutes, "hours": hours}

def track_app_usage(interval=1):
    app_usage = defaultdict(float)
    last_app = None
    last_time = time.time()

    while True:
        try:
            current_time = time.time()
            current_app = get_foreground_window_title()

            if current_app != last_app:
                if last_app is not None:
                    app_usage[last_app] += current_time - last_time
                last_app = current_app
                last_time = current_time

            time.sleep(interval)
        except KeyboardInterrupt:
            if last_app is not None:
                app_usage[last_app] += time.time() - last_time

            formatted_app_usage = {
                app: convert_seconds(time) for app, time in app_usage.items()
            }
            return formatted_app_usage

if __name__ == "__main__":
    try:
        print("Starting app usage tracker. Press Ctrl+C to stop.")
        app_usage = track_app_usage()
    except KeyboardInterrupt:
        print("Stopping app usage tracker.")
    finally:
        save_to_file(app_usage)
        print("App usage data saved to JSON file.")
