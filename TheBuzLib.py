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
    
    def get_users(self):
        db_ref = db.reference("/", app=self.app)
        
        usernames = db_ref.child("usernames").get()
        numbers = db_ref.child("numbers").get()
        times = db_ref.child("times").get()
        extensions = db_ref.child("extensions").get()

        users = []

        for name in usernames:
            new_user = {"name": usernames[name]}

            new_user["number"] = numbers[name]
            new_user["time"] = times[name]
            new_user["extensions"] = extensions[name]
            new_user["sent"] = False
                          
            users.append(new_user)
        
        return users

    def refresh_users(self):
        dbReference = db.reference("/", app=self.app)
        
        usernames = dbReference.child("usernames").get()
        numbers = dbReference.child("numbers").get()
        times = dbReference.child("times").get()
        extensions = dbReference.child("extensions").get()

        users = []

        for name in usernames:
            new_user = {"name": usernames[name]}

            new_user["number"] = numbers[name]
            new_user["time"] = times[name]
            new_user["extensions"] = extensions[name]
            new_user["sent"] = False
                          
            users.append(new_user)
        
        return users       


class Messenger:
    def __init__(self) -> None:
        self.client = Client("AC8019d9ef2f2d8295d0fd87f430a186f2", "f576251d5b238ab5458dee60e9888dbc")
    
    def send_message(self, to: str, message: str):
        self.client.messages.create(body=message, to=to, from_='+13479708748')

