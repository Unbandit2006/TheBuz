from firebase_admin import db
from firebase_admin import credentials

class Database:
	def __init__(self, certificate_file: str):
		self.cert = credentials.Certificate()
		self.name_ref = db.reference("/usersnames")

connection = Database("C:\\Dev\\Python\\TheBuz\\Src\\Config.json")
