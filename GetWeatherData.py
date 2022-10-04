# This is the file that will get data from the WeatherAPI

import json
import requests
import time


class WeatherData:
    def __init__(self, APIKey, Zipcode, Hours):
        self.APIKey = APIKey
        self.Zipcode = Zipcode
        self.Hours = Hours
        self.Message = None

    def GetWeatherData(self):

        Request = requests.request("GET",
                                   f"https://api.weatherapi.com/v1/forecast.json?key={self.APIKey}&q={self.Zipcode}&days=1").text
        Content = json.loads(Request)

        LocalTime = time.time()
        LocalTime = time.localtime(LocalTime)
        LocalHour = LocalTime.tm_hour

        ListofHours = Content['forecast']['forecastday'][0]['hour']

        HoursToSearch = []
        for i in range(self.Hours + 1):
            HoursToSearch.append(LocalHour + i)

        Message = [rf"The Weather for the next {self.Hours} hours for Zipcode {self.Zipcode}:\n\n"]
        for Hour in HoursToSearch:
            Period = ""

            if int(Hour) == 24:
                Hour = 12
                Period = "AM"

            elif int(Hour) > 24:
                Hour = int(Hour) - 24
                Period = "AM"

                if int(Hour) == 12:
                    Period = "PM"

                elif int(Hour) > 12:
                    Hour = int(Hour) - 12
                    Period = "PM"
            
            elif int(Hour) > 12:
                Hour = int(Hour) - 12
                Period = "PM"
            
            elif int(Hour) < 12:
                Hour = int(Hour)
                Period = "AM"
            
            elif int(Hour) == 12:
                Hour = int(Hour)
                Period = "PM"

            Time = ListofHours[Hour]['time'][11:16]
            Temperature = ListofHours[Hour]['temp_f']
            FeelsLike = ListofHours[Hour]['feelslike_f']
            BriefForecast = ListofHours[Hour]['condition']['text']

            Message.append(
                rf"At {Hour}:{Time[3:]} {Period}\nBrief Forecast: {BriefForecast}\nTemperature: {Temperature}°F\nFeels Like: {FeelsLike}°F\n\n")

        self.Message = "".join(Message)

        return self.Message
