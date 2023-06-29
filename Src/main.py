import TheBuzLib as TBL

# TheBuz Startup Sequence
print("Startup Sequence")

reader = TBL.Reader("Config.json")
print("Created Config Reader")

database = TBL.Database(reader)
print("Created Database Connection")

# 
