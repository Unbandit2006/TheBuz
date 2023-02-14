import pytextnow as ptn
from firebase_admin import db as firebase_database

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
        return self.users
