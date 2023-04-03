import holidays
from datetime import date

usHolidays = holidays.US()


def get_holiday(timeObj):
    timeString = f"{timeObj.tm_year}-{timeObj.tm_mon}-{timeObj.tm_mday}"

    if timeString in usHolidays:
        return usHolidays.get(timeString)
