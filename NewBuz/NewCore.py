# TheBuz Core Functionality
# Written by: Daniel Zhel
# Written on: 06/18/2023

import TheBuzLib as TBL
import time
import os

oldTime = time.localtime()

# logger = TBL.Logger()
# logger.write("Init", "Logger Active")

configReader = TBL.ConfigReader("C:\\Dev\\Python\\TheBuz\\Src\\Config.json")
# logger.write("Init", "ConfigReader Active")

database = TBL.Database(configReader)
# logger.write("Init", "DatabaseReader Active")

MAIN_BUZZER_FOLDER = "C:\\Dev\\Python\\TheBuz\\Buzzers\\"
while True:
    newTime = time.localtime()
    if oldTime.tm_mday != newTime.tm_mday:
        # logger.changeFile(newTime)
        oldTime = newTime


    for person in database.getPeople():
        personBuzzers = person[3]
        personTime = list(map(int, person[0].split(":")))

        # Calculate 30 min in advance to the persons time
        personTimeInMin = personTime[0] * 60 + personTime[1]
        personTimeInMin -= 30
        
        newHour = personTimeInMin // 60
        newMin = personTimeInMin % 60

        # if newHour == newTime.tm_hour and newMin == newTime.tm_min:
        for buzzer in personBuzzers:
            newMonth = "0" + str(newTime.tm_mon) if newTime.tm_mon < 10 else newTime.tm_mon
            newMDay = "0" + str(newTime.tm_mday) if newTime.tm_mday < 10 else newTime.tm_mday
            hour = "0" + str(newTime.tm_hour) if newTime.tm_hour < 10 else newTime.tm_hour
            mins = "0" + str(newTime.tm_min) if newTime.tm_min < 10 else newTime.tm_min
            
            altMins = (int(mins) + 30) % 60
            altHour = (int(hour) + (int(mins) + 30) // 60) % 24
            altMins = "0" + str(altMins) if altMins < 10 else altMins
            altHour = "0" + str(altHour) if altHour < 10 else altHour

            if not os.path.exists(f"C:\\Dev\\Python\\TheBuz\\NewBuz\\images\\{buzzer};{personBuzzers[buzzer]};{newTime.tm_year}-{newMonth}-{newMDay}-{hour}-{mins}.jpg"):
                pass



    quit(0)
