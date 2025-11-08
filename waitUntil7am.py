from datetime import datetime
import sys

def check_if_7am():
    now = datetime.now()
    if now.hour < 7:
        print("\nIts not 7:00am yet. Mr.Keogh doesnt have the data.")
        print("Please run this program at or after 7:00am.")
        sys.exit(0)