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
AmntOfHours = int(input("Amount of Hours: "))
AmntOfUsers = int(input("Amount of Users: "))
PhoneNum = int(input("Phone Number: "))
Hour = str(input("Send At What Start Hour [0-24]: "))
Min = str(input("Send At What Start Min [00-59]: "))
Zipcode = input("Zipcode: ")

users = []

for i in range(AmntOfUsers):
    if int(Min) >= 60:
        Min = int(Min)
        Min -= 60
        Min = str(Min)

        Hour = int(Hour)
        Hour += 1
        Hour = str(Hour)

    Min = Min.zfill(2)

    # print(f"amntOfHours: {AmntOfHours}")
    # print(f"fname: {FirstName}")
    # print(f"lname: {str(i)}")
    # print(f"number: {PhoneNum}")
    # print(f"time: {Hour}:{Min}")
    # print(f"zipcode: {Zipcode}\n\n")

    UserRef.push().set({
    "amntOfHours": AmntOfHours,
    "fname": FirstName,
    "lname": str(i),
    "number": PhoneNum,
    "time": Hour+":"+Min,
    "zipcode": Zipcode
    })

    Min = int(Min)
    Min += 5
    Min = str(Min)

    user = {"amntOfHours": AmntOfHours,"fname": FirstName,"lname": str(i),"number": PhoneNum,"time": Hour+":"+Min,"zipcode": Zipcode}
    print(f"Successfully Added {user}")