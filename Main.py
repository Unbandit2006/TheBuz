from Program import *
import configparser
import pytextnow


def create_user_objs(usernames: list) -> list[User]:
    user_objs = []

    for user in usernames:
        user_objs.append(User(reader.get_value(user)))
    
    return user_objs

def get_user_numbers(users:list):
    user_nums = {}
    
    for user in users:
        user_nums[user.get_number()] = user.get_zipcode()

    return user_nums

def log(string:str, log_file:str=".log"):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(string)

def log_error(string:str, log_file:str=".log"):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"ERROR: {string}")

config = configparser.RawConfigParser()
config.read("Config.ini")

mode = "HOME"

username = str(config.get("CONSTANTS", "username"))
_sid_cookie = str(config.get("CONSTANTS", "sid_cookie"))
_csrf_cookie = str(config.get("CONSTANTS", "csrf_cookie"))
messenger = pytextnow.Client(username, _sid_cookie, _csrf_cookie)
messenger.auth_reset(sid_cookie=_sid_cookie, csrf_cookie=_csrf_cookie)

reader = FirebaseReader(config, mode)

# Usernames
usernames_reference = admin.db.reference("Usernames")
usernames_etag = usernames_reference.get(etag=True)[1]

old_etag = usernames_etag
users = create_user_objs(reader.get_all_usernames())
user_numbers = get_user_numbers(users)
old_users_etag = reader.get_etag()

while True:
    time = Time()

    try:
        unread_messages = messenger.get_unread_messages()
    except Exception as e:
        print(e)
        log_error(e)

    for unread_message in unread_messages:
        if unread_message.first_contact == False:
            random_user_zip = user_numbers.get(unread_message.number[1:])

            if unread_message.content.lower().strip() == "update":
                weather_api_key = config.get("CONSTANTS", "weather_api_key")

                message = rf"Current Weather\n---------------"
                new_weather = Weather(weather_api_key, random_user_zip)
                message += new_weather.get_data()

                messenger.send_sms(unread_message.number, message)
                print(f"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nSent to {unread_message.number[1:]}\nMessage: '{message}'\nUPDATE\n")
                log(f"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nSent to {unread_message.number[1:]}\nMessage: '{message}'\nUPDATE\n")
        
        unread_message.mark_as_read()

    if reader.get_if_changed(old_users_etag)[0] == True and usernames_reference.get_if_changed(old_etag)[0] == False:
        users = create_user_objs(reader.get_all_usernames())
        user_numbers = get_user_numbers(users)
        old_users_etag = reader.get_etag()

    if usernames_reference.get_if_changed(old_etag)[0] == True:
        users = create_user_objs(reader.get_all_usernames())
        user_numbers = get_user_numbers(users)
        old_etag = usernames_reference.get(etag=True)[1]
    
    for user in users: 
        if user.get_run() == False and time.get_hour() == user.get_hour() and time.get_minutes() == user.get_minutes():
            message = user.create_message(config.get("CONSTANTS", "weather_api_key"))
            messenger.send_sms(user.get_number(), message)
            print(f"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nSent to {user.get_name()}\nMessage: '{user.get_message()}'\n\n")
            log(f"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nSent to {user.get_name()}\nMessage: '{user.get_message()}'\n\n")


