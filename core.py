import TheBuzLib as TheBuz
import time
import calendar
import Buzzers

myReader = TheBuz.Reader("Config.json")
myDB = TheBuz.Database(myReader)
myUsers = myDB.get_users()

oldTime = time.localtime()

running = True
while running:
    for user in myUsers:
        newTime = time.localtime()

        newMonthName = calendar.month_name[newTime.tm_mon]
        newDay = "0"+str(newTime.tm_mday) if newTime.tm_mday < 10 else str(newTime.tm_mday)
        newYear = str(newTime.tm_year)

        newHour = "0"+str(newTime.tm_hour) if newTime.tm_hour < 10 else str(newTime.tm_hour)
        newMin = "0"+str(newTime.tm_min) if newTime.tm_min < 10 else str(newTime.tm_min)

        newTime = f"{newHour}:{newMin}"                    

        if newTime == user.get("time"):

            message = rf"Hello {user.get('name')}\n"\
                    rf"Today is {newMonthName} {newDay}, {newYear}\n\n"\

            if "Weather" in user.get("extensions"):
                message = Buzzers.Weather.add_to_message(user.get("extensions").get("Weather"), message)
            
            print(message)

