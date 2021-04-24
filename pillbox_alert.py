# #!/usr/bin/python3

'''
Author: Loti Ibrahimi (20015453)
Course: BSc (Hons) in the Internet of Things.

Event Listener Overview:
* Check pillBoxData > boxAlerts (in the realtime database) for: 
- alertState:  True / False (True = trigger SMS alert)
- alertType: scheduleAlert / warningAlert (schedule alert notification / warning alert if pillbox opened outside of scheduled times.)

1. Pull down new event data from RTDB (pillBoxData > boxAlerts)
2. Carry out the respective SMS alerts depending on specific event data fields (alertState & alertType).
3. Set the event field 'alertState' to False once an alert is complete i.e. SMS is sent.
(This is done to prevent events triggering SMS alerts again on system reboots/script re-run.)
4. If no new events are detected, keep listening.

* Enter this command before script if KeyError: 'TWILIO_ACCOUNT_SID': 
source ./twilio.env

Normally will need to specify this on a new reboot.
'''

import os
from twilio.rest import Client
import time, datetime

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

# Global Variables
# Account SID and Token stored in my local env. variable file twilio.env
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def listener(event):
    # print(event.event_type)  # can be 'put' or 'patch'
    # print(event.path)  # relative to the reference
    # print(event.data)  # new data at /reference/event.path. None if deleted.

    # Alert event types to look out for:
    alertState = event.data['alertState'] # True / False
    alertType = event.data['alertType'] # scheduleAlert / warningAlert

    if alertState == True and alertType == 'scheduleAlert':
        print('* Twilio [Schedule SMS Alert] Status:', alertState, '\n(Sending SMS Alert...)')
        print('')

        # Current Timestamp
        timestamp = datetime.datetime.now().strftime('Time: %H:%M, Date: %d/%m/%Y')

        # Pull out the fixed data associated with the recent alert event from the realtime db.
        pillDue = event.data['pillDue']
        quantityDue = event.data['quantityDue']
        contactName = event.data['contactName']
        contactNumber = event.data['contactNumber']
        
        # Text message to be sent.
        message = client.messages.create(
            body='Hey '+ contactName +'! Your scheduled pill is now due - ('+ timestamp +') \n * Pill Type: '+ pillDue +'\n * Quantity: '+ str(quantityDue) +' \n Please access your Pillbox.',
            from_='+16124306181',
            # Retrieving the number from the event itself.
            to=contactNumber
            # Stored in my local env. variable file twilio.env
            # to=os.environ['MY_PHONE_NUMBER']
        )
        print(message.sid)

        print('>-------------------- Alert SMS being sent --------------------<')
        print('Hey ', contactName ,'! Your scheduled pill is now due - (', timestamp ,') \n * Pill Type: ', pillDue ,'\n * Quantity: ', quantityDue ,' \n Please access your Pillbox.')
        print('>--------------------------------------------------------------<')
        
        # Schedule Alert SMS has been sent. 
        scheduleAlert = False

        # Updated event data to be sent to Firebase.
        # - alertState set to False.
        data = {
            'alertType': 'scheduleAlert',
            'alertInfo': 'schedule_due',
            'alertState': scheduleAlert,
            'timestamp': timestamp,
            'pillDue': pillDue,
            'quantityDue': quantityDue,
            'contactName': contactName,
            'contactNumber': contactNumber
        }

        db.reference('/').child('pillBoxData').child('boxAlerts').set(data)
        # # Update the 'history' data under 'boxAccessData', with a history of pushes. 
        db.reference('/').child('pillBoxData').child('boxAlertMemory').push(data)

        # # Set the Twilio Alert event to False, once the SMS has been sent.
        print('<! Notification Alert SMS successfully sent !>')

    elif alertState == True and alertType == 'warningAlert':
        print('* Twilio [Warning SMS Alert] Status:', alertState, '\n(Sending SMS Alert...)')
        print('')

        # Current Timestamp
        timestamp = datetime.datetime.now().strftime('Time: %H:%M, Date: %d/%m/%Y')

        # Pull out the fixed data associated with the recent warning alert event from the realtime db.
        alertInfo = event.data['alertInfo']
        contactName = event.data['contactName']
        contactNumber = event.data['contactNumber']

        # Text message to be sent.
        message = client.messages.create(
            body='Hey '+ contactName +'! Your pillbox was opened outside of scheduled times! - ('+ timestamp +') \n * Alert info : '+ alertInfo +' \n Please check your Pillbox.',
            from_='+16124306181',
            # Retrieving the number from the event itself.
            to=contactNumber
            # Stored in my local env. variable file twilio.env 
            # to=os.environ['MY_PHONE_NUMBER']
        )
        print(message.sid)

        print('>-------------------- Alert SMS being sent --------------------<')
        print('Hey ', contactName ,'! Your pillbox was opened outside of scheduled times! - (', timestamp ,') \n * Alert info : ', alertInfo ,' \n Please check your Pillbox.')
        print('>--------------------------------------------------------------<')
        
        # Warning SMS has been sent. 
        warningAlert = False

        # Event data to be sent back to Firebase with only two updates:
        # - alertState updated to False.
        data = {
            'alertType': 'warningAlert',
            'alertInfo': 'lid_warning_alert',
            'alertState': warningAlert,
            'timestamp': timestamp,
            'contactName': contactName,
            'contactNumber': contactNumber
        }

        db.reference('/').child('pillBoxData').child('boxAlerts').set(data)
        # # Update the 'history' data under 'boxAccessData', with a history of pushes. 
        db.reference('/').child('pillBoxData').child('boxAlertMemory').push(data)

        # # Set the Twilio Alert event to False, once the SMS has been sent.
        print('\n <! Notification Alert SMS successfully sent !>')
     
            
    else:
        print('\n + Current Alert State:', alertState ,'\n (No alert request detected) +')
    print('')


def main():
    print('')
    print('===============================================================')
    print('    Actively Monitoring Alert event data from Realtime DB      ')
    print('===============================================================')
    print('\n [CTRL + C (x2) to quit]')
    print('')

    # Listen for event changes within pillBoxData > boxAlerts for new event data.
    db.reference('pillBoxData').child('boxAlerts').listen(listener)
    try:
        while True:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            print('System active check', timestamp)
            time.sleep(60)
    except:
        time.sleep(2)
        print('  Done')

main()

    
