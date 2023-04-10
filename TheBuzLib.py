import json
import firebase_admin
from firebase_admin import db
from twilio.rest import Client

class Reader:
    def __init__(self, file: str, mode: str= "Dev") -> None:
        self.contents = json.loads(open(file).read()).get(mode)
    
    def get_key(self, key: str):
        return self.contents.get(key, False)

class Database:
    def __init__(self, reader: Reader) -> None:
        self.reader = reader

        cred = firebase_admin.credentials.Certificate(self.reader.get_key("database").get("credentials"))
        self.app = firebase_admin.initialize_app(cred, options={"databaseURL": self.reader.get_key("database").get("reference_url")})
    
    def add_user(self, name: str, number: str, time: str, zipcode: str):
        dbReference = db.reference("/", app=self.app)

        usernames = dbReference.child("usernames")

        key = usernames.push(name).key

        num = dbReference.child("numbers").child(key)
        num.set(f"{number}")

        clock = dbReference.child("times").child(key)
        clock.set(f"{time}")

        extensions = dbReference.child("extensions").child(key)
        extensions.set({"Weather":zipcode})


    def get_users(self):
        dbReference = db.reference("/", app=self.app)
        
        usernames = dbReference.child("usernames").get()
        numbers = dbReference.child("numbers").get()
        times = dbReference.child("times").get()
        extensions = dbReference.child("extensions").get()

        users = []

        for name in usernames:
            newUser = {"name": usernames[name]}

            newUser["number"] = numbers[name]
            newUser["time"] = times[name]
            newUser["extensions"] = extensions[name]
            newUser["sent"] = False
                          
            users.append(newUser)
        
        return users


    def get_messages(self):
        messages = db.reference("/messages", app=self.app).get()

        allMessages = []
        for x in messages:
            allMessages.append((x, messages[x]))

        return allMessages

    def change_value(self, what):
        messages = db.reference("/messages", app=self.app).get()

        for x in messages:
            if x == what:
                old_data = messages[x]

                new_data = []
                for i in old_data:
                    if i in [True, False]:
                        i = not i

                    new_data.append(i)

                db.reference(f"/messages/{x}", app=self.app).set(new_data)



class Messenger:
    def __init__(self) -> None:
        self.client = Client("AC8019d9ef2f2d8295d0fd87f430a186f2", "f576251d5b238ab5458dee60e9888dbc")
    
    def send_message(self, to: str, message: str):
        self.client.messages.create(body=message, to=to, from_='+13479708748')

