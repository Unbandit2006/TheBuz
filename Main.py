from Program import *
import configparser
import pytextnow

class MessageReader:
    def __init__(self, client: pytextnow.Client):
        self.client = client

    def get_all_messages(self):
        return self.client.get_unread_messages()
    
    def get_message_from_number(self, num:str):
        value = ""

        for message in self.get_all_messages():
            if message.number == num:
                value = message

        return value

    def correlate_with_users(self, users:list[User]):
        for user in users:
            for message in self.get_all_messages():
                if message.number == user.get_number():
                    return (user, message)
    
    def wait_for_words(self, words:dict):
        for word in words:
            for message in self.get_all_messages():
                message.pure_message = message.content.lower().strip()
                
                if message.pure_message == word:
                    words[word](message)
                
                    message.mark_as_read()
    
    def word_contains(self, words:dict):
        for word in words:
            for message in self.get_all_messages():
                message.pure_message = message.content.lower().strip()
                
                if message.pure_message.__contains__(word):
                    words[word](message)
                
                    message.mark_as_read()
    
    def on_any(self, action):
        '''
        NOTE: You have to call mark_as_read for the message
        '''
        for message in self.get_all_messages():
            message.pure_message = message.content.lower().strip()

            action(message)


            


class ConfigReader:
    def __init__(self, filename:str):
        self.filename = filename

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

config = configparser.RawConfigParser()
config.read("Config.ini")

mode = "PRODUCTION"

username = str(config.get(mode, "username"))
_sid_cookie = str(config.get(mode, "sid_cookie"))
_csrf_cookie = str(config.get(mode, "csrf_cookie"))
messenger = pytextnow.Client(username, _sid_cookie, _csrf_cookie)
messenger.auth_reset(sid_cookie=_sid_cookie, csrf_cookie=_csrf_cookie)

reader = FirebaseReader(config, mode)
message_reader = MessageReader(messenger)

# Usernames
usernames_reference = admin.db.reference("Usernames")
usernames_etag = usernames_reference.get(etag=True)[1]

old_etag = usernames_etag
users = create_user_objs(reader.get_all_usernames())
user_numbers = get_user_numbers(users)
old_users_etag = reader.get_etag()
old_time = Time()

IncomingMessageCounter = 0
OutgoingMessageCounter = 0


yes_ppl = {}

def sign_up_zipcode(message):
    if message.number in yes_ppl and yes_ppl[message.number]["name"]==True:
        yes_ppl[message.number]["name"] = message_reader.get_message_from_number(message.number).content
        messenger.send_sms(message.number, rf"Hello {yes_ppl[message.number]['name']}\nWhat is your zipcode?")
        yes_ppl[message.number]["zipcode"] = True

        message.mark_as_read()

def sign_up_time(message):
    if message.number in yes_ppl and yes_ppl[message.number]["zipcode"]==True:
        yes_ppl[message.number]["zipcode"] = message_reader.get_message_from_number(message.number).content
        messenger.send_sms(message.number, rf"What time would you like to recieve TheBuz?")
        yes_ppl[message.number]["time"] = True

        messenger.send_sms(message.number, rf"{message_reader.incoming_messages}")

        message.mark_as_read()

def sign_up_yes(message):

    if message.number in yes_ppl:
        if message.number[1:] in user_numbers.keys():
            messenger.send_sms(message.number, "You Are Already an subscriber to TheBuz")
            yes_ppl.remove(message.number)
        
        else:
            messenger.send_sms(message.number, r"Very Good! :)\nWhat is your name?")
            yes_ppl[message.number]["name"] = True

def sign_up(message):
    messenger.send_sms(message.number, "Do you want to Sign Up for TheBuz?")
    yes_ppl[message.number] = {"name":False, "zipcode":False, "time":False}

