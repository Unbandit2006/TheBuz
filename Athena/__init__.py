import pytextnow as ptn
from firebase_admin import db as firebase_database
from collections.abc import Callable
import time

"""
A library of knowledge for TheBuz

Author:
    Daniel Zheleznov
"""


class User:
    def __init__(self, name: str, phone_number: str, message_time: str, **kwargs):
        """
        This is a Class to make a new user.

        Args:
            name: String = The Name of the User
            phone_number: String = The Phone Number of the User
            message_time: String = Time for the user to recieve the message

            KWARGS
            weather_info: Dictionary = This Contains all of the useful information for the weather
                zipcode: String = The zipcode the user requested

        Author:
            Daniel Zheleznov
        """
        self.name = name
        self.phone_number = phone_number
        self.message_time = message_time
        self.sent = False

        if "weather_info" in kwargs:
            self.weather_info = kwargs["weather_info"]

    def __str__(self):
        return f"{self.name}, {self.phone_number}, {self.message_time}, {self.weather_info}"


class UserList:
    def __init__(self, messenger: ptn.Client, database_ref: firebase_database.Reference):
        """
        This is a Class to make a user list, or the Collection of users in a easy to acces way.

        Args:
            messenger: ptn.Client = The messenger of the Core Program
            database_ref: firebase_database.Reference = The reference to the database in firebase, MUST BE GLOBAL REFERENCE

        Author:
            Daniel Zheleznov
        """
        self.users = None
        self.messenger = messenger
        self.database_ref = database_ref

    def make_user_list(self):
        """
        This is a Function to make the users and store it into a variable

        Author:
            Daniel Zheleznov
        """
        self.users = []

        usernames = self.database_ref.child("usernames")
        phone_numbers = self.database_ref.child("numbers")
        message_times = self.database_ref.child("times")
        weathers = self.database_ref.child("weather")

        for person in usernames.get():
            new_user = User(str(usernames.child(person).get()), str(phone_numbers.child(person).get()),
                            str(message_times.child(person).get()),
                            weather_info=weathers.child(person).get())

            self.users.append(new_user)

    def get_users(self):
        """
        This is a Function returns the users made by the user list

        Author:
            Daniel Zheleznov
        """
        return self.users

    def search(self, number: str):
        """
        This is a Function returns the user based on a search number

        Args:
            number: String = The number to search for in the user list

        Author:
            Daniel Zheleznov
        """
        for person in self.users:
            if person.phone_number == number:
                return person


class Logger:
    def __init__(self):
        """
        This is a Class to make a Logger.

        Author:
            Daniel Zheleznov
        """
        self.filename = ""

    def start_logger(self):
        """
        This is a function that will intialize everything.

        Author:
            Daniel Zheleznov
        """
        clock = time.localtime()

        self.filename = f"logs\\{clock.tm_year}_{clock.tm_mon}_{clock.tm_mday}.log"

        try:
            with open(self.filename, "x") as file:
                file.write("Date|Time|Type|Message\n")
                file.close()
            
        except Exception as e:
            pass
    
    def add_message(self, message:str, status:str):
        """
        This is a function that will apend message and the type of log to the file

        Author:
            Daniel Zheleznov
        """
        clock = time.localtime()

        try:
            with open(self.filename, "a") as file:
                file.write(f"{clock.tm_year}/{clock.tm_mon}/{clock.tm_mday}|{clock.tm_hour}:{clock.tm_min}|{status}|{message}\n")
                file.close()

            print(f"{clock.tm_year}/{clock.tm_mon}/{clock.tm_mday}|{clock.tm_hour}:{clock.tm_min}|{status}|{message}")
        except Exception as e:
            print("ERROR WITH LOGGER FILE NOT MADE")


class MessageReader:
    def __init__(self, messenger: ptn.Client, logger: Logger):
        """
        This is a Class to make a Reader to read messages from the client.

        Args:
            messenger: ptn.Client = The messenger of the Core Program

        Author:
            Daniel Zheleznov
        """
        self.mesenger = messenger
        self.messages = {}
        self.logger = logger

    def add_message(self, message: str, action: Callable[[dict], None]):
        """
        Adds a message to the message list to then be read and do an action to when the message
        equals to the recieved messages.

        Args:
            message: String = The String to be read in the revcieved messages
            action: Function = The function to be executed when the message equals to the recieved message.
                SHOULD take in a dict.

        Author:
            Daniel Zheleznov
        """
        self.messages[message.lower().strip()] = action

    def read_messages(self):
        """
        This function actually reads the mesages and based on the messages list, it actually executes the action

        Author:
            Daniel Zheleznov
        """
        message_info = {}

        try:
            for message in self.mesenger.get_unread_messages():
                message_info["number"] = message.number
                message_info["message"] = message.content.lower().strip()

                if message.content.lower().strip() in self.messages.keys():
                    self.messages[message.content.lower().strip()](message_info)

                message.mark_as_read()

        except Exception as e:
            self.logger.add_message(e, "Error")

