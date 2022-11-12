import Program
import configparser
import firebase_admin as admin
from firebase_admin import db
import pytextnow

class User:
    def __init__(self, user_info:dict):
        self.__user = user_info
        self.__message = ""

    def get_name(self):
        return self.__user.get("fname"), self.__user.get("lname")
    
    def get_number(self):
        return str(self.__user.get("number"))
    
    def get_message(self):
        return self.__message
    
    def create_message(self, weather_api_key:str):
        self.__user.get("time")
        time = Program.Time()
        
        user_time = self.__user.get("time").split(":")

        if user_time[0] == time.get_hour() and user_time[1] == time.get_minutes():
            self.__message += rf"Today is {time.get_day_name()}, {time.get_month_name()} {time.get_day_number()}, {time.get_year()}.\n"
            
            if self.__user.get("weather", False):
                weather = Program.Weather(weather_api_key, self.__user.get("zipcode"))
                self.__message += weather.get_data()

            return self.__message

class FirebaseReader:
    def __init__(self, config, mode):
        default_cred = config.get(mode, "cred_file_location")
        cert = admin.credentials.Certificate(default_cred)
        admin.initialize_app(cert, options={"databaseURL":"https://beeper5252022-default-rtdb.firebaseio.com/"})
        self.__db_ref = admin.db.reference("Users")

    def get_all_usernames(self):
        usernames = []
        for user in self.__db_ref.get():
            usernames.append(user)
        
        return usernames
    
    def get_value(self, key):
        return self.__db_ref.child(key).get()        



config = configparser.RawConfigParser()
config.read("Config.ini")

mode = "HOME"

username = str(config.get("CONSTANTS", "username"))
_sid_cookie = str(config.get("CONSTANTS", "sid_cookie"))
_csrf_cookie = str(config.get("CONSTANTS", "csrf_cookie"))
messenger = pytextnow.Client(username, _sid_cookie, _csrf_cookie)
messenger.auth_reset(sid_cookie=_sid_cookie, csrf_cookie=_csrf_cookie)

reader = FirebaseReader(config, mode)

for user in reader.get_all_usernames():
    info = reader.get_value(user)

    new_user = User(info)
    message = new_user.create_message(config.get("CONSTANTS", "weather_api_key"))

    if message != None:
        messenger.send_sms(new_user.get_number(), message)
        print(f"Sent to {new_user.get_name()}\nMessage: '{new_user.get_message()}'")



