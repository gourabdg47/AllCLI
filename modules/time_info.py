from datetime import datetime

def time_info():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    day_str = now.strftime("%A")
    time_str = now.strftime("%H-%M-%S")
    return date_str, day_str, time_str
