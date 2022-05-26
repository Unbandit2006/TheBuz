# Main File that get user data and blasts it
import firebase_admin as admin
from firebase_admin import db
import time
import GetWeatherData
import pytextnow

Credentials = admin.credentials.Certificate("Firebase-sdk.json")
admin.initialize_app(Credentials, {"databaseURL":"https://beeper5252022-default-rtdb.firebaseio.com/"})

UserRef = db.reference('Users')
UserData = UserRef.get()

CurrentTime = time.time()
CurrentTime = time.localtime(CurrentTime)
CurrentHour = CurrentTime.tm_hour
CurrentMin = CurrentTime.tm_min

Messenger = pytextnow.Client('daniel.zheleznov', 's%3AAzwc-q8e75aJ_a4eWuPrN-K324IiXIWl.jRRw9gH%2FIpyENQ4yxzKTaKsLspUWQmS0j39Z6nSbuEc', 's%3AYGxOhxYPJKW6HUv9sY8e4jH7.%2FyGJf1oP9YNycMOjQfk%2FqjtOoI4yU3GKbZVD1DDRfE8')

for User in UserData:
	Time = UserData[User]['time']
	Zipcode = UserData[User]['zipcode']
	AmntOfHours = UserData[User]['amntOfHours']
	Number = UserData[User]['number']
	Time = Time.split(":")

	# if int(Time[0]) == CurrentHour and int(Time[1]) == CurrentMin:
	# 	Message = GetWeatherData.WeatherData("016e19390dba4ad5807184556222205", Zipcode, AmntOfHours).GetWeatherData()
	# 	Messenger.send_sms(str(Number), Message)

	Message = GetWeatherData.WeatherData("016e19390dba4ad5807184556222205", Zipcode, AmntOfHours).GetWeatherData()
	Messenger.send_sms(str(Number), Message)