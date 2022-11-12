import requests as request
import json
from typing import Literal 
import time

class Time:
    def __init__(self):
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

    def get_minutes(self):
        if self.__current_time[4] <  10:
            return "0" + str(self.__current_time[4])
        
        else:
            return str(self.__current_time[4]) 
    
    def get_hour(self):
        if self.__current_time[3] < 10:
            return "0" + str(self.__current_time[3])
        
        else:
            return str(self.__current_time[3])

    def get_month_name(self):
        return self.__months.get(self.__current_time[1])
    
    def get_day_number(self):
        return str(self.__current_time[2])
    
    def get_day_name(self):
        return self.__weekdays.get(self.__current_time[6])
    
    def get_year(self):
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

        parsed_data["daily_max_temp"] = pretified_data["forecast"]["forecastday"][0]["day"]["maxtemp_f"]
        parsed_data["daily_min_temp"] = pretified_data["forecast"]["forecastday"][0]["day"]["maxtemp_f"]
        parsed_data["icon"] = self.__emojis.get(pretified_data["forecast"]["forecastday"][0]["day"]["condition"]["code"], "")
        parsed_data["overall_forecast"] = pretified_data["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        parsed_data["chance_rain"] = pretified_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
        parsed_data["chance_snow"] = pretified_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_snow"]

        return parsed_data
        

    def get_data(self):
        '''
        Description: Returns parsed weather data in string form
        Attributes: none
        '''
        data = self.__request_data()        
        if self.__expanded == 0:
            self.__return_message += r"\n\n"
            self.__return_message += rf"Overall Forecast: {data['overall_forecast']} {data['icon']}\n"
            self.__return_message += rf"Max Temperature: {data['daily_max_temp']} °F\n"
            self.__return_message += rf"Min Temperature: {data['daily_min_temp']} °F\n\n"

            if data["chance_rain"] != 0:
                self.__return_message += rf"There is a {data['chance_rain']}% chance of rain today. ☔☹\nDon't forget to bring an umbrella. ☂\n\n"
            
            if data["chance_snow"] != 0:
                self.__return_message += rf"There is a {data['chance_snow']}% chance of snow today. 🌨☹"
        
        return self.__return_message