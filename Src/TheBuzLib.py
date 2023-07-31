import json
import firebase_admin
from firebase_admin import db
import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, format_datetime
import datetime


class Reader:
    def __init__(self, file: str, mode: str = "Dev") -> None:
        self.contents = json.loads(open(file).read()).get(mode)

    def get_key(self, key: str):
        return self.contents.get(key, False)


class Database:
    def __init__(self, reader: Reader) -> None:
        self.reader = reader

        cred = firebase_admin.credentials.Certificate(self.reader.get_key("database").get("credentials"))
        self.app = firebase_admin.initialize_app(cred, options={
            "databaseURL": self.reader.get_key("database").get("reference_url")})

    def add_user(self, name: str, number: str, time: str, zipcode: str):
        dbReference = db.reference("/", app=self.app)

        usernames = dbReference.child("usernames")

        key = usernames.push(name).key

        num = dbReference.child("numbers").child(key)
        num.set(f"{number}")

        clock = dbReference.child("times").child(key)
        clock.set(f"{time}")

        extensions = dbReference.child("extensions").child(key)
        extensions.set({"Weather": zipcode})

        carriers = dbReference.child("carriers").child(key)
        carriers.set(f"cool") # TODO CHANGE THIS SO THAT IT HAS PRORPER

    def get_users(self):
        dbReference = db.reference("/", app=self.app)

        usernames = dbReference.child("usernames").get()
        numbers = dbReference.child("numbers").get()
        times = dbReference.child("times").get()
        extensions = dbReference.child("extensions").get()
        carrier = dbReference.child("carriers").get()

        users = []

        for name in usernames:
            newUser = {"name": usernames[name], "number": numbers[name], "time": times[name],
                       "extensions": extensions[name], "sent": False, "carrier": carrier[name]}

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

    def find_user(self, search_term: int | str):
        usernames = db.reference("/usernames", app=self.app).get()
        numbers = db.reference("/numbers", app=self.app).get()

        if type(search_term) == int:
            for x in numbers:
                if numbers[x] == search_term:
                    times = db.reference("times").get()
                    extensions = db.reference("extensions").get()
                    carriers = db.reference("carriers").get()

                    newUser = {"name": usernames[x]}
                    newUser["number"] = numbers[x]
                    newUser["time"] = times[x]
                    newUser["extensions"] = extensions[x]
                    newUser["sent"] = False
                    newUser["carrier"] = carriers[x]

                    return newUser
                
        elif type(search_term) == str:
            usernames = db.reference("/usernames", app=self.app).get()

            for x in usernames:
                if usernames[x] == search_term:
                    times = db.reference("times").get()
                    extensions = db.reference("extensions").get()
                    carriers = db.reference("carriers").get()

                    newUser = {"name": usernames[x]}
                    newUser["number"] = numbers[x]
                    newUser["time"] = times[x]
                    newUser["extensions"] = extensions[x]
                    newUser["sent"] = False
                    newUser["carrier"] = carriers[x]

                    return newUser
                
    def remove_user(self, search_term: str):
        usernames = db.reference("/usernames", app=self.app).get()

        for x in usernames:
            if usernames[x] == search_term:
                db.reference(f"/usernames/{x}").delete()
                db.reference(f"/times/{x}").delete()
                db.reference(f"/numbers/{x}").delete()
                db.reference(f"/extensions/{x}").delete()
                db.reference(f"/carriers/{x}").delete()

    def get_zipcode_stats(self):
        zipcodes = {}
        usernames = db.reference("/usernames", app=self.app).get()

        for x in usernames:
            zipcode = db.reference(f"/extensions/{x}/Weather").get()
            if zipcode in zipcodes.keys():
                zipcodes[zipcode] += 1
            else:
                zipcodes[zipcode] = 1

        return zipcodes

    def get_service_stats(self):
        services = {}
        usernames = db.reference("/usernames", app=self.app).get()

        for x in usernames:
            service = db.reference(f"/extensions/{x}/Weather").get()
            if service in services.keys():
                services[service] += 1
            else:
                services[service] = 1

        return services       


class Messenger:
    def __init__(self) -> None:
        # self.client = Client("AC8019d9ef2f2d8295d0fd87f430a186f2", "f576251d5b238ab5458dee60e9888dbc")
        pass

    def send_message(self, to: str, message: str):
        self.client = smtp.SMTP("smtp.gmail.com", 587)
        self.client.starttls()
        self.client.ehlo()
        self.client.login("JohnCrichton.Mars@gmail.com", "kjzjxjkorqnzbrmc")

        self.email = MIMEMultipart("alternative")
        self.email["Date"] = format_datetime(datetime.datetime.now())
        self.email["Message-ID"] = make_msgid()
        self.email["Subject"] = "Daily Info"
        self.email["From"] = "TheBuz <JohnCrichton.Mars@gmail.com>"

        # self.client.messages.create(body=message, to=to, from_='+13479708748')
        self.email["To"] = to

        body = MIMEText(message, "html", "UTF-8")
        self.email.attach(body)

        self.client.sendmail("JohnCrichton.Mars@gmail.com", to, self.email.as_string())