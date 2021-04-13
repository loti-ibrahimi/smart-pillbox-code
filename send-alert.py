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

def main():
    print('')
    print('============================================================')
    print('    Fetching current Alert event data from Realtime DB      ')
    print('============================================================')
    print('')
    rtdb = db.reference('pillBoxData').child('boxAlerts').get()
    twilioAlertStatus = rtdb['twilioSMSAlert']
    if twilioAlertStatus == True:
        print('* Current Twilio SMS Alert Status:', twilioAlertStatus, '\n (Sending Alert...)')

        # Sample mock data (as if fetched from main schedules DB)
        pillType = 'PillA'
        pillQuantity = 1
        '''
        <Summary Checklist> 
        * Check TwilioSMSAlert event in the realtime database
        * Trigger SMS ALert if TwilioSMSAlert = True.
        * Set the event to False once Alert is complete.

        Cost is 7c per SMS, budget is €14. Roughly 200 SMS.
        '''

        # Account SID and Token stored in my local env. variable file twilio.env
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        # Text message to be sent.
        message = client.messages.create(
            body='Schedule Pill is now Due. \n * Pill Type: '+ pillType +'\n * Quantity: '+ str(pillQuantity) +' \n Please access your Pillbox.',
            from_='+16124306181',
            # Stored in my local env. variable file twilio.env
            to=os.environ['MY_PHONE_NUMBER']
        )
        print(message.sid)

        # Default value for SMS alert event. 
        twilioAlert = False
        # Current timestamp.
        timestamp = datetime.datetime.now().strftime('Time: %H:%M:%S, Date: %d/%m/%Y')


        # Defined data variables to be sent to Firebase.
        data = {
            'twilioSMSAlert': twilioAlert,
            'timestamp': timestamp,
        }

        # Set the Twilio Alert event to False, once the SMS has been sent.
        print('*! Realtime DB Twilio SMS Alert successfully sent !*')
        db.reference('/').child('pillBoxData').child('boxAlerts').set(data)
        # Update the 'history' data under 'boxAccessData', with a history of pushes. 
        db.reference('/').child('pillBoxData').child('boxAlertMemory').push(data)
        
    else:
        print('* Current Alert Status:', twilioAlertStatus, '\n (No Alerts triggered)')
    print('')

main()

    
