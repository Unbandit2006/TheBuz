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

    # holiday = ""+Buzzers.Holidays.get_holiday(newTime)

    newMonthName = calendar.month_name[newTime.tm_mon]
    newDay = "0"+str(newTime.tm_mday) if newTime.tm_mday < 10 else str(newTime.tm_mday)
    newYear = str(newTime.tm_year)

    newHour = "0"+str(newTime.tm_hour) if newTime.tm_hour < 10 else str(newTime.tm_hour)
    newMin = "0"+str(newTime.tm_min) if newTime.tm_min < 10 else str(newTime.tm_min)

    newTime = f"{newHour}:{newMin}"

    oldDay = "0"+str(oldTime.tm_mday) if oldTime.tm_mday < 10 else str(oldTime.tm_mday)

    # Only is true on diff day from start day
    if newDay != oldDay:
        myUsers = myDB.get_users()
        oldTime = time.localtime()
        myUsers = myDB.get_users()

    for user in myUsers:                  

        if newTime == user.get("time"):

            message = f"Hello {user.get('name')}\n"\
                    f"Today is {newMonthName} {newDay}, {newYear}\n\n"\

            if user.get("sent") == False:

                if "Weather" in user.get("extensions"):
                    message += Buzzers.Weather.add_to_message(user.get("extensions").get("Weather"))

                if "News" in user.get("extensions"):
                    message += Buzzers.News.get_news()
            
                myMessenger.send_message(user.get("number"), message)
                user["sent"] = True

    
    # Reading messages
    for message in myDB.get_messages():
        uuid = message[0]
        to = message[1][0]
        body = message[1][1].lower().strip().split(" ")
        value = message[1][3]

        user = myDB.find_user(to)
        extensions = user.get("extensions")
        
        if value == False:
            if body[0] == "refresh":
                if body[1] in map(lambda x: x.lower(), extensions):
                    if "weather" == body[1]:
                        message = Buzzers.Weather.add_to_message(user.get("extensions").get("Weather"))
                        myMessenger.send_message(to, message)

                        myDB.change_value(uuid)

                    elif "news" == body[1]:
                        message = Buzzers.News.get_news()
                        myMessenger.send_message(to, message)

                        myDB.change_value(uuid)

                    else:
                        message = "That is an invalid command\nPlease try typing 'Refresh' before the buzzer you want to recieve."
                        myMessenger.send_message(to, message)
                        myDB.change_value(uuid)

                
                else:
                    message = "That is an invalid command\nPlease try typing 'Refresh' before the buzzer you want to recieve."
                    myMessenger.send_message(to, message)
                    myDB.change_value(uuid)

            else:
                message = "That is an invalid command\nPlease try typing 'Refresh' before the buzzer you want to recieve."
                myMessenger.send_message(to, message)
                myDB.change_value(uuid)

