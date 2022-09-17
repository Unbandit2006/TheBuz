import firebase_admin as admin
from firebase_admin import db

'''
This Program is internal use only.
'''

# Connect to Firebase
DATABASE_URL = "https://beeper5252022-default-rtdb.firebaseio.com/"

Credentials = admin.credentials.Certificate("beeper5252022-firebase-adminsdk-te6kd-a403e68aff.json")
admin.initialize_app(Credentials, {"databaseURL": DATABASE_URL})

UserRef = db.reference('Users')

# Make a new user
FirstName = str(input("First Name: "))
LastName = str(input("Last Name: "))
AmntOfHours = int(input("Amount of Hours: "))
PhoneNum = int(input("Phone Number: "))
Hour = str(input("Send At What Hour [0-24]: "))
Min = str(input("Send At What Min [00-59]: "))
Zipcode = int(input("Zipcode: "))

UserRef.push().set({
    "amntOfHours": AmntOfHours,
    "fname": FirstName,
    "lname": LastName,
    "number": PhoneNum,
    "time": Hour+":"+Min,
    "zipcode": Zipcode
})
