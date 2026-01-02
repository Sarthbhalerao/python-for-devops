import os
import time
import json
import smtplib
from email.message import EmailMessage

import psutil

CONFIG_FILE = "7.2_config.json" # all related configuration details are stored in this file
# function to get current timestamp
def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


# function to load configuration
def load_config(file_name=CONFIG_FILE):
    """Load SMTP configuration from JSON file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)
        with open(file_path, "r") as f:
            return json.load(f)["smtp"]
    except Exception as err:
        print(f"Failed to load config file: {err}")
        exit(1)

# function to send email alert
def send_email_alert(subject, body, smtp_config):
    try:
        msg = EmailMessage()
        msg["From"] = smtp_config["sender_email"]
        msg["To"] = smtp_config["receiver_email"]
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP(smtp_config["server"], smtp_config["port"]) as server:
            server.starttls()
            server.login(
                smtp_config["sender_email"],
                smtp_config["sender_password"]
            )
            server.send_message(msg)
        print("Alert email sent successfully!")
    except Exception as err:
        print(f"Email sending failed: {err}")

# function to get threshold limit
def get_threshold_input(metric_name):
    while True:
        try:
            threshold_value = float(input(f"Enter {metric_name} utilization threshold : "))
            if 0 <= threshold_value <= 100:
                return threshold_value
            else:
                print("Threshold value must be between 0 to 100.")
        except ValueError:
            print("Invalid input, Please enter a number.")

# function to get current system usage
def get_system_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    return cpu_usage, memory_usage, disk_usage

def evaluate_alerts(cpu_usage, memory_usage, disk_usage, cpu_threshold, memory_threshold, disk_threshold):
    alerts = [] # List to collect alert messages

    if cpu_usage > cpu_threshold:
        alerts.append(f"CPU usage high: {cpu_usage}% (Threshold: {cpu_threshold}%)")
        print("ALERT: CPU threshold breached!")
    else:
        print("CPU usage is normal.")

    if memory_usage > memory_threshold:
        alerts.append(f"Memory usage high: {memory_usage}% (Threshold: {memory_threshold}%)")
        print("ALERT: Memory threshold breached!")
    else:
        print("Memory usage is normal.")

    if disk_usage > disk_threshold:
        alerts.append(f"Disk usage high: {disk_usage}% (Threshold: {disk_threshold}%)")
        print("ALERT: Disk threshold breached!")
    else:
        print("Disk usage is normal.")

    return alerts


def main():
    smtp_config = load_config() # Load SMTP configuration
    print("\nPLEASE PROVIDE THRESHOLD!!!\n")
    cpu_threshold = get_threshold_input("CPU")
    memory_threshold = get_threshold_input("Memory")
    disk_threshold = get_threshold_input("Disk")
    print(f"\n----------------------------------------------------------------")
    print(f"\nCheking Current System Usage ({timestamp()})....\n")
    cpu_usage, memory_usage, disk_usage = get_system_usage()
    print(f"Current CPU usage : ",cpu_usage,"%")
    print(f"Current Memory usage : ",memory_usage,"%")
    print(f"Current Disk usage : ",disk_usage,"%")
    print(f"\nResult : ")
    print("\n----------------------------------------------------------------")
    alerts = evaluate_alerts(cpu_usage, memory_usage, disk_usage, cpu_threshold, memory_threshold, disk_threshold)
    print("\n----------------------------------------------------------------")
    if alerts:
        email_body = f"🚨 System Health Alert ({timestamp()})\n\n" + "\n".join(alerts)
        send_email_alert("System Health Alert", email_body, smtp_config)
    else:
        print("System is healthy. No alerts triggered.")

if __name__ == "__main__": # __main__ block is used to execute some code only if the file was run directly, and not imported as a module.
    main()

