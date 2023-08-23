from dataclasses import dataclass
import os
import time

import firebase_admin as fba
import firebase_admin.db as fdb
import firebase_admin.credentials as fbc

@dataclass
class User:
    uuid: str
    name: str
    extensions: list
    messages: list
    number: str
    time: str
    beta: bool

class Database:
    def __init__(self) -> None:
        cred = fbc.Certificate(os.environ.get("FIREBASE_CRED_FILEPATH"))
        self.default_app = fba.initialize_app(cred, options={"databaseURL":"https://beeper5252022-default-rtdb.firebaseio.com/"})

        self.users = []
        self._refresh_people()

    def close_connection(self) -> None:
        fba.delete_app(self.default_app)

    def _refresh_people(self) -> None:
        for uuid in fdb.reference("usernames", app=self.default_app).get():
            self.users.append(User(uuid, 
                                   name=fdb.reference(f"usernames", app=self.default_app).child(uuid).get(),
                                   extensions=fdb.reference("extensions", app=self.default_app).child(uuid).get(),
                                   messages=fdb.reference("messages", app=self.default_app).child(uuid).get(),
                                   number=fdb.reference("carriers", app=self.default_app).child(uuid).get(),
                                   time=fdb.reference("times", app=self.default_app).child(uuid).get(),
                                   beta=fdb.reference("betas", app=self.default_app).child(uuid).get() 
                                   ))
