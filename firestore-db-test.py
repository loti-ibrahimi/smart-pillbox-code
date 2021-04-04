#!/usr/bin/python

# Import required libraries

# Firebase Admin SDK 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/pi/Documents/Smart-Pillbox/firebase-sdk/thesmartpillbox-ffb73-firebase-adminsdk-q4yrs-ddd08428fc.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


print('')
print('======================================')
print('Testing fetching data from Firestore')
print('======================================')
print('')

# Get/display all document data from the first doc of 'pillPlan' collection 
doc_ref1 = db.collection('pillPlan').document('OtejDVB9HBeYju581KAt')
data1 = doc_ref1.get()
if data1.exists:
    # f-string to display a variable within the string
    print(f'Document data [pillPlan]: {data1.to_dict()}')
    print('---------------------------------')
else:
    print('No document found')



# Get/display all document data from the first doc of 'pillPlan' collection 
doc_ref2 = db.collection('pillPlan').document('OtejDVB9HBeYju581KAt').collection('pillSchedules').document('FwPg0Ic9J4ZP64YZToLp')
data2 = doc_ref2.get()
if data2.exists:
    # f-string to display a variable within the string
    print(f'Document data [pillSchedules/pill A]: {data2.to_dict()}')
    print('---------------------------------')
    print('')
else:
    print('No document found')



print('')
print('GET/Display all Documents within the pillSchedules sub-collection')
print('=================================================================')
docsSchedules = db.collection('pillPlan').document('OtejDVB9HBeYju581KAt').collection('pillSchedules').stream()

for schedule in docsSchedules:
    print(f'{schedule.id} => {schedule.to_dict()}')


print('')
print('GET/Display data for a specific pillBox plan')
print('=================================================================')
docData1 = db.collection('pillPlan').where('boxID', '==', 'box1').stream()

for doc in docData1:
    print('{} => {}'.format(doc.id, doc.to_dict()))


print('')
print('GET/Display data for a specific pill schedule')
print('=================================================================')
docData2 = db.collection('pillPlan').document('OtejDVB9HBeYju581KAt').collection('pillSchedules').where('pillCompartment', '==', 1).stream()

for doc2 in docData2:
    print('{} => {}'.format(doc2.id, doc2.to_dict()))





