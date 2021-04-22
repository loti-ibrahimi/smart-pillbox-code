# Firebase Admin SDK 
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/home/pi/Documents/Smart-Pillbox/firebase-sdk/thesmartpillbox-ffb73-firebase-adminsdk-q4yrs-ddd08428fc.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesmartpillbox-ffb73-default-rtdb.firebaseio.com/'
})

'''
<Script Overview> 
* Defining data & creating a document to be added (if document doesn't alrady exist) else update the Firestore DB.

Quick Solution for an ideal CRUD webapp interface - which I didnt get around to.

'''

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
        'pillQuantity': 2,
        'pillType': 'pill_g',
        'schedule_id': 'sched1comp4qt2',
        'time': '14:30'
    },
    {  
        'day': 'Monday',
        'pillCompartment': 2,
        'pillQuantity': 1,
        'pillType': 'pill_bw',
        'schedule_id': 'sched2comp2qt1',
        'time': '14:45'
    },
    {  
        'day': 'Monday',
        'pillCompartment': 1,
        'pillQuantity': 2,
        'pillType': 'pill_w',
        'schedule_id': 'sched3comp1qt2',
        'time': '15:30'
    },
    {  
        'day': 'Monday',
        'pillCompartment': 3,
        'pillQuantity': 3,
        'pillType': 'pill_b',
        'schedule_id': 'sched4comp3qt3',
        'time': '17:30'
    },
    ]
}

# Add a new document in collection "pillPlan" with ID 'pill_box1'
setDoc = db.collection('pillPlan').document('pillBox_1')

try: 
    setDoc.set(data)
    print('New schedule successfully added. \n', data)

except:
    print('!Failed to add new schedule to Firestore DB!')