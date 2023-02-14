import firebase_admin as firebase
from firebase_admin import credentials
from firebase_admin import db as database
import json

# Read Configuration File
mode = "Dev"
with open("Configuration.json", "r") as file:
    config = json.load(file)[mode]

with open("info.json", "r") as file:
    info = json.load(file)["Users"]

# Firebase Client Credentials
cred = credentials.Certificate(config["database"]["credentials"])

# Firebase Client Creation
connection = firebase.initialize_app(cred, name="TheBuz")
print("Initalized Database Connection")

# Firebase Client Reference
database_reference = database.reference("/", connection, config["database"]["reference_url"])

usernames_reference = database_reference.child("usernames")
phone_numbers_reference = database_reference.child("numbers")
message_times_reference = database_reference.child("times")
weathers_reference = database_reference.child("weather")

number_data = {}
message_data = {}
weather_data = {}

for user in info:
    new_user_ref = usernames_reference.push(info[user]["fname"])
    key = new_user_ref.key

    number_data[key] = "+" + str(info[user]["number"])
    message_data[key] = info[user]["time"]
    weather_data[key] = {"zipcode": info[user]["zipcode"]}

    print("Got Data ", info[user]["fname"])

phone_numbers_reference.set(number_data)
message_times_reference.set(message_data)
weathers_reference.set(weather_data)

print("Uploaded All Data")
