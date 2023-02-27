import pytextnow as ptn
import json
import firebase_admin as firebase
from firebase_admin import credentials
from firebase_admin import db as database
import Athena
import Scripts
import time

# Read Configuration File
mode = "Production"
with open("Configuration.json", "r") as file:
    config = json.load(file)[mode]

# PyTextNow Client Creation
apollo = ptn.Client(config["user"]["name"], config["user"]["sid_cookie"], config["user"]["csrf_cookie"])
print("Initalized Client")

# Firebase Client Credentials
cred = credentials.Certificate(config["database"]["credentials"])

# Firebase Client Creation
connection = firebase.initialize_app(cred, name="TheBuz")
print("Initalized Database Connection")

# Firebase Client Reference
database_reference = database.reference("/", connection, config["database"]["reference_url"])

users = Athena.UserList(apollo, database_reference)
users.make_user_list()
print("Made User List")


# Read Message
def hello(info):
    person = users.search(info["number"])

    try:
        apollo.send_sms(info["number"], rf"Hello {person.name}\nI hope you are having a good day. :)")
    except Exception as e:
        print(str(e) + " Error")


def refresh(info):
    person = users.search(info["number"])

    if info["message"] == "refresh weather":
        Scripts.Weather(person).create_message()
        try:
            apollo.send_sms(person.phone_number, person.message)
            print(f"Sent weather to {person.name}")
        except Exception as e:
            print(str(e) + " Error")

    elif info["message"] == "refresh news":
        Scripts.News(person).create_message()
        try:
            apollo.send_sms(person.phone_number, person.message)
            print(f"Sent news to {person.name}")
        except Exception as e:
            print(str(e) + " Error")

    else:
        Scripts.Weather(person).create_message()
        Scripts.News(person).add_message()
        try:
            apollo.send_sms(person.phone_number, person.message)
            print(f"Sent refresher to {person.name}")
        except Exception as e:
            print(str(e) + " Error")


reader = Athena.MessageReader(apollo)

reader.add_message("hello", hello)
reader.add_message("refresh news", refresh)
reader.add_message("refresh weather", refresh)
reader.add_message("refresh", refresh)

print("Made Message Reader")

start_time = time.localtime()
running = True
while running:
    try:
        apollo.auth_reset(config["user"]["sid_cookie"], config["user"]["csrf_cookie"])
    except Exception as e:
        print(str(e) + " Error")

    current_time = time.localtime()

    if current_time.tm_mday != start_time.tm_mday:
        users.make_user_list()
        start_time = time.localtime()
        print("Refreshed User List")

    if current_time.tm_hour <= 12:
        hour = "0" + str(current_time.tm_hour)
    else:
        hour = current_time.tm_hour

    if current_time.tm_min < 10:
        minutes = "0" + str(current_time.tm_min)
    else:
        minutes = current_time.tm_min

    formatted_time = f"{hour}:{minutes}"

    # Send Message
    for user in users.get_users():

        if formatted_time == user.message_time:
            message = Scripts.Weather(user).create_message()
            Scripts.News(user).add_message()

            if not user.sent:
                try:
                    apollo.send_sms(user.phone_number, user.message)
                    print(f"Sent {user}")
                except Exception as e:
                    print(str(e) + " Error")

                user.sent = True
                try:
                    apollo.auth_reset(config["user"]["sid_cookie"], config["user"]["csrf_cookie"])
                except Exception as e:
                    print(str(e) + " Error")
                print("Apollo has been reset")

    # Read Message
    reader.read_messages()
