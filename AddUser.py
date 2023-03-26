import TheBuzLib as TheBuz

name = input("Name: ")
number = input("Number: ")
time = input("Time [HH:MM]: ")
zipcode = input("Zipcode: ")

myReader = TheBuz.Reader("Config.json")
myDB = TheBuz.Database(myReader)

myDB.add_user(name, number, time, zipcode)
