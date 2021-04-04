#!/usr/bin/python

# Import required libraries
import time, datetime
import RPi.GPIO as GPIO
import pyrebase

# Firebase DB Config 
config = {
  "apiKey": "aqHY9rKYT0BX122qqCXDRvtbHgxmDCSe4ivfLZMP",
  "authDomain": "thesmartpillbox-ffb73.firebaseapp.com",
  "databaseURL": "https://thesmartpillbox-ffb73-default-rtdb.firebaseio.com/",
  "storageBucket": "thesmartpillbox-ffb73.appspot.com"
}

sense_pin = 17

def detect(channel):
    timestamp = datetime.datetime.now().strftime('Time: %H:%M:%S, Date: %d/%m/%Y')

    boxLid = int(GPIO.input(channel))

    # Defined data variables to be sent to Firebase.
    data = {
        'boxAccessStatus': boxLid,
        'timeStamp': timestamp,      
    }

    if GPIO.input(channel) == 0: #if low (0) sensor value
        print('Sensor low detected  [',GPIO.input(channel),'] - [Box Lid Opened]; Magnet far; [', timestamp, ']')
        # Sending data to 'boxAccessData' in Firebase Realtime.
        # Update the '1-set' data under 'boxAccessData' 
        db.child('boxAccessData').child('current').set(data)
        # Update the '2-push' data under 'boxAccessData', with a history of pushes. 
        db.child('boxAccessData').child('history').push(data)

    else: 
        print('Sensor high detected [',GPIO.input(channel),'] - [Box Lid CLosed]; Magnet near; [', timestamp, ']')
        # Update the '1-set' data under 'boxAccessData' 
        db.child('boxAccessData').child('current').set(data)
        # Update the '2-push' data under 'boxAccessData', with a history of pushes. 
        db.child('boxAccessData').child('history').push(data)

# Main
def main():
    print('CTRL + C to quit')
    detect(sense_pin)

    try:
        while True:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            print('System active check', timestamp)
            time.sleep(60)

    except:
        time.sleep(2)
        GPIO.remove_event_detect(sense_pin) #reset interrupt
        GPIO.cleanup()
        print('  Done')


firebase = pyrebase.initialize_app(config)
db = firebase.database()

GPIO.setmode(GPIO.BCM)
GPIO.setup(sense_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(sense_pin, GPIO.BOTH, callback=detect)

if __name__=="__main__":
    main()