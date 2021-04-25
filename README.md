# smart-pillbox-code
Smart Pillbox Code - Box Sensor(s) / Pill Schedules
![alt text](https://github.com/loti-ibrahimi/smart-pillbox-code/blob/master/smart-pillbox.jpg)

### Three main scripts (run on RaspberryPi startup using Crontab):
- **pillbox_schedules.py**: script which checks and fetches database schedules; displays information on LCD and pushes events to a realtime databse (for different alerts).
- **pillbox_senses.py**: script that reads the Hall-effect sensor data and sends events to the realtime database (is box lid **open** or **closed**).
- **pillbox_alerts.py**: event listener script that listens for alert events and carries out appropriate SMS notifications.

### Other script(s):
- **add_update_schedules.py**: Script for updating schedules (ideally would be replaced with a user interface on a webapp featuring CRUD functionality.
- **firestore-db-test.py**: Test script for Firebase DB queries. 
- **lcd_test.py**: Test script for different LCD displays options. 

### Library Script:
- **grove_rgb_lcd.py**: library for Grove LCD functionality, containing some basic callable functions to get a simple Grove LCD displaying text.
