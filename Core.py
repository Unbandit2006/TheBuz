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

# Logger
chronos_log = Athena.Logger()
chronos_log.start_logger()

# PyTextNow Client Creation
apollo = ptn.Client(config["user"]["name"], config["user"]["sid_cookie"], config["user"]["csrf_cookie"])
chronos_log.add_message("Initialized Client", "Initialization")

# Firebase Client Credentials
cred = credentials.Certificate(config["database"]["credentials"])

# Firebase Client Creation
connection = firebase.initialize_app(cred, name="TheBuz")
chronos_log.add_message("Initialized Database Connection", "Initialization")

# Firebase Client Reference
database_reference = database.reference("/", connection, config["database"]["reference_url"])

users = Athena.UserList(apollo, database_reference)
users.make_user_list()
chronos_log.add_message("Initialized User List", "Initialization")


# Read Message
def hello(info):
    person = users.search(info["number"])

    try:
        apollo.send_sms(info["number"], rf"Hello {person.name}\nI hope you are having a good day. :)")
    except Exception as e:
        chronos_log.add_message(str(e), "Error")


def refresh(info):
    person = users.search(info["number"])

    if info["message"] == "refresh weather":
        Scripts.Weather(person).create_message()
        try:
            apollo.send_sms(person.phone_number, person.message)
            chronos_log.add_message(f"Send weather to {person.name}", "Sent")
        except Exception as e:
            chronos_log.add_message(str(e), "Error")

    elif info["message"] == "refresh news":
        Scripts.News(person).create_message()
        try:
            apollo.send_sms(person.phone_number, person.message)
            chronos_log.add_message(f"Sent news to {person.name}", "Sent")
        except Exception as e:
            chronos_log.add_message(str(e), "Error")

    else:
        Scripts.Weather(person).create_message()
        # Scripts.News(person).add_message()
        try:
            apollo.send_sms(person.phone_number, person.message)
            chronos_log.add_message(f"Sent refresher to {person.name}", "Sent")
        except Exception as e:
            chronos_log.add_message(str(e), "Error")


reader = Athena.MessageReader(apollo, chronos_log)

reader.add_message("hello", hello)
# reader.add_message("refresh news", refresh)
reader.add_message("refresh weather", refresh)
reader.add_message("refresh", refresh)

chronos_log.add_message("Initialized Message Reader", "Initialization")

start_time = time.localtime()
running = True
while running:
    chronos_log.start_logger()

    try:
        apollo.auth_reset(config["user"]["sid_cookie"], config["user"]["csrf_cookie"])
    except Exception as e:
        chronos_log.add_message(str(e), "Error")

    current_time = time.localtime()

    if current_time.tm_mday != start_time.tm_mday:
        users.make_user_list()
        start_time = time.localtime()
        chronos_log.add_message("Refreshed User List", "Refreshed")

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
                    chronos_log.add_message(f"Sent to {user}", "Sent")
                except Exception as e:
                    chronos_log.add_message(str(e), "Error")

                user.sent = True
                try:
                    apollo.auth_reset(config["user"]["sid_cookie"], config["user"]["csrf_cookie"])
                except Exception as e:
                    chronos_log.add_message(str(e), "Error")
                chronos_log.add_message("Apollo has be refreshed", "Refreshed")

    # Read Message
    reader.read_messages()
