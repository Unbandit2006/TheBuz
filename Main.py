from sqlite3 import connect 
from pytextnow import Client
from datetime import datetime
from Library import Weather

### Default Variables ###
USERNAME = "daniel.zheleznov"
SID_COOKIE = "s%3AK_TlbPpYEIkY01wWEdvC_GV-y-PJFqnV.4YS4giXxnszUjh4gR5g%2FjOcpOozVfPnXRR5F6xZUOzs"
CSRF_COOKIE = "s%3A6DwypcTpav0UoWFcWZYu5lmp.pIu7k1cXm65Pj5Mi%2FblwW%2BJ0FF2DkjB14mJD2RafXUE"
DATABASE_LOCATION = "C:\\Dev\\Messaging\\ModernCode\\Test.db"

### Variables used by the program ###
Messenger = Client(USERNAME, SID_COOKIE, CSRF_COOKIE)
DB = connect(DATABASE_LOCATION)
DBCursor = DB.cursor()
Now = datetime.now() 
CurrentWeekday = Now.strftime("%w")
CurrentTime = str(Now)[11:16]
MonthName = Now.strftime("%B")
DayOfMonth = Now.strftime("%d")
Year = Now.strftime("%Y")

UsersInformation = DBCursor.execute("SELECT * FROM Users").fetchall()

### Goes through each user and sends if they wanted ###
for User in UsersInformation:
    DaysOfWeek = User[0].split(",")
    Number = str(User[3])

    if DaysOfWeek.__contains__(CurrentWeekday) == True:
        # Checks to see if the User selected for this day
        if CurrentTime == User[1]:
            if int(CurrentTime.split(":")[0]) >= 12:
                # Evening Text Message
                Messenger.send_sms(Number, rf"Good Afternoon {User[4]},\nToday is {MonthName} {DayOfMonth}, {Year}.")

                WeatherInfo = Weather(str(User[2]), User[5], DB).GetWeather()          
                Messenger.send_sms(Number, WeatherInfo)

            elif int(CurrentTime.split(":")[0]) <= 12:
                # Morning Text Message
                Messenger.send_sms(Number, rf"Good Morning {User[4]},\nToday is {MonthName} {DayOfMonth}, {Year}.")

                WeatherInfo = Weather(str(User[2]), User[5], DB).GetWeather()
                Messenger.send_sms(Number, WeatherInfo)