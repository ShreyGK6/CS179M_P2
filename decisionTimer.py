import os
import time
import threading

timeout_ocurred = False
decision_made = False

def timeout_handler(duration_sec = 300):
    global timeout_ocurred, decision_made
    checkpoints = {60,120,180,240}
    for elapsed in range(1,duration_sec + 1):
        time.sleep(1)
        if decision_made:
            return
        remaining = duration_sec - elapsed
        if remaining in checkpoints:
            minutes_left = remaining //60
            print(f"\n {minutes_left} minute{'s' if minutes_left > 1 else ''}left to decide.")
    timeout_ocurred = True
    print("\n[ERROR] Decision time expired (5 minutes). Program terminated.\n")
    os._exit(1)

#used threading to start a timer in the background
def start_decision_timer(duration_sec = 300):
    global timeout_ocurred, decision_made
    timeout_ocurred = False
    decision_made = False
    timer_thread = threading.Thread(target = timeout_handler, args=(duration_sec,),daemon=True)
    timer_thread.start()
    return timer_thread

def stop_decision_timer():
    global timeout_ocurred, decision_made
    decision_made = True
    
