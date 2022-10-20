# The Buz
For several months, I've been working on this project on and off. It was my pride and joy, but the time has come to say goodbye. It has taught me a great deal. It caused me a tremendous deal of pain, but I have never been happier with it. I will now release the project as open source for everyone to use. But be warned: I have a few things to tell you about how to run it.
## Requirements to run The Buz
Well since it is a Python project, you will need to install Python as well as pip, Python's package manager.

</br><b>To check if you have Python run:</b>
```
python --version
```
If you get a similar result to this:
```
Python 3.9.9
```
You are perfectly fine with what you have.
</br><b>WARNING:</b> YOU NEED 3.9.9 OR HIGHER FOR BEEPER TO WORK

</br><b>To check if you have pip run:</b>
```
pip --version
```
If you get a similar result to this:
```
pip 22.0.4
```
You are perfectly fine with what you have.

</br><b>Install Proper Modules For Beeper To Work</b>
</br>Now for this you can use anything a Python Virtual Environment or just local machine. But no matter which one you use run this command:
```
pip install firebase_admin pytextnow
```

## To Run The Buz
Now that everything is installed you have just a little bit to run the program

- You need to make a Firebase account and make a realtime database with whatever name you want.
- You then need to go and obtain a private key from Project Settings > Service accounts > Python > Generate new private key
- Once you get that move that file into the directory with the Main.py File
- Now go back to your Realtime Database and grab the url. (The URL is located above where the data will go) and now paste it into the quotations in the DATABASE_URL variable in the Main.py file.

Now you got Firebase over with, go to TextNow

- Retrieve your username from TextNow either by making a new account or by copying you name, and pasting it into the USERNAME variable, inside the quotations in the Main.py file
- Retrieve your connect.sid from TextNow and paste the cookie value inside of the quotations for the variable called SID_COOKIE (If you don't know how to get the connect.sid go and watch this video)
<video src="Videos/SID_COOKIE.mp4" type="video/mp4" controls width=800></video>
- Now you need to Retrieve _csrf cookie value in the same manner you got the connect.sid cookie, and once you got it paste it into the quotations for variable CSRF_COOKIE in the Main.py File

Now you got TextNow over with, go to [WeatherAPI](https://www.weatherapi.com/)
- Make an account on WeatherAPI it is free
- Once you did that go and create an API Key, copy and paste that key in the API_KEY variable in the Main.py file

<b>FINALLY YOU CAN RUN IT</b>

## To get messages
To get and send messages you need to make a key-key-value in Firebase Realtime Database section

<b>STRUCTURE FOR DB</b> (Use Exact Names For Keys):
```
Users {
    RandomUser1 {
        "amntOfHours":int value;
        "fname":str value;
        "lname":str value;
        "number":int value;
        "time":"Hour:Min" /*In that notaition Hour can be from 0-23*/;
        "zipcode":int value;
        "celebrations": dict value /*In the dictionary it will be the "NameOfCelebration":["Date","AdditionalInfo"]*/;
    };
    RandomUser2 {
        "amntOfHours":int value;
        "fname":str value;
        "lname":str value;
        "number":int value;
        "time":"Hour:Min" /*In that notaition Hour can be from 0-23*/;
        "zipcode":int value;
        "celebrations": dict value /*In the dictionary it will be the "NameOfCelebration":["Date","AdditionalInfo"]*/;
    };
};
```

## Tools
### Current Tools
[WeatherAPI](https://www.weatherapi.com/)
[DB](https://firebase.com)
[Text](https://www.textnow.com)

### Upcoming Tools
[WeatherAPI](https://www.visualcrossing.com/weather-data)
