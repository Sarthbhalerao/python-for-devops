# Write a Python function to check the CPU utilization of your system. If the CPU utilization is above 75%, print a warning message indicating high CPU usage; otherwise, print a message indicating normal CPU usage.

import psutil
def check_cpu_utilization():
    threshold = int(input("Enter the CPU utilization threshold (in percentage): ")) 
    cpu_utilization = psutil.cpu_percent(interval=1)  # Get CPU utilization over a 1 second interval
    if cpu_utilization > threshold:
        print(f"Warning: High CPU usage detected! Current CPU utilization is {cpu_utilization}%.")
    else:
        print(f"CPU usage is normal. Current CPU utilization is {cpu_utilization}%.")
# Call the function to check CPU utilization
check_cpu_utilization()

def check_memory_utilization():
    threshold = int(input("Enter the Memory utilization threshold (in percentage): ")) 
    memory = psutil.virtual_memory()
    memory_utilization = memory.percent  # Get Memory utilization percentage
    if memory_utilization > threshold:
        print(f"Warning: High Memory usage detected! Current Memory utilization is {memory_utilization}%.")
    else:
        print(f"Memory usage is normal. Current Memory utilization is {memory_utilization}%.")
# call the function to check Memory utilization
check_memory_utilization()

def check_disk_utilization():
    threshold = int(input("Enter the Disk utilization threshold (in percentage): ")) 
    disk = psutil.disk_usage('/')
    disk_utilization = disk.percent  # Get Disk utilization percentage
    if disk_utilization > threshold:
        print(f"Warning: High Disk usage detected! Current Disk utilization is {disk_utilization}%.")
    else:
        print(f"Disk usage is normal. Current Disk utilization is {disk_utilization}%.")
# call the function to check Disk utilization
check_disk_utilization()    

# Note: You may need to install the 'psutil' library if you haven't already. You can do this using pip:
# pip install psutil