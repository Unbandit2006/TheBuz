import sqlite3 as sql
import pytextnow as ptn
import datetime as time
import requests
import json

def ReadConfigFile(filename:str):
    FileContent = []
    with open(filename, "r") as file:
        FileLines = file.readlines()
        for Line in FileLines:
            Line = Line.removesuffix("\n")

            if Line.__contains__("-"):
                Line = Line.split("-")
            
            FileContent.append(Line)

    return FileContent

class Message:
    def __init__(self, DatabaseLocation:str, Username:str, SIDCookie:str, CSRFCookie:str):
        self.DB = sql.connect(DatabaseLocation)
        self.DBCursor = self.DB.cursor()

        self.Messanger = ptn.Client(Username, SIDCookie, CSRFCookie)
    
    def check_times(self, send_time:str):
        current_time_unformated = time.datetime.now()
        current_time_formated = str(current_time_unformated)[11:16]


        if current_time_formated == send_time:
            return True
        else:
            return False

    def get_user_info(self, table:str):
        self.DBCursor.execute(f"SELECT * FROM {table}")
        results = self.DBCursor.fetchall()

        return results
    
    def get_weather_based_on_zip_and_time(self, zipcode:int, amnt_of_hours:int):
        approved_zips = self.get_user_info("ApprovedZips")

        for zip in approved_zips:
            approvedzipcode = zip[0]
            latitude = zip[1]
            longitude = zip[2]
            # info = zip[3]
            
            if approvedzipcode == zipcode:

                link = requests.request("GET", f"https://api.weather.gov/points/{latitude},{longitude}").content
                link = json.loads(link)
                link = link["properties"]["forecastHourly"]

                weather_data = requests.request("GET", f"{link}").content
                weather_data = json.loads(weather_data)
                weather_data = weather_data["properties"]["periods"]

                Info = rf"The Weather for the next {amnt_of_hours}\n of Zip Code: {zipcode} is\n\n"

                for Hour in range(amnt_of_hours):
                    StartHour = weather_data[Hour]["startTime"][11:13]
                    StartMin = weather_data[Hour]["startTime"][13:16]
                    Temperature = weather_data[Hour]["temperature"]
                    ShortForecast = weather_data[Hour]["shortForecast"]

                    Info += rf"{StartHour}{StartMin} Temperature: {Temperature}°F\nForecast: {ShortForecast}\n\n"
                    
                return Info
            
            else:
                continue
        

    def BlastMessages(self):
        now = time.datetime.now()
        current_weekday = now.strftime("%w")
        current_day_of_month = now.strftime("%B") + " " + now.strftime("%d") + ", " + now.strftime("%Y")
        UserInfo = self.get_user_info("Users")

        for User in UserInfo:
            User = list(User)
            User[0] = User[0].split(",")

            if User[0].__contains__(current_weekday):
                if self.check_times(User[1]) == True:
                    Zipcode = User[2]
                    PhoneNumber = str(User[3])
                    Name = User[4]
                    AmntOfHours = User[5]
                    UserTime = User[1].split(":")

                    WeatherData = self.get_weather_based_on_zip_and_time(Zipcode, AmntOfHours)
                    
                    if int(UserTime[0]) >= 12:
                        self.Messanger.send_sms(PhoneNumber, rf"Good Afternoon {Name},\nToday is {current_day_of_month}")
                        self.Messanger.send_sms(PhoneNumber, str(WeatherData))
                    else:
                        self.Messanger.send_sms(PhoneNumber, rf"Good Morning {Name},\nToday is {current_day_of_month}")
                        self.Messanger.send_sms(PhoneNumber, str(WeatherData))                        


            


if __name__ == '__main__':
    print(ReadConfigFile("C:\\Dev\\Messaging\\ModernCode\\Library\\.config"))
    # test = Message("C:\\Dev\\Messaging\\ModernCode\\Test.db", "daniel.zheleznov", "s%3AEVlLBKZ1B-jJxmJgvCP9ZnvBJ6OFWWok.0Xq5lXTGeOtIxKgZMlXnjElD0SRIYl2lRR2gq4zxmMw", "s%3A6CicNN4mdjzmeqhatTTN798R.IP8%2BdMpyfZkUAjlr67tw7iGRhHG3kritTTQ%2BaIhJPSc")
    # test.BlastMessages()