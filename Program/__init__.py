import requests as request
import json
from typing import Literal 
import time
import configparser
import firebase_admin as admin
from firebase_admin import db

class Time:
    def __init__(self):
        '''
        Name: Time
        Type: Class
        Author: Daniel Zheleznov

        Description: Creates Time object to get that time
        '''
        self.__current_time_secounds = time.time()
        self.__current_time = time.localtime(self.__current_time_secounds)

        self.__months = {
            1:"January",
            2:"February",
            3:"March",
            4:"April",
            5:"May",
            6:"June",
            7:"July",
            8:"August",
            9:"September",
            10:"October",
            11:"November",
            12:"December"
        }

        self.__weekdays = {
            0:"Monday",
            1:"Tuesday",
            2:"Wednesday",
            3:"Thurday",
            4:"Friday",
            5:"Saturday",
            6:"Sunday"
        }
    
    def get_unix(self):
        return self.__current_time_secounds

    def get_minutes(self):
        '''
        Description: Returns the current minutes
        '''
        if self.__current_time[4] <  10:
            return "0" + str(self.__current_time[4])
        
        else:
            return str(self.__current_time[4]) 
    
    def get_hour(self):
        '''
        Description: Returns the current hour
        '''
        if self.__current_time[3] < 10:
            return "0" + str(self.__current_time[3])
        
        else:
            return str(self.__current_time[3])

    def get_month_name(self):
        '''
        Description: Returns the Month Name
        '''
        return self.__months.get(self.__current_time[1])
    
    def get_month_number(self):
        '''
        Description: Returns the Month Number
        '''    
        return self.__current_time[1]

    def get_day_number(self):
        '''
        Description: Return the day number
        '''
        return str(self.__current_time[2])
    
    def get_day_name(self):
        '''
        Description: Return the day name
        '''
        return self.__weekdays.get(self.__current_time[6])
    
    def get_year(self):
        '''
        Description: Return the current year
        '''
        return str(self.__current_time[0])

