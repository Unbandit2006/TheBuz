import datetime
import firebase_admin as admin
from firebase_admin import db

class Anniversaries:
    def __init__(self, User):
        self.User = User
        self.Today = datetime.date.today()
        self.TodayMonth = self.Today.month
        self.TodayDay = self.Today.day
        self.Today = f"{self.TodayMonth}-{self.TodayDay}"

    def GetAniversariesData(self):
        Message = ""
        Celebrations = self.User.get("celebrations", False)

        if Celebrations != False:
            
            for Celebration in Celebrations:
                CelebrationType = Celebration
                CelebrationDate = Celebrations[Celebration][0]
                CelebrationAdditional = Celebrations[Celebration][1]

                if CelebrationDate == self.Today:
                    # TODO MAKE A FILING SYSTEM THAT WILL FILE OUT UNIQUE MESSAGES FOR ANNISVERSAY AN BIRTHDAYS

                    if CelebrationType == "birthday":
                        if CelebrationAdditional == "me":
                            Message += f"Happy Birthday {self.User.get('fname')}. 🎉🎂🎈\nMay this birthday and the coming year bring you good surprises — filled with sunshine, smiles and sweethearts.\n\n"
                        
                        else:
                            Message += f"Don't forget to congratulate {CelebrationAdditional} on their birthday. 🎉🎂🎈\n\n"

                    elif CelebrationType == "aniversary":
                        pass

        return Message

if __name__ == "__main__":
    USERNAME = "daniel.zheleznov"  # Type your textnow username here
    SID_COOKIE = "s%3Ap9_JYxmBC1B-YAe0kgIzhRv1DW1T8NjZ.2MJMus0dmOmI9hboz6c2MJERrZwiGx7qtPqOckVPtFg"  # Get your SID cookie from the textnow website and put it here
    CSRF_COOKIE = "s%3AV4rbcFeU2Za3InJ3kpCSpiQ2.siFz5SKHYYlCPOMneROboJXCfsHQZJk6BtRh%2B51c8fw"  # Get your CSRF cookie from the textnow website and put it here
    DATABASE_URL = "https://beeper5252022-default-rtdb.firebaseio.com/"  # Get your database URL from the firebase website and put it here
    DATABASE_CRED = "beeper5252022-firebase-adminsdk-te6kd-a403e68aff.json"  # Type what your credential filename
    APIKEY = "016e19390dba4ad5807184556222205"  # Get your API key from the weather API website and put it here

    Credentials = admin.credentials.Certificate(f"{DATABASE_CRED}")
    admin.initialize_app(Credentials, {"databaseURL": DATABASE_URL})

    UserRef = db.reference('Users')
    UserData = UserRef.get()
    
    for User in UserData:
        UserInfo = UserData[User]

        info = Anniversaries(UserInfo)
        print(info.GetAniversariesData())

