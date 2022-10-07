# Main File that get user data and blasts it
import firebase_admin as admin
from firebase_admin import db
import time
import GetWeatherData
import pytextnow
import calendar

USERNAME = "daniel.zheleznov"  # Type your textnow username here
SID_COOKIE = "s%3Ap9_JYxmBC1B-YAe0kgIzhRv1DW1T8NjZ.2MJMus0dmOmI9hboz6c2MJERrZwiGx7qtPqOckVPtFg"  # Get your SID cookie from the textnow website and put it here
CSRF_COOKIE = "s%3AV4rbcFeU2Za3InJ3kpCSpiQ2.siFz5SKHYYlCPOMneROboJXCfsHQZJk6BtRh%2B51c8fw"  # Get your CSRF cookie from the textnow website and put it here
DATABASE_URL = "https://beeper5252022-default-rtdb.firebaseio.com/"  # Get your database URL from the firebase website and put it here
DATABASE_CRED = "beeper5252022-firebase-adminsdk-te6kd-a403e68aff.json"  # Type what your credential filename
APIKEY = "016e19390dba4ad5807184556222205"  # Get your API key from the weather API website and put it here

Credentials = admin.credentials.Certificate(f"{DATABASE_CRED}")
admin.initialize_app(Credentials, {"databaseURL": DATABASE_URL})

UserRef = db.reference('Users')
UserData = UserRef.get()

CurrentTime = time.time()
CurrentTime = time.localtime(CurrentTime)
CurrentHour = CurrentTime.tm_hour
CurrentMin = CurrentTime.tm_min
CurrentDay = CurrentTime.tm_mday
CurrentMonth = CurrentTime.tm_mon
CurrentMonth = calendar.month_name[CurrentMonth]
CurrentDOTW = CurrentTime.tm_wday
CurrentDOTW = calendar.day_name[CurrentDOTW]
CurrentYear = CurrentTime.tm_year

Messenger = pytextnow.Client(USERNAME, SID_COOKIE, CSRF_COOKIE)
Messenger.auth_reset(sid_cookie=SID_COOKIE, csrf_cookie=CSRF_COOKIE)

for User in UserData:
    UserInfo = UserData[User]
    Name = UserInfo['fname'] + " " + UserInfo['lname']
    Time = UserInfo['time']
    Time = Time.split(":")
    Zipcode = UserInfo['zipcode']
    AmntOfHours = UserInfo['amntOfHours']
    Number = UserInfo['number']

    if int(Time[0]) == CurrentHour and int(Time[1]) == CurrentMin:
        Message = ""

        # Greetings
        Message += rf"Hello, {Name}.\nToday is {CurrentDOTW}, {CurrentMonth} {CurrentDay}, {CurrentYear}.\n\n"

        Message += GetWeatherData.WeatherData(APIKEY, Zipcode, AmntOfHours).GetWeatherData()
        print(f"\nThe Weather Data is {Message}")
        print(len(Message))
        Messenger.send_sms(str(Number), Message)
        print(f"Sent To {UserInfo} at {CurrentTime}\n")
