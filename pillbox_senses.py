#!/usr/bin/python3

'''
Author: Loti Ibrahimi (20015453)
Course: BSc (Hons) in the Internet of Things.

Script Overview:
* Look out for & read in data from the hall-effect sensor. (1:magnetic field near or 0:magnetic field far)
* Sending this data to a Realtime DB. 
* RTDB defined under pillBoxData > boxSensors / boxSensorMemory
* Continues to listen and post new events.  
'''

# Import required libraries
import time, datetime
import RPi.GPIO as GPIO

# Firebase Admin SDK 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/home/pi/Documents/Smart-Pillbox/firebase-sdk/thesmartpillbox-ffb73-firebase-adminsdk-q4yrs-ddd08428fc.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://thesmartpillbox-ffb73-default-rtdb.firebaseio.com/"
})

sense_pin = 17

def detect(channel):
    timestamp = datetime.datetime.now().strftime('Time: %H:%M:%S, Date: %d/%m/%Y')

    boxLidStatus = int(GPIO.input(channel))

    # Defined data variables to be sent to Firebase.
    data = {
        'boxLidStatus': boxLidStatus,
        'timestamp': timestamp,
    }

    if GPIO.input(channel) == 0: #if low (0) sensor value
        print('Sensor low detected  [',GPIO.input(channel),'] - [Box Lid Opened]; Magnet far; [', timestamp, ']')
        # Sending data to 'boxAccessData' in Firebase Realtime.
        # Update the 'current' data under 'boxAccessData' 
        db.reference('/').child('pillBoxData').child('boxSensors').set(data)
        # Update the 'history' data under 'boxAccessData', with a history of pushes. 
        db.reference('/').child('pillBoxData').child('boxSensorMemory').push(data)

    else: 
        print('Sensor high detected [',GPIO.input(channel),'] - [Box Lid CLosed]; Magnet near; [', timestamp, ']')
        # Update the 'current' data under 'boxAccessData' 
        db.reference('/').child('pillBoxData').child('boxSensors').set(data)
        # Update the 'history' data under 'boxAccessData', with a history of pushes. 
        db.reference('/').child('pillBoxData').child('boxSensorMemory').push(data)

# Main
def main():
    print('')
    print('=====================================================')
    print('      Actively Monitoring Pillbox sensor data        ')
    print('=====================================================')
    print('\n [CTRL + C to quit]')
    print('')
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

GPIO.setmode(GPIO.BCM)
GPIO.setup(sense_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(sense_pin, GPIO.BOTH, callback=detect)

if __name__=="__main__":
    main()