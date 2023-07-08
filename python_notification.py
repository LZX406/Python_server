## Install request module by running ->
#  pip3 install requests

# Replace the deviceToken key with the device Token for which you want to send push notification.
# Replace serverToken key with your serverKey from Firebase Console

# Run script by ->
# python3 fcm_python.py


import time
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('task-management-43840-firebase-adminsdk-fjzn0-d9602fbede.json')
serverToken = 'AAAAnBUXl8U:APA91bHPRYEDM3oNshlJjjS7qcnvEY5ttO-d2cQa-0OhzjaBT6Pw4eT8c4r0K73GFuzRMupJJ7-baBc2YQUzT9vRlu1E9GIPli9USP1evF3rnYsBnNXbZtXKU8qTfNnVN74zp2D6H4KT'
app = firebase_admin.initialize_app(cred)

db = firestore.client()

notification_ref = db.collection(u'Notification')

starttime = time.time()
while True:
    docs = notification_ref.stream()
    for doc in docs:
        title=str(doc.to_dict()['title'])
        body=str(doc.to_dict()['body'])
        user_id=str(doc.to_dict()['user_id'])
        user_ref = db.collection(u'User').document(user_id)
        user = user_ref.get()
        doc_id=doc.id
        if user.exists:
            deviceToken=str(user.to_dict()['token'])
            if deviceToken!='None':
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                  }
                body = {
                      'notification': {'title': title,
                                        'body': body
                                        },
                      'to':
                          deviceToken,
                      'priority': 'high',
                    #   'data': dataPayLoad,
                    }
                response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
                print(response.status_code)
                print(response.json())
                if response.json()['success']==1:
                    print("send success")
                    db.collection(u'Notification').document(doc_id).delete()
    time.sleep(1.0 )









#deviceToken = 'fofSS6sxSYaDeUkrCPuuVj:APA91bGzwU-o6nG4P4Rc_24UtJ4fW4nregm6VCrFIV6GDqX3ncnEpmdiq8WnmiquScLPxQD37-tQ79xCb1hAe7FCdcVp8dZSghDlBVwPfkm2QMuaN3fCrtChJAdO5GP1UUlD1fDSlgWA'



