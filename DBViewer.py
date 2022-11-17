import dearpygui.dearpygui as dpg
import firebase_admin as admin
from firebase_admin import db
import configparser


class FirebaseReader:
    '''
    Name: FirebaseUser
    Type: Class
    Author: Daniel Zheleznov

    Description: Reads and Parses data from Firebase
    '''
    def __init__(self, config:configparser.RawConfigParser, mode:str):
        '''
        Constructor
        Description: Creates a FirebaseReader object to read the database
        Attributes: 
        config - config object of the ini file
        mode - where to look at in the ini file
        '''
        default_cred = config.get(mode, "cred_file_location")
        cert = admin.credentials.Certificate(default_cred)
        admin.initialize_app(cert, options={"databaseURL":"https://beeper5252022-default-rtdb.firebaseio.com/"})
        self.__db_ref = admin.db.reference("Users")

    def get_etag(self):
        data = self.__db_ref.get(etag=True)[1]

        return data
    
    def get_ref(self):
        return self.__db_ref

    def get_all_usernames(self):
        '''
        Description: Returns all the usernames from the database
        '''
        usernames = []
        for user in self.__db_ref.get():
            usernames.append(user)
        
        return usernames
    
    def get_value(self, key):
        '''
        Description: Returns the value for the provided key
        Attributes:
        key - what to search in the database
        '''
        return self.__db_ref.child(key).get()


config = configparser.RawConfigParser()
config.read("Config.ini")

reader = FirebaseReader(config, "HOME")



dpg.create_context()
dpg.create_viewport(title='Firebase Viewer')

with dpg.window(tag="Primary"):

    for user in reader.get_all_usernames():
        with dpg.tree_node(label=user):
            dpg.add_selectable(label=reader.get_value(user)["fname"])
            dpg.add_selectable(label=reader.get_value(user)["lname"])
            dpg.add_selectable(label=reader.get_value(user)["number"])

# dpg.show_debug()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()