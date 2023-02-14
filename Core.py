import pytextnow as ptn
import json
import firebase_admin as firebase
from firebase_admin import credentials
from firebase_admin import db as database
import Athena
import Scripts
import time

# Read Configuration File
mode = "Dev"
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

current_time = time.localtime()
formatted_time = f"{current_time.tm_hour}:{current_time.tm_min}"

for user in users.get_users():

    # if formatted_time == user.message_time:
    message = Scripts.Weather(user).create_message()
    Scripts.News(user).add_message()
    print(user.message)
