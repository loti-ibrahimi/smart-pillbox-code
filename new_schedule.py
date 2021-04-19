# Firebase Admin SDK 
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/Users/lotiibrahimi/Dropbox/WIT-IOT/FYP/FYP-2021/Workspace/Code/Smart-Pillbox/firebase-sdk/thesmartpillbox-ffb73-firebase-adminsdk-q4yrs-ddd08428fc.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesmartpillbox-ffb73-default-rtdb.firebaseio.com/'
})

db = firestore.client()
docData = db.collection("pillPlan").where('boxID', '==', 'box1').stream()

for doc in docData:
    pillPlanData = doc.to_dict()

    schedules = doc.get('pillSchedules')

    scheduleData = {  
        'day': 'Monday',
        'pillCompartment': 4,
        'pillQunatity': 2,
        'pillType': 'pill_D',
        'schedule_id': 'sched4comp4qt2',
        'time': '18:30'
    }
    try: 
        schedules.set(scheduleData)
        print('New schedule successfully added. \n', scheduleData)

    except:
        print('!Failed to add new schedule to Firestore DB!')

