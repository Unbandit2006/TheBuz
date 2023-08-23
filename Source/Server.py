import TheBuzLib
import os
import time

# TheBuz Server Initailization Sequence
database = TheBuzLib.Database()
print("Created TheBuz Database Connection")
messenger = TheBuzLib.Messenger()

# TheBuz Main Sequence
old_time = time.time()

running = True
while running:
    
    current_time = time.strftime("%H:%M")
    for person in database.users:
        if current_time == person.time:
            if person.beta == True:
                message = []
                
                for extension in person.extensions:
                    if os.path.exists(f"Buzzers/{extension}"):
                        os.chdir(f"../Buzzers/{extension}")
                        module = TheBuzLib.import_module_by_path("./Main.py", extension)
                        image = module.main_image(person.extensions[extension])
                        message.append(os.getcwd()+f"/"+image)

                        # TODO Check if the data has changed and if so, update the db

                messenger.send_image_messages(person.number, message)

            # else:
            #     message = ""

            #     for extension in person.extensions:
            #         if os.path.exists(f"Buzzers/{extension}"):
            #             os.chdir(f"Buzzers/{extension}")
            #             module = TheBuzLib.import_module_by_path("./Main.py", extension)
            #             text = module.main_text(person.extensions[extension])
            #             message += text              

            #     messenger.send_text_message(person.number, message)


                # DEBUG ONLY
                print(f"SENT: {person.number} @ {current_time} for {person.time}")

    

# TheBuz Server Shutdown Sequence
database.close_connection()
print("Closed TheBuz Database Connection.")
