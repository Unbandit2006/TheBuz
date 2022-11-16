import Program
import configparser
import firebase_admin as admin
from firebase_admin import db
import pytextnow

class User:
    '''
    Name: User
    Type: Class
    Author: Daniel Zheleznov

    Description: User object for simplicity
    '''

    def __init__(self, user_info:dict):
        '''
        Constructor
        Description: Creates a User object for the developer to easily manipulate data
        Attributes: user_info - a dictionary of user data that can be retrieved from FirebaseReader
        '''
        self.__user = user_info
        self.__message = ""
        self.__has_run = False

    def get_name(self):
        '''
        Description: Returns the name of the user
        '''
        return self.__user.get("fname"), self.__user.get("lname")
    
    def get_number(self):
        '''
        Description: Returns the number of the user
        '''
        return str(self.__user.get("number"))
    
    def get_message(self):
        '''
        Description: Returns the message for the user
        '''
        return self.__message
    
    def get_run(self):
        '''
        Description: Returns the has_run for the user
        '''
        return self.__has_run

    def get_hour(self):
        '''
        Description: Returns the hour for the user
        '''
        return self.__user["time"].split(":")[0]
    
    def get_minutes(self):
        '''
        Description: Returns the minutes for the user
        '''
        return self.__user["time"].split(":")[1]
    
    def create_message(self, weather_api_key:str):
        '''
        Description: Creates a message, currently only does weather and current date
        Arguments: weather_api_key - the sequence of letters and numbers that weather api provides
        '''
        self.__user.get("time")
        time = Program.Time()
        
        user_time = self.__user.get("time").split(":")

        if user_time[0] == time.get_hour() and user_time[1] == time.get_minutes() and self.__has_run == False:
            self.__message += rf"Hello {self.__user.get('fname')}.\nToday is {time.get_day_name()}, {time.get_month_name()} {time.get_day_number()}, {time.get_year()}.\n"
            
            if self.__user.get("weather", False) and self.__has_run == False:
                weather = Program.Weather(weather_api_key, self.__user.get("zipcode"))
                self.__message += weather.get_data()

            self.__has_run = True
            return self.__message

class FirebaseReader:
    '''
    Name: FirebaseUser
    Type: Class
    Author: Daniel Zheleznov

    Description: Reads and Parses data from Firebase
    '''
    def __init__(self, config:configparser.RawConfigParser, mode:str):
        '''
        Constructor
        Description: Creates a FirebaseReader object to read the database
        Attributes: 
        config - config object of the ini file
        mode - where to look at in the ini file
        '''
        default_cred = config.get(mode, "cred_file_location")
        cert = admin.credentials.Certificate(default_cred)
        admin.initialize_app(cert, options={"databaseURL":"https://beeper5252022-default-rtdb.firebaseio.com/"})
        self.__db_ref = admin.db.reference("Users")

    def get_all_usernames(self):
        '''
        Description: Returns all the usernames from the database
        '''
        usernames = []
        for user in self.__db_ref.get():
            usernames.append(user)
        
        return usernames
    
    def get_etag(self):
        '''
        Description: Returns ETag to be used in get_if_changed
        '''
        etag = self.__db_ref.get(etag=True)
        etage = etag[1]
        return etage

    def get_if_changed(self, etag):
        '''
        Description: Returns if something in the Users table is changed
        '''
        return self.__db_ref.get_if_changed(etag)
    
    def get_value(self, key):
        '''
        Description: Returns the value for the provided key
        Attributes:
        key - what to search in the database
        '''
        return self.__db_ref.child(key).get()        

def create_user_objs(usernames: list) -> list[User]:
    user_objs = []

    for user in usernames:
        user_objs.append(User(reader.get_value(user)))
    
    return user_objs

config = configparser.RawConfigParser()
config.read("Config.ini")

mode = "HOME"

username = str(config.get("CONSTANTS", "username"))
_sid_cookie = str(config.get("CONSTANTS", "sid_cookie"))
_csrf_cookie = str(config.get("CONSTANTS", "csrf_cookie"))
messenger = pytextnow.Client(username, _sid_cookie, _csrf_cookie)
messenger.auth_reset(sid_cookie=_sid_cookie, csrf_cookie=_csrf_cookie)

reader = FirebaseReader(config, mode)

old_etag = reader.get_etag()
users = create_user_objs(reader.get_all_usernames())


while True:
    if reader.get_if_changed(old_etag)[0] == True:
        users = create_user_objs(reader.get_all_usernames())
        old_etag = reader.get_if_changed(old_etag)[2]

    time = Program.Time()
    for user in users:
        if user.get_run() == False and time.get_hour() == user.get_hour() and time.get_minutes() == user.get_minutes():
            message = user.create_message(config.get("CONSTANTS", "weather_api_key"))
            messenger.send_sms(user.get_number(), message)
            print(f"Sent to {user.get_name()}\nMessage: '{user.get_message()}'")



