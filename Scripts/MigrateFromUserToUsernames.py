import firebase_admin as admin
from firebase_admin import db

'''
This Program is internal use only.
'''

# Connect to Firebase
DATABASE_URL = "https://beeper5252022-default-rtdb.firebaseio.com/"

credentials = admin.credentials.Certificate("./beeper5252022-firebase-adminsdk-te6kd-2022802ce3.json")
admin.initialize_app(credentials, {"databaseURL": DATABASE_URL})

user_ref = db.reference('Users')
username_ref = db.reference("Usernames")

users = []
for i in user_ref.get():
    users.append(i)
    print(i)

username_ref.set(users)