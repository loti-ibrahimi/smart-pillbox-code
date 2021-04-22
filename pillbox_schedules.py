#!/usr/bin/python3

'''
Author: Loti Ibrahimi (20015453)
Course: BSc (Hons) in the Internet of Things.

Script Overview:
* Setup GPIO pins for the four different LEDs. 
* Access the Firestore DB pillPlans and check the data for 'pillBox_1'. # Each pillbox will have a pillplan assigned to it, with ID being pillBox_<number>
* While at it, also retrieve sensor event data from Firebase Realtime DB. 
- Currently will have access to both the static DB & the realtime DB values needed.

* Loop through the 'pillSchedules' array from 'pillbox_1' data.

Schedule Check algorithm:
1. Pull out all useful schedule variables from the DB that will be used: 
- 'pillDay' e.g. 'Monday'
- 'pillTime' e.g. '15:00'
By subtracting the current real time (in minutes) from the pillTime (converted in minutes), thresholds could be set within scheduled times to perform checks. 
In this case 5 mins was decided as a suitable threshold, with 1 min being critical alert stage.
(This script was configured in Crontab to run automatically every 5 mins, hence why 5 mins was)

* When a schedule is met, a respective LED compartmet [1-4] is lit (showing what pill to take).
* Alert events of either 'scheduleAlert' or 'warningAlert' will be triggered on two conditions:
1. scheduleAlert: schedule is met (within 1 min threshold) SMS alert notification with pill details.
2. warningAlert: check RTDB if pillbox lid is open outside of scheduled times - warning SMS.
'''

# Import required libraries
import time, datetime
import calendar
from datetime import date
import RPi.GPIO as GPIO

# Firebase Admin SDK 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

cred = credentials.Certificate('/home/pi/Documents/Smart-Pillbox/firebase-sdk/thesmartpillbox-ffb73-firebase-adminsdk-q4yrs-ddd08428fc.json')
# firebase_admin.initialize_app(cred)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://thesmartpillbox-ffb73-default-rtdb.firebaseio.com/"
})

dbfirestore = firestore.client()

#Defining LED GPIO ports. 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) # Blue LED (e.g. compartment 1)
GPIO.setup(23, GPIO.OUT) # Yellow LED (e.g compartment 2)
GPIO.setup(24, GPIO.OUT) # Red LED (e.g compartment 3)
GPIO.setup(25, GPIO.OUT) # Green LED (e.g compartment 4)

print('')
print('')
print('============================================================')
print('                Fetching data from Firestore                ')
print('                           ++++++                           ')
print('    Fetching current box sensor data from Firebase RTDB     ')
print('============================================================')
print('')
print('Scanning..')
print('')
time.sleep(5) # sleep 60 seconds.

# Pill Plan for Box 1
docData = dbfirestore.collection('pillPlan').where('boxID', '==', 'pillBox_1').stream()

