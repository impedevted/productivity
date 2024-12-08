import sys
import os
from datetime import datetime

HOSTS_FILE = "/etc/hosts"
REDIRECT_IP = "127.0.0.1"

def block_website(website):
    """
    Add an entry to /etc/hosts to block the website.
    """
    with open(HOSTS_FILE, "r+") as hosts_file:
        content = hosts_file.read()
        if website not in content:
            hosts_file.write(f"{REDIRECT_IP} {website}\n")
            hosts_file.write(f"{REDIRECT_IP} www.{website}\n")

def unblock_website(website):
    """
    Remove the entry from /etc/hosts to unblock the website.
    """
    with open(HOSTS_FILE, "r") as hosts_file:
        lines = hosts_file.readlines()
    with open(HOSTS_FILE, "w") as hosts_file:
        for line in lines:
            if website not in line:
                hosts_file.write(line)

def add_cron_jobs(website, start_time, end_time):
    """
    Add cron jobs to block and unblock the website at specific times.
    """
    block_command = f"python3 {os.path.abspath(__file__)} block {website}\n"
    unblock_command = f"python3 {os.path.abspath(__file__)} unblock {website}\n"

    # Validate the time format
    try:
        datetime.strptime(start_time, "%H:%M")
        datetime.strptime(end_time, "%H:%M")
    except ValueError:
        print("Invalid time format. Use HH:MM (24-hour format).")
        sys.exit(1)

    # Prepare cron jobs
    cron_block = f"{start_time.split(':')[1]} {start_time.split(':')[0]} * * * {block_command}"
    cron_unblock = f"{end_time.split(':')[1]} {end_time.split(':')[0]} * * * {unblock_command}"

    # Write to crontab
    os.system(f'(crontab -l 2>/dev/null; echo "{cron_block}") | crontab -')
    os.system(f'(crontab -l 2>/dev/null; echo "{cron_unblock}") | crontab -')

    print(f"Blocking schedule set for {website}:")
    print(f" - Block starts at {start_time}")
    print(f" - Block ends at {end_time}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python block_website.py <block/unblock> <website> [<start_time> <end_time>]")
        print("Example to block immediately: python block_website.py block youtube.com")
        print("Example to schedule: python block_website.py schedule youtube.com 8:00 19:00")
        sys.exit(1)

    action = sys.argv[1]
    website = sys.argv[2]

    if action == "block":
        block_website(website)
    elif action == "unblock":
        unblock_website(website)
    elif action == "schedule" and len(sys.argv) == 5:
        start_time = sys.argv[3]
        end_time = sys.argv[4]
        add_cron_jobs(website, start_time, end_time)
    else:
        print("Invalid usage or missing arguments.")
        sys.exit(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root. Use sudo.")
        sys.exit(1)
    main()
