# Firebase Admin SDK 
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/home/pi/Documents/Smart-Pillbox/firebase-sdk/thesmartpillbox-ffb73-firebase-adminsdk-q4yrs-ddd08428fc.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesmartpillbox-ffb73-default-rtdb.firebaseio.com/'
})

db = firestore.client()

data = {
    'boxID': 'pillBox_1',
    'boxName': "Loti's Pillbox",
    'userName': 'librahimi',
    'carerContacts': {
        'email': 'edoe@outlook.com',
        'name': 'Emma',
        'surname': 'Doe',
        'phone': '0854211853'
    },
    'contactDetails': {
        'email': 'loti.ibrahimi@outlook.com',
        'name': 'Loti',
        'surname': 'Ibrahimi',
        'phone': '0834616893'
    },
    'pillSchedules': [
    {  
        'day': 'Monday',
        'pillCompartment': 4,
        'pillQunatity': 2,
        'pillType': 'pill_green',
        'schedule_id': 'sched1comp4qt2',
        'time': '18:30'
    }
    ]
}

# Add a new document in collection "pillPlan" with ID 'pill_box1'
setDoc = db.collection('pillPlan').document('pillBox_1')

try: 
    setDoc.set(data)
    print('New schedule successfully added. \n', data)

except:
    print('!Failed to add new schedule to Firestore DB!')