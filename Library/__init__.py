from requests import request
from json import loads
import logging as log

log.basicConfig(level=log.INFO, filename="log.log", filemode="a", format="%(asctime)s||%(message)s")

class Weather:
    def __init__(self, ZipCode, AmntOfHours, DBConnection):
        self.Zip = ZipCode
        self.Hours = AmntOfHours
        self.DB = DBConnection
        self.DBCursor = self.DB.cursor()
    
    def GetWeather(self):
        Geolocation = self.DBCursor.execute("SELECT * FROM ApprovedZips WHERE Zips=?", [self.Zip]).fetchall()
        Geolocation = Geolocation[0]

        if Geolocation[3] == None:
            # This is for when the link is null
            # Gets link for the hourly forecast

            try:
                GetLink = request("GET", f"https://api.weather.gov/points/{Geolocation[1]},{Geolocation[2]}")
                JSONContent = loads(GetLink.text)
                Link = JSONContent["properties"]["forecastHourly"]
        
                # Places that Link into the DB
                self.DBCursor.execute("UPDATE ApprovedZips SET Link = (?) WHERE Zips = (?)", [(Link), (self.Zip)])
                self.DB.commit()

                ### Functionality To Send Info ###
                Forecast = request("GET", f"{Link}")
                JSONContent = loads(Forecast.text)
                Time = JSONContent["properties"]["periods"]
                Information = [rf"This is the Weather for the next {self.Hours} hours for Zipcode {self.Zip}:\n\n"]

                for Hour in range(self.Hours):
                    Info = rf"{Time[Hour]['startTime'][11:13]}{Time[Hour]['startTime'][13:16]} Temperature: {Time[Hour]['temperature']}°F\nForecast: {Time[Hour]['shortForecast']}\n\n"
                    Information.append(Info)

                Informations = "".join(Information)

                return Informations
            
            except Exception as e:
                log.exception(f"ERROR: {e}||PROPERTIES: {JSONContent['properties']}")

        else:
            # This is for when link is not null meaning it is actually populated with a link
            ### Functionality To Send Info ###
            try:
                Link = self.DBCursor.execute("SELECT * FROM ApprovedZips WHERE Zips=?", [self.Zip]).fetchall()
                Link = Link[0][3]

                Forecast = request("GET", f"{Link}")
                JSONContent = loads(Forecast.text)
                Time = JSONContent["properties"]["periods"]
                Information = [rf"This is the Weather for the next {self.Hours} hours for Zipcode {self.Zip}:\n\n"]
    
                for Hour in range(self.Hours):
                    Info = rf"{Time[Hour]['startTime'][11:13]}{Time[Hour]['startTime'][13:16]} Temperature: {Time[Hour]['temperature']}°F\nForecast: {Time[Hour]['shortForecast']}\n\n"
                    Information.append(Info)

                Informations = "".join(Information)

                return Informations
            
            except Exception as e:
                log.exception(f"ERROR: {e}||PROPERTIES: {JSONContent['properties']}")