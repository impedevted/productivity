# Block Website Script

This Python script allows you to block a specific website (e.g., `youtube.com`) on a Linux system during specified time periods or immediately. It modifies the `/etc/hosts` file to redirect the website to `127.0.0.1`, effectively blocking access.

## Prerequisites

- Python 3 installed on your system.
- Root privileges (required to modify `/etc/hosts` and set up cron jobs).

## How to Use

### 1. Save the Script

Save the script as `block_website.py` on your system.

### 2. Make the Script Executable

Run the following command to make the script executable:
```bash
chmod +x block_website.py
```

### 3. Usage 

Block a Website Immediately
```bash
sudo python3 block_website.py block youtube.com
```

Unblock a Website
```bash
sudo python3 block_website.py unblock youtube.com
```

Schedule Blocking
```bash
sudo python3 block_website.py schedule youtube.com 8:00 19:00
```

### 4. How It Works
#### Blocking via /etc/hosts
* The script modifies the /etc/hosts file to redirect the domain (e.g., youtube.com and www.youtube.com) to 127.0.0.1, effectively blocking access to the website.
#### Cron Jobs
* The script schedules blocking and unblocking tasks using cron. At the specified times, the script will:
  * Add entries to /etc/hosts to block the website.
  * Remove entries from /etc/hosts to unblock the website.
#### HTTPS Support
* By overriding DNS resolution via /etc/hosts, the script effectively blocks both HTTP and HTTPS traffic for the specified domains.
#### Managing Cron Jobs
* View Existing Cron Jobs
To view all scheduled cron jobs for the current user:

```bash
crontab -l
```

Remove All Cron Jobs
To remove all cron jobs for the current user (be cautious, this will delete all existing cron jobs):

```bash
crontab -r
```

Example Cron Job
When scheduling blocking, the script automatically creates cron jobs like the following:

Block YouTube at 8:00 AM:

cron
Copy code
0 8 * * * python3 /path/to/block_website.py block youtube.com
Unblock YouTube at 7:00 PM:

cron
Copy code
0 19 * * * python3 /path/to/block_website.py unblock youtube.com
##### Notes
Root Privileges: Editing /etc/hosts and managing cron require root privileges, so always run the script with sudo.
Scheduling Time Format: Use 24-hour time format for scheduling (e.g., 8:00 for 8 AM, 19:00 for 7 PM).
DNS Caching: Browsers or the system may cache DNS responses. Restart your browser or flush DNS if changes do not take effect immediately.


bash
Copy code
crontab -l
Remove All Cron Jobs:

bash
Copy code
crontab -r

