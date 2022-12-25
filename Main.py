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

def log(message:str, number:str, custom_message:str, log_file:str=".log"):
    time = Time()
    with open(log_file, "a", encoding="utf-8") as file:
        dmessage = rf"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nSent to {number}\nMessage: '{message}'\n{custom_message}\n"
        dmessage_print = f"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nSent to {number}\nMessage: '{message}'\n{custom_message}\n"
        file.write(dmessage)
        print(dmessage)

def log_error(message:str, log_file:str=".log"):
    time = Time()
    with open(log_file, "a", encoding="utf-8") as file:
        dmessage = rf"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nError Message: {message}\nERROR\n"
        dmessage_print = f"At [{time.get_hour()}:{time.get_minutes()}] [{time.get_month_number()}/{time.get_day_number()}/{time.get_year()}]\nError Message: {message}\nERROR\n"
        file.write(dmessage)
        print(dmessage_print)

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
old_time = Time()

while True:
    time = Time()

    if time.get_day_number() == old_time.get_day_number():
        try:
            unread_messages = messenger.get_unread_messages()
        except Exception as e:
            log_error(e)

        available_commands = {"update <Valid Zipcode>":"Get the most recent and up to date information of the weather.","help":"Get information about all of our commands"}
        for unread_message in unread_messages:
            if unread_message.first_contact == False:
                random_user_zip = user_numbers.get(unread_message.number[1:])
                unread_message.message = unread_message.content.lower().strip()

                weather_api_key = config.get("CONSTANTS", "weather_api_key")
                
                if unread_message.message.__contains__(" ") == True:
                    unread_message.message = unread_message.message.split(" ")

                    if unread_message.message[0] == "update":
                        random_user_zip = unread_message.message[1]

                        try:
                            message = rf"Current Weather\nAt Zipcode {random_user_zip}\n---------------\n"
                            new_weather = Weather(weather_api_key, random_user_zip)
                            message += new_weather.get_current_feels_like_temp()
                            message += new_weather.get_data()

                            messenger.send_sms(unread_message.number, message)
                            log(message, unread_message.number[1:], "UPDATE")

                        except Exception as e:
                            message = r"Invalid Zipcode\n\nThe number you have typed up is an invalid zipcode.\nPlease type in a valid zipcode with the 'Update' command."
                            messenger.send_sms(unread_message.number, message)
                            log(message, unread_message.number[1:], "UPDATE_ERROR")
                
                elif unread_message.message == "update":
                    message = rf"Current Weather\n---------------\n"
                    new_weather = Weather(weather_api_key, random_user_zip)
                    message += new_weather.get_current_feels_like_temp()
                    message += new_weather.get_data()

                    messenger.send_sms(unread_message.number, message)
                    log(message, unread_message.number[1:], "UPDATE")

                elif unread_message.message == "help" or unread_message.message == "?":
                    message = rf""
                    for x in available_commands:
                        message += rf"{x.capitalize()} - {available_commands[x]}\n"

                    messenger.send_sms(unread_message.number[1:], message)
                    log(message, unread_message.number[1:], "HELP")

                else:
                    message = rf"Unknown Command\nPlease type one of the following for their respective actions:\n\n"
                    for x in available_commands:
                        message += rf"{x.capitalize()} - {available_commands[x]}\n"
                    
                    messenger.send_sms(unread_message.number[1:], message)
                    log(message, unread_message.number[1:], "UNKNOWN COMMAND")
                    
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
            user_days = user.get_days()
            if time.get_day_name() in user_days:
                if user.get_run() == False and time.get_hour() == user.get_hour() and time.get_minutes() == user.get_minutes():
                    message = user.create_message(config.get("CONSTANTS", "weather_api_key"))
                    message += r"Type 'help' or '?' to get information about all of our commands"
                    try:
                        messenger.send_sms(user.get_number(), message)
                    except Exception as e:
                        log_error(e)

                    log(message, user.get_number(), "SENT")

    else:
        old_time = Time()
        users = create_user_objs(reader.get_all_usernames())
        user_numbers = get_user_numbers(users)
        old_users_etag = reader.get_etag()        