while True:
    time = Time()
    logger = Logger(time)
    logger.start()

    if time.get_day_number() == old_time.get_day_number():
        message_reader.wait_for_words({"sign up":sign_up, "yes":sign_up_yes, "yea":sign_up_yes, "yeah":sign_up_yes})
        message_reader.on_any(sign_up_zipcode)
        message_reader.on_any(sign_up_time)
        # message_reader.word_contains({"update ":update})
        # try:
        #     unread_messages = messenger.get_unread_messages()
        # except Exception as e:
        #     logger.message("None", e, "ERROR")

        # available_commands = {"update <Valid Zipcode>":"Get the most recent and up to date information of the weather.","help":"Get information about all of our commands"}
        # for unread_message in unread_messages:
        #     IncomingMessageCounter += 1

        #     if unread_message.first_contact == False:
        #         random_user_zip = user_numbers.get(unread_message.number[1:])
        #         unread_message.message = unread_message.content.lower().strip()

        #         weather_api_key = config.get(mode, "weather_api_key")
                
        #         if unread_message.message.__contains__(" ") == True:
        #             unread_message.message = unread_message.message.split(" ")

        #             if unread_message.message[0] == "update":
        #                 random_user_zip = unread_message.message[1]

        #                 try:
        #                     message = rf"Current Weather\nAt Zipcode {random_user_zip}\n---------------\n"
        #                     new_weather = Weather(weather_api_key, random_user_zip)
        #                     print(new_weather)
        #                     message += new_weather.get_current_feels_like_temp()
        #                     message += new_weather.get_data()

        #                     messenger.send_sms(unread_message.number, message)
        #                     OutgoingMessageCounter += 1
        #                     logger.message(unread_message.number[1:], message, "SUCCESS && UPDATE")

        #                 except Exception as e:
        #                     message = r"Invalid Zipcode\n\nThe number you have typed up is an invalid zipcode.\nPlease type in a valid zipcode with the 'Update' command."
        #                     messenger.send_sms(unread_message.number, message)
        #                     OutgoingMessageCounter += 1
        #                     logger.message(unread_message.number[1:], message, "ERROR && UPDATE")
                
        #         elif unread_message.message == "update":
        #             message = rf"Current Weather\n---------------\n"
        #             new_weather = Weather(weather_api_key, random_user_zip)
        #             print(new_weather)
        #             message += new_weather.get_current_feels_like_temp()
        #             message += new_weather.get_data()

        #             messenger.send_sms(unread_message.number, message)
        #             OutgoingMessageCounter += 1
        #             logger.message(unread_message.number[1:], message, "SUCCESS && UPDATE")

        #         elif unread_message.message == "help" or unread_message.message == "?":
        #             message = rf""
        #             for x in available_commands:
        #                 message += rf"{x.capitalize()} - {available_commands[x]}\n"

        #             messenger.send_sms(unread_message.number[1:], message)
        #             OutgoingMessageCounter += 1
        #             logger.message(unread_message.number[1:], message, "SUCCESS && HELP")
                
        #         elif unread_message.message == "messages":
        #             OutgoingMessageCounter += 1
        #             messenger.send_sms(unread_message.number[1:], fr"Outgoing Messages: {OutgoingMessageCounter}\nIncoming Messages: {IncomingMessageCounter}")
        #             logger.message(unread_message.number[1:], fr"Outgoing Messages: {OutgoingMessageCounter}\nIncoming Messages: {IncomingMessageCounter}", "SUCCESS && MESSAGES")

        #         else:
        #             message = rf"Unknown Command\nPlease type one of the following for their respective actions:\n\n"
        #             for x in available_commands:
        #                 message += rf"{x.capitalize()} - {available_commands[x]}\n"
                    
        #             messenger.send_sms(unread_message.number[1:], message)
        #             OutgoingMessageCounter += 1
        #             logger.message(unread_message.number[1:], message, "UNKNOWN COMMAND")
                    
        #     unread_message.mark_as_read()

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
                message = user.create_message(config.get(mode, "weather_api_key"))
                message += r"Type 'help' or '?' to get information about all of our commands"
                try:
                    messenger.send_sms(user.get_number(), message)
                    OutgoingMessageCounter += 1
                except Exception as e:
                    logger.message(user.get_number(), e, "ERROR")

                logger.message(user.get_number(), message, "SENT")

    else:
        old_time = Time()
        users = create_user_objs(reader.get_all_usernames())
        user_numbers = get_user_numbers(users)
        old_users_etag = reader.get_etag()        
