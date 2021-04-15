#!/usr/bin/python

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
print('============================================================')
print('          Fetching current event data from Realtime DB      ')
print('============================================================')
print('')
rtdb = db.reference('pillBoxData').child('boxSensors').get()
currentBoxLidStatus = rtdb['boxLidStatus']
if currentBoxLidStatus == 1:
    print('* Current BOX LID Status:', currentBoxLidStatus, '(Closed)')
else:
    print('* Current BOX LID Status:', currentBoxLidStatus, '(Open)')
print('')

print('')
print('')
print('============================================================')
print('                Fetching data from Firestore')
print('============================================================')
print('')
# Pill Plan for Box 1
docData = dbfirestore.collection('pillPlan').where('boxID', '==', 'box1').stream()

for doc in docData:
    pillPlanData = doc.to_dict()
    # test = doc.whereField('schedule', isEqualTo, 'S1')
    print('{} => {}'.format(doc.id, doc.to_dict()))
    print('+------------------------------------+')
    print('NEW', pillPlanData)
    print('<=================================================================>')
    schedules = doc.get('pillSchedules')
    for schedule in schedules:
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

        # Default value for SMS alert event
        twilioAlert = False

        # Display all data that was chosen from the Database for schedule analysis
        print('')
        print('Schedule preview          ==> ', schedule)
        print('+--------------------------------------------------------------------+')
        print('Current-Day               ==> ', currentDay)
        print('Pill-Time | In Minutes    ==> ', pillTime,' | ', pillTimeInMinutes)
        print('Current-Time | In Minutes ==> ', currentTime,' | ', currentTimeMinutes)
        print('+--------------------------------------------------------------------+')
        # # Loop check the different conditions/events.
        while True: 
            # If the current time is within 5 minutes of the scheduled time kick off 
            if abs(pillTimeInMinutes-currentTimeMinutes)<=1 and pillDay == currentDay:
                # Alert Event triggered - RTDB TwilioSMS alert updated to True.
                twilioAlert = True
                timestamp = datetime.datetime.now().strftime('Time: %H:%M:%S, Date: %d/%m/%Y')

                # Defined data variables to be sent to Firebase.
                data = {
                    'twilioSMSAlert': twilioAlert,
                    'timestamp': timestamp,
                    'pillDue': pillType,
                    'quantityDue': pillQuantity,
                }

                print('*! Realtime DB Alert event set to trigger Twilio SMS notification !*')
                db.reference('/').child('pillBoxData').child('boxAlerts').set(data)
                # Update the 'history' data under 'boxAccessData', with a history of pushes. 
                db.reference('/').child('pillBoxData').child('boxAlertMemory').push(data)
                
                print('')
                print('A scheduled pill is now due!')
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
                print('A scheduled pill is now due!')
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
            else:
                print('The next schedule is not due for another while')
                break

