# #!/usr/bin/python3
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

'''
<Event Listener Summary> 
* Check pillBoxData > boxAlerts (in the realtime database) for TwilioSMSAlert events.
* Pull down the event data on any new event.
* Trigger SMS ALert if TwilioSMSAlert = True.
* Set the event to False once Alert is complete and SMS is sent.

* Enter this command before script when KeyError: 'TWILIO_ACCOUNT_SID': 
source ./twilio.env
'''


# Global Variables
# Account SID and Token stored in my local env. variable file twilio.env
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def listener(event):
    print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /reference/event.path. None if deleted

    twilioAlertStatus = event.data['twilioSMSAlert']

    if twilioAlertStatus == True:
        print('* Current Twilio SMS Alert Status:', twilioAlertStatus, '\n(Sending SMS Alert...)')
        print('')

        # Current Timestamp
        timestamp = datetime.datetime.now().strftime('Time: %H:%M, Date: %d/%m/%Y')

        # Pull out the Pill Data associated with the recent alert event from the realtime db.
        userName = event.data['username']
        pillDue = event.data['pillDue']
        quantityDue = event.data['quantityDue']

        # Text message to be sent.
        message = client.messages.create(
            body='Hey'+ userName +'! Your scheduled pill is now due - ('+ timestamp +') \n * Pill Type: '+ pillDue +'\n * Quantity: '+ str(quantityDue) +' \n Please access your Pillbox.',
            from_='+16124306181',
            # Stored in my local env. variable file twilio.env
            to=os.environ['MY_PHONE_NUMBER']
        )
        print(message.sid)
        print('>----- Alert SMS being sent -----<')
        print('Hey ', userName ,'! Your scheduled pill is now due - (', timestamp ,') \n * Pill Type: ', pillDue ,'\n * Quantity: ', quantityDue ,' \n Please access your Pillbox.')
        print('>--------------------------------<')
        
        # Message has been sent. 
        twilioAlert = False

        # Updated event data to be sent to Firebase.
        data = {
            'twilioSMSAlert': twilioAlert,
            'timestamp': timestamp,
            'alertStatus': 'Sent',
        }

        db.reference('/').child('pillBoxData').child('boxAlerts').set(data)
        # # Update the 'history' data under 'boxAccessData', with a history of pushes. 
        db.reference('/').child('pillBoxData').child('boxAlertMemory').push(data)

        # # Set the Twilio Alert event to False, once the SMS has been sent.
        print('<! Twilio SMS Alert successfully sent !>')
            
    else:
        print('* Current Alert Status:', twilioAlertStatus, '\n (No alerts detected.)')
    print('')


def main():
    print('')
    print('============================================================')
    print('    Fetching current Alert event data from Realtime DB      ')
    print('============================================================')
    print('')

    # Listen for event changes within pillBoxData > boxAlerts for new event data.
    db.reference('pillBoxData').child('boxAlerts').listen(listener)
    while True:
        time.sleep(0.1)
main()

    
