# Main File that get user data and blasts it
import firebase_admin as admin
from firebase_admin import db
import time
import GetWeatherData
import pytextnow

USERNAME = "" # Type your textnow username here
SID_COOKIE = "" # Get your SID cookie from the textnow website and put it here
CSRF_COOKIE = "" # Get your CSRF cookie from the textnow website and put it here
DATABASE_URL = "" # Get your database URL from the firebase website and put it here
APIKEY = "" # Get your API key from the weather API website and put it here

Credentials = admin.credentials.Certificate("Firebase-sdk.json")
admin.initialize_app(Credentials, {"databaseURL":DATABASE_URL})

UserRef = db.reference('Users')
UserData = UserRef.get()

CurrentTime = time.time()
CurrentTime = time.localtime(CurrentTime)
CurrentHour = CurrentTime.tm_hour
CurrentMin = CurrentTime.tm_min

Messenger = pytextnow.Client(USERNAME, SID_COOKIE, CSRF_COOKIE)

for User in UserData:
	Time = UserData[User]['time']
	Zipcode = UserData[User]['zipcode']
	AmntOfHours = UserData[User]['amntOfHours']
	Number = UserData[User]['number']
	Time = Time.split(":")

	if int(Time[0]) == CurrentHour and int(Time[1]) == CurrentMin:
		Message = GetWeatherData.WeatherData(APIKEY, Zipcode, AmntOfHours).GetWeatherData()
		Messenger.send_sms(str(Number), Message)