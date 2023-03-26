import TheBuzLib as TheBuz
import time
import calendar
import Buzzers

myReader = TheBuz.Reader("Config.json")
myDB = TheBuz.Database(myReader)
myUsers = myDB.get_users()
myMessenger = TheBuz.Messenger()

oldTime = time.localtime()

running = True
while running:
    newTime = time.localtime()

    newMonthName = calendar.month_name[newTime.tm_mon]
    newDay = "0"+str(newTime.tm_mday) if newTime.tm_mday < 10 else str(newTime.tm_mday)
    newYear = str(newTime.tm_year)

    newHour = "0"+str(newTime.tm_hour) if newTime.tm_hour < 10 else str(newTime.tm_hour)
    newMin = "0"+str(newTime.tm_min) if newTime.tm_min < 10 else str(newTime.tm_min)

    newTime = f"{newHour}:{newMin}"

    oldDay = "0"+str(oldTime.tm_mday) if oldTime.tm_mday < 10 else str(oldTime.tm_mday)
    if newDay != oldDay:
        myDB.refresh_users()

    for user in myUsers:                  

        if newTime == user.get("time"):

            message = f"Hello {user.get('name')}\n"\
                    f"Today is {newMonthName} {newDay}, {newYear}\n\n"\

            if "Weather" in user.get("extensions") and user.get("sent") == False:

                if user.get("sent") == False:
                    message = Buzzers.Weather.add_to_message(user.get("extensions").get("Weather"))
                
                    myMessenger.send_message(user.get("number"), message)
                    user["sent"] = True