for doc in docData:
    '''
    pillPlanData = doc.to_dict()
    print('{} => {}'.format(doc.id, doc.to_dict()))
    print('+------------------------------------+')
    print('NEW', pillPlanData)
    print('<=================================================================>')
    '''
    # Get user details
    userDetails = doc.get('contactDetails')

    '''
    Box Sensor Readings. 
    '''
    rtdb = db.reference('pillBoxData').child('boxSensors').get()
    currentBoxLidStatus = rtdb['boxLidStatus']

    # Get all schedules
    schedules = doc.get('pillSchedules')
    for schedule in schedules:
        # Schedule variables
        pillDay = schedule['day']
        todays_date = date.today()
        currentDay = calendar.day_name[todays_date.weekday()]
        pillTime = datetime.datetime.strptime(schedule['time'],'%H:%M')
        pillTimeInMinutes = pillTime.hour*60+pillTime.minute
        currentTime = datetime.datetime.now().strftime('%H:%M')
        currentTimeMinutes = datetime.datetime.now().hour*60 + datetime.datetime.now().minute
        pillCompartment = schedule['pillCompartment']
        pillType = schedule['pillType']
        pillQuantity = schedule['pillQuantity']

        # User details
        contactName = userDetails['name']
        contactNumber = userDetails['phone']

        '''
        # Display all data that was chosen from the Database for schedule analysis
        print('')
        print('Schedule preview          ==> ', schedule)
        print('+--------------------------------------------------------------------+')
        print('Current-Day               ==> ', currentDay)
        print('Pill-Time | In Minutes    ==> ', pillTime,' | ', pillTimeInMinutes)
        print('Current-Time | In Minutes ==> ', currentTime,' | ', currentTimeMinutes)
        print('+--------------------------------------------------------------------+')
        '''
        # Loop through & check if schedules are met.
        while True: 
            # If the current time is within 5 minutes of the scheduled time kick off 
            if abs(pillTimeInMinutes-currentTimeMinutes)<=1 and pillDay == currentDay:
                '''
                Alert Event - Schedule Met
                ----------------------------------
                '''
                # Alert Event triggered - RTDB alertState alert updated to True.
                scheduleAlert = True
                timestamp = datetime.datetime.now().strftime('Time: %H:%M, Date: %d/%m/%Y')

                
                # Defined data variables to be sent to Firebase.
                data = {
                    'alertType': 'scheduleAlert',
                    'alertInfo': 'schedule_due',
                    'alertState': scheduleAlert,
                    'timestamp': timestamp,
                    'pillDue': pillType,
                    'quantityDue': pillQuantity,
                    'contactName': contactName,
                    'contactNumber': contactNumber
                }

                print('*! Alert event sent to Realtime DB !*')
                db.reference('/').child('pillBoxData').child('boxAlerts').set(data)
                # Update the 'history' data under 'boxAccessData', with a history of pushes. 
                db.reference('/').child('pillBoxData').child('boxAlertMemory').push(data)
                '''
                ----------------------------------
                '''

                print('')
                print('Your scheduled pill is now due.')
                print('+ Scheduled Time:', pillTime)
                print('+ Current Time:', currentTime)
                print('+================  PILL DETAILS ==================+')
                print('- Compartment: ', pillCompartment)
                print('- Pill Type:', pillType)
                print('- Pill Quantity:', pillQuantity)
                print('+=================================================+')       
                time.sleep(5)
                print('')
                print('Please take ',pillQuantity, ' pills from the highlighted compartment.')
                # Light appropriate Pill Compartment depending on schedule compartment number.
                if pillCompartment == 1:
                    GPIO.output(25, True) # Turn on Green LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(25, False) # Turn off Green LED
                    print('Until next time!')
                elif pillCompartment == 2:
                    GPIO.output(24, True) # Turn on Red LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(24, False) # Turn off Red LED
                    print('Until next time!')
                elif pillCompartment == 3:
                    GPIO.output(23, True) # Turn on Yellow LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(23, False) # Turn off Yellow LED
                    print('Until next time!')
                elif pillCompartment == 4:
                    GPIO.output(18, True) # Turn on Blue LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(18, False) # Turn off Blue LED
                    print('Until next time!')
                else:
                    GPIO.output(18, False) # Turn off Blue LED
                    GPIO.output(23, False) # Turn off Yellow LED
                    GPIO.output(24, False) # Turn off Red LED
                    GPIO.output(25, False) # Turn off Green LED
                break

            elif abs(pillTimeInMinutes-currentTimeMinutes)<=5 and pillDay == currentDay:
                print('')
                print('Next schedule is near, dont forget to take your pills!')
                print('+ Scheduled Time:', pillTime)
                print('+ Current Time:', currentTime)
                print('+================  PILL DETAILS ==================+')
                print('- Compartment: ', pillCompartment)
                print('- Pill Type:', pillType)
                print('- Pill Quantity:', pillQuantity)
                print('+=================================================+')
                if pillCompartment == 1:
                    GPIO.output(25, True) # Turn on Green LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(25, False) # Turn off Green LED
                    print('Until next time!')
                    break
                elif pillCompartment == 2:
                    GPIO.output(24, True) # Turn on Red LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(24, False) # Turn off Red LED
                    print('Until next time!')
                    break
                elif pillCompartment == 3:
                    GPIO.output(23, True) # Turn on Yellow LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(23, False) # Turn off Yellow LED
                    print('Until next time!')
                    break
                elif pillCompartment == 4:
                    GPIO.output(18, True) # Turn on Blue LED
                    time.sleep(30) # Stay lit for 30 sec.
                    GPIO.output(18, False) # Turn off Blue LED
                    print('Until next time!')
                    break
                else:
                    GPIO.output(18, False) # Turn off Blue LED
                    GPIO.output(23, False) # Turn off Yellow LED
                    GPIO.output(24, False) # Turn off Red LED
                    GPIO.output(25, False) # Turn off Green LED
                break

            elif currentBoxLidStatus == 1:
                print('* Current BOX LID Status:', currentBoxLidStatus, '(Closed)')
                break
            else:
                print('* Current BOX LID Status:', currentBoxLidStatus, '(Open)')
                break

    else:
        if currentBoxLidStatus == 0:
            timestamp = datetime.datetime.now().strftime('Time: %H:%M, Date: %d/%m/%Y')
            print('\n Warning - Pillbox lid is open & no schedule is currently due! \n (', timestamp ,')')
            '''
            Warning (Red Alert) Event - Box opened outside of scheduled hours.
            --------------------------------------------------------------------------
            '''
            # Alert Event triggered - RTDB alertState alert updated to True.
            warningAlert = True
            timestamp = datetime.datetime.now().strftime('Time: %H:%M, Date: %d/%m/%Y')

            # Defined data variables to be sent to Firebase.
            data = {
                'alertType': 'warningAlert',
                'alertInfo': 'lid_warning_alert',
                'alertState': warningAlert,
                'timestamp': timestamp,
                'contactName': contactName,
                'contactNumber': contactNumber
            }

            print('*! Warning Alert event sent to Realtime DB !*')
            db.reference('/').child('pillBoxData').child('boxAlerts').set(data)
            # Update the 'history' data under 'boxAccessData', with a history of pushes. 
            db.reference('/').child('pillBoxData').child('boxAlertMemory').push(data)
            '''
            ---------------------------------------------------------------------------
            '''
            break
        else: 
            print('\n All is well! No schedule is due at the moment.')
        break
        

