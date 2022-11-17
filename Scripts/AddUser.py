import firebase_admin as admin
from firebase_admin import db
from firebase_admin import firestore

'''
This Program is internal use only.
'''

# Connect to Firebase
DATABASE_URL = "https://beeper5252022-default-rtdb.firebaseio.com/"

credentials = admin.credentials.Certificate("./beeper5252022-firebase-adminsdk-te6kd-2022802ce3.json")
admin.initialize_app(credentials, {"databaseURL": DATABASE_URL})

user_ref = db.reference('Users')
username_ref = db.reference("Usernames")

# Make a new user
first_name = str(input("First Name: "))
last_name = str(input("Last Name: "))
phone_num = int(input("Phone Number: "))
hour = str(input("Send At What Hour [0-24]: "))
minutes = str(input("Send At What Min [00-59]: "))
zipcode = str(input("Zipcode: "))

actual_user = user_ref.push()
actual_user.set({
"fname": first_name,
"lname": last_name,
"number": phone_num,
"time": hour+":"+minutes,
"zipcode": zipcode,
"weather":True
})

username_ref.update({len(username_ref.get()):actual_user.key})
