import smtplib
from email.message import EmailMessage
from PIL import Image

class Messenger:
    def __init__(self) -> None:
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        self.server.login("TheBuzNY@gmail.com", "wafmjdaxuhhltpdn")

    def send_text_message(self, person: str, msg: str):
        temp_msg = EmailMessage()
        temp_msg["Subject"] = "Daily TheBuz Message"
        temp_msg["From"] = "TheBuzNY@gmail.com"
        temp_msg["To"] = person        

        try:
            temp_msg.set_content("\n"+msg)
        
        except smtplib.SMTPSenderRefused:
            self.server.login("TheBuzNY@gmail.com", "wafmjdaxuhhltpdn")
            self.send_message(person, msg)

        self.server.send_message(temp_msg, "TheBuzNY@gmail.com", person)

    def send_image_messages(self, person: str, msg: list):

        temp_msg = EmailMessage()
        temp_msg["Subject"] = "Daily TheBuz Message"
        temp_msg["From"] = "TheBuzNY@gmail.com"
        temp_msg["To"] = person

        try:
            for message in msg:
                with open(message, "rb") as file:
                    if Image.open(message).format.lower() == "jpeg":
                        temp_msg.add_attachment(file.read(), maintype="image", subtype="jpg", filename=message)
        
        except smtplib.SMTPSenderRefused:
            self.server.login("TheBuzNY@gmail.com", "wafmjdaxuhhltpdn")
            self.send_message(person, msg)

        self.server.send_message(temp_msg, "TheBuzNY@gmail.com", person)