'''
Name: Weather
Type: Class
Author: Daniel Zheleznov

Description: Returns weather data parsed from WeatherAPI
'''
class Weather:
    def __init__(self, api_key:str, zipcode:str, aqi:Literal["yes","no"]="yes", expanded:bool = 0, expanded_info:list = None):
        '''
        Constructor
        Description: Creates a Weather Object
        Attributes:
        api_key - the api key provided by WeatherAPI
        zipcode - the zipcode for the user
        amount_of_hours - the amount of hours the user wants to get
        expanded - get expanded information of the weather (user will get to decide on the website), 0 means no, 1 means yes
        expanded_info - what the user wants to recieve in list form
        '''
        self.__api_key = api_key
        self.__zipcode = zipcode
        self.__aqi = aqi
        self.__expanded = expanded
        self.__expanded_info = expanded_info
        self.__return_message = ""

        # Got data from https://www.weatherapi.com/docs/weather_conditions.json
        self.__emojis = {
            1000:"☀",
            1003:"⛅",
            1006:"☁",
            1009:"☁☁",
            1030:"🌫",
            1063:"☂",
            1066:"🌨",
            1069:"🌨❄",
            1072:"❄☔",
            1087:"⛈",
            1114:"🌬❄",
            1117:"🌨❄",
            1135:"🌫",
            1147:"❄🌫",
            1150:"🌧",
            1153:"🌧",
            1168:"❄🌧",
            1171:"❄🌧🌧",
            1180:"🌧",
            1183:"🌧",
            1186:"🌧",
            1189:"🌧",
            1192:"🌧🌧🌧",
            1195:"🌧🌧🌧",
            1198:"❄🌧",
            1201:"❄🌧🌧",
            1204:"🌨☔",
            1207:"🌨🌨☔",
            1210:"🌨",
            1213:"🌨",
            1216:"🌨",
            1219:"🌨🌨",
            1222:"🌨🌨🌨",
            1225:"🌨🌨🌨",
            1237:"❄❄❄🌧",
            1240:"🌧",
            1243:"🌧🌧",
            1246:"🌧🌧🌧",
            1249:"🌨☔",
            1252:"🌨🌨☔",
            1255:"🌨",
            1258:"🌨🌨",
            1261:"❄🌨",
            1264:"❄🌨🌨",
            1273:"⛈",
            1276:"⛈⛈",
            1279:"❄⚡",
            1282:"❄⚡⚡"
        }

    def __request_data(self):
        '''
        Internal Function
        Description: returns data from the API
        Attributes: none
        '''        
        req = request.request("GET", "https://api.weatherapi.com/v1/forecast.json", params={"key":self.__api_key, "q":self.__zipcode, "days":1, "aqi":self.__aqi})
        raw_data = req.text
        parsed_data = {}
        pretified_data = json.loads(raw_data)

        parsed_data["daily_max_temp_f"] = pretified_data["forecast"]["forecastday"][0]["day"]["maxtemp_f"]
        parsed_data["daily_max_temp_c"] = pretified_data["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
        parsed_data["daily_min_temp_f"] = pretified_data["forecast"]["forecastday"][0]["day"]["mintemp_f"]
        parsed_data["daily_min_temp_c"] = pretified_data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
        parsed_data["icon"] = self.__emojis.get(pretified_data["forecast"]["forecastday"][0]["day"]["condition"]["code"], "")
        parsed_data["overall_forecast"] = pretified_data["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        parsed_data["chance_rain"] = pretified_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
        parsed_data["chance_snow"] = pretified_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_snow"]
        parsed_data["current"] = pretified_data["current"]

        return parsed_data
        

    def get_data(self, degrees:str="f"):
        '''
        Description: Returns parsed weather data in string form
        Attributes: none
        '''
        data = self.__request_data()        
        if self.__expanded == 0:
            self.__return_message += r"\n\n"
            self.__return_message += rf"Overall Forecast: {data['overall_forecast']} {data['icon']}\n"
            query_max = "daily_max_temp_"+degrees
            query_min = "daily_min_temp_"+degrees
            self.__return_message += rf"Max Temperature: {data[query_max]} °{degrees.capitalize()}\n"
            self.__return_message += rf"Min Temperature: {data[query_min]} °{degrees.capitalize()}\n\n"

            if data["chance_rain"] != 0:
                self.__return_message += rf"There is a {data['chance_rain']}% chance of rain today. ☔☹\nDon't forget to bring an umbrella. ☂\n\n"
            
            if data["chance_snow"] != 0:
                self.__return_message += rf"There is a {data['chance_snow']}% chance of snow today. 🌨☹"
        
        return self.__return_message

    def get_current_feels_like_temp(self, degrees:str="f"):
        data = self.__request_data()
        query = "feelslike_"+degrees
        current_feels_like = rf"It currently feels like: {data['current'][query]} °{degrees.capitalize()}"

        return current_feels_like
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
    
    def get_zipcode(self):
        '''
        Description: Returns the zipcode of the user
        '''
        return self.__user.get("zipcode")
    
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
    
    def get_days(self):
        return self.__user.get("dow")
    
    def create_message(self, weather_api_key:str):
        '''
        Description: Creates a message, currently only does weather and current date
        Arguments: weather_api_key - the sequence of letters and numbers that weather api provides
        '''
        time = Time()
        
        user_time = self.__user.get("time").split(":")
        if user_time[0] == time.get_hour() and user_time[1] == time.get_minutes() and self.__has_run == False:
            self.__message += rf"Hello {self.__user.get('fname')}.\nToday is {time.get_day_name()}, {time.get_month_name()} {time.get_day_number()}, {time.get_year()}.\n"
            
            if self.__user.get("weather", False) and self.__has_run == False:
                weather = Weather(weather_api_key, self.__user.get("zipcode"))
                self.__message += weather.get_current_feels_like_temp()
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


import os
class Logger:
    def __init__(self, clock:Time):
        self.clock = clock
    
    def start(self):
        directory = f"{self.clock.get_year()}/{self.clock.get_month_number()}"
        directory = os.path.abspath(directory)

        if not os.path.exists(directory):
            os.makedirs(directory)

        file = f"log_{self.clock.get_year()}{self.clock.get_month_number()}{self.clock.get_day_number()}.psv"
        file = directory +"/"+file
        self.current_file = file

        if not os.path.exists(file):
            with open(file, "x") as f:
                f.write("Time|Recipient|Message|Status\n")
            
    def message(self, recipient, message, status):
        with open(self.current_file, "a", encoding="utf-8") as f:
            message = str(message)
            f.write(f"{self.clock.get_hour()}:{self.clock.get_minutes()}|{recipient}|{message}|{status}\n")
            print(f"{self.clock.get_hour()}:{self.clock.get_minutes()}|{recipient}|{message}|{status}\n")