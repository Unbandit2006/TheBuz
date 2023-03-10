import Athena
import requests
import time
import gnews

icons = {
    1000: "🌞🌞",
    1003: "🌤🌤",
    1006: "☁☁",
    1009: "☁☁",
    1030: "🌫🌫",
    1063: "🌧🌧",
    1066: "❄❄",
    1069: "🌧🧊",
    1072: "🌨🌨",
    1087: "⛈⛈",
    1114: "🌬❄",
    1117: "🌨🌨",
    1135: "🌁🌁",
    1147: "❄🌁",
    1150: "🌧🌧",
    1153: "🌧",
    1168: "🥶🌧",
    1171: "🥶🌧",
    1180: "🌧",
    1183: "🌧",
    1186: "🌧🌧",
    1189: "🌧🌧",
    1192: "🌧🌧",
    1195: "🌧🌧",
    1198: "🥶🌧",
    1201: "🥶🌧",
    1204: "🌧🧊",
    1207: "🌧🧊",
    1210: "❄",
    1213: "❄",
    1216: "❄❄",
    1219: "❄❄",
    1222: "❄❄",
    1225: "❄",
    1237: "🧊",
    1240: "🌧",
    1243: "🌧🌧",
    1246: "🌧🌧",
    1249: "🧊🌧",
    1252: "🧊🌧",
    1255: "🌨",
    1258: "🌨🌨",
    1261: "🧊",
    1264: "🧊🧊",
    1273: "⛈",
    1276: "⛈⛈",
    1279: "❄⚡",
    128: "❄⚡"
}


def joke():
    req = requests.get("https://official-joke-api.appspot.com/jokes/general/random")

    setup = req.json()[0].get("setup")
    punchline = req.json()[0].get("punchline")

    return setup, punchline


class Weather:
    def __init__(self, user: Athena.User, logger: Athena.Logger):
        self.user = user
        self.logger = logger

    def create_message(self):
        global content, current_weather, min_value, max_value, percentage_rain, percentage_snow
        actual_time = time.strftime("%A. %B, %d %Y")
        formatted_time = rf"{actual_time}\n\n"
        message = rf"Hello {self.user.name}.\nToday is {formatted_time}"

        current_weather = ""
        overall_weather = ""
        max_value = ""
        min_value = ""
        percentage_rain = ""
        percentage_snow = ""

        try:
            user_zipcode = self.user.weather_info["zipcode"]

            request = requests.get(f'http://api.weatherapi.com/v1/forecast.json',
                               {"key": "016e19390dba4ad5807184556222205", "q": user_zipcode, "days": 1,
                                "aqi": "no", "alert": "yes"})
            
            content = request.json()

            current_weather = content.get("current", {}).get("feelslike_f", "N/A")
            overall_weather = content.get("forecast", {}).get("forecastday", ())[0]["day"]["condition"]
            overall_icon = icons[overall_weather['code']] 
            max_value = content.get("forecast", {}).get("forecastday", ())[0].get("day", {}).get("maxtemp_f", "N/A")
            min_value = content.get("forecast", {}).get("forecastday", ())[0].get("day", {}).get("mintemp_f", "N/A")
            percentage_rain = content.get("forecast", {}).get("forecastday", ())[0].get("day", {}).get("daily_chance_of_rain", "N/A")
            percentage_snow = content.get("forecast", {}).get("forecastday", ())[0].get("day", {}).get("daily_chance_of_snow", "N/A")


            message += rf"It currently feels like: {current_weather} °F\nOverall forecast: {overall_weather['text']} {overall_icon}\n"\
                        rf"Max. temperature: {max_value} °F\nMin. temperature: {min_value} °F\n"
            
            if percentage_rain != 0:
                message += rf"There is a {percentage_rain}% chance of rain today\nDon't forget to bring your Umbrella ☂\n\n"
            
            elif percentage_snow != 0:
                message += rf"There is a {percentage_snow}% chance of snow today\nDon't forget to bring your Umbrella ☂\nAnd dress warm.\n\n"

        except Exception as e:
            self.logger.add_message(e, "Error Weather")

            funny_joke = joke()

            message += rf"Sadly we couldn't retrieve the weather for today. :(\nHere is a joke in the meantime.\n{funny_joke[0]}\n{funny_joke[1]}\n\n"

        self.user.message = message

class News:
    def __init__(self, user):
        self.user = user

    def create_message(self):
        news = gnews.GNews(max_results=4)

        self.user.message = r"Top Headlines\n\n"

        latest = news.get_top_news()

        for article in latest:
            self.user.message += rf"{article['title']}\n\n"

    def add_message(self):
        news = gnews.GNews(max_results=4)

        self.user.message += r"Top Headlines\n\n"

        latest = news.get_top_news()

        for article in latest:
            self.user.message += rf"{article['title']}\n\n"
