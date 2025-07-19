'''
📝 Task: System Resource Monitoring CLI Dashboard
Context:
We often run lightweight scripts from the command line (CLI) to monitor key resource metrics like CPU, memory, and disk usage. 
These help us troubleshoot performance issues quickly or include them in larger automated monitoring workflows.
🎯 Objective:
Build a basic CLI dashboard that shows real-time (or near real-time) system resource usage.
✅ Requirements:
    Display the following stats in a clean CLI format:
        Current CPU usage (e.g., % used)
        Memory usage (% used)
        Disk usage (% used for root partition)
    Output format example:
========== System Resource Dashboard ==========
CPU Usage   : 28.7%
Memory Usage: 62.4%
Disk Usage  : 79.2%
===============================================
Use Python with the psutil library. Install with:
pip install psutil
BONUS (optional but valuable):

    Refresh every 5 seconds using a loop.

    Clear screen between refreshes (os.system("cls" if os.name == "nt" else "clear")).

    Add a timestamp at the top.

    Stop after 5 refreshes or press Ctrl+C to quit.
'''
'''
We are not taking any arguments from the user or terminal so we don't need the argparse module
We can use the psutil python library to get the stats and then just print them
Add small features a real engineer might:

    ✅ Add argparse so user can do:
        --interval 2 (refresh every 2 sec)
        --cycles 10 (run for 10 cycles)
    ✅ Add log output to a .txt file (timestamped)
    ✅ Add alerts (e.g., warn if CPU > 80%)
'''

import psutil
import time
from datetime import datetime
import argparse


def get_real_time_cpu_metrics():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\nTimestamp: {timestamp}")
    print("========== System Resource Dashboard ==========")
    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=1)  # CPU utilization over 1 second
    print(f"CPU Usage\t: {cpu_percent}%")
    if cpu_percent > 80:
        print("WARNING, THE CPU PERCENTAGE IS GREATER THAN 80%.") #can also use the logging module
     # Memory Usage
    memory_info = psutil.virtual_memory()
    print(f"Memory Usage\t: {memory_info.used / (1024**3):.2f} GB ({memory_info.percent}%)")

    # Disk Usage (for a specific partition, e.g., root)
    disk_usage = psutil.disk_usage('/')
    print(f"Disk Usage\t: {disk_usage.used / (1024**3):.2f} GB ({disk_usage.percent}%)")

    print("===============================================")

    with open("dashboard_report.txt", "a") as f:
        f.write(f"{timestamp}\n")
        f.write(f"CPU Usage: {cpu_percent}%, Memory Usage: {memory_info.percent}%, Disk Usage: {disk_usage.percent}%\n")

def main():
    count=0
    parser = argparse.ArgumentParser(description="CLI Dashboard")
    parser.add_argument("-i", "--interval", help="The time in seconds for refresh")
    parser.add_argument("-c", "--cycle", help="The amount of cycles program will run")

    arguments = parser.parse_args()
    
    try:
        interval = int(arguments.interval)
        cycle = int(arguments.cycle)
        while True:
            get_real_time_cpu_metrics()
            count+=1
            time.sleep(interval)
            if count == cycle:
                break
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()