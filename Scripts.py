import Athena
import requests
import time
import gnews

icons = {
    1000: "🌞🌞🌞",
    1003: "🌤🌤🌤",
    1006: "☁☁",
    1009: "☁☁☁",
    1030: "🌫🌫🌫",
    1063: "🌧🌧",
    1066: "❄❄",
    1069: "🌧🧊",
    1072: "🌨🌨",
    1087: "⛈⛈",
    1114: "🌬❄",
    1117: "🌨🌨🌨",
    1135: "🌁🌁🌁",
    1147: "❄🌁",
    1150: "🌧🌧",
    1153: "🌧",
    1168: "🥶🌧",
    1171: "🥶🌧🌧",
    1180: "🌧",
    1183: "🌧",
    1186: "🌧🌧",
    1189: "🌧🌧",
    1192: "🌧🌧🌧",
    1195: "🌧🌧🌧",
    1198: "🥶🌧",
    1201: "🥶🌧🌧",
    1204: "🌧🧊",
    1207: "🌧🧊🌧🧊",
    1210: "❄",
    1213: "❄",
    1216: "❄❄",
    1219: "❄❄",
    1222: "❄❄❄",
    1225: "❄",
    1237: "🧊",
    1240: "🌧",
    1243: "🌧🌧",
    1246: "🌧🌧🌧",
    1249: "🧊🌧",
    1252: "🧊🌧🌧",
    1255: "🌨",
    1258: "🌨🌨🌨",
    1261: "🧊",
    1264: "🧊🧊🧊",
    1273: "⛈",
    1276: "⛈⛈",
    1279: "❄⚡",
    128: "❄⚡❄⚡"
}


def joke():
    req = requests.get("https://official-joke-api.appspot.com/jokes/general/random")

    setup = req.json()[0].get("setup")
    punchline = req.json()[0].get("punchline")

    return setup, punchline


class Weather:
    def __init__(self, user: Athena.User):
        self.user = user

    def create_message(self):
        actual_time = time.strftime("%A. %B, %d %Y")
        formatted_time = rf"{actual_time}\n\n"
        message = rf"Hello {self.user.name}.\nToday is {formatted_time}"

        zipcode = self.user.weather_info["zipcode"]
        request = requests.get(f'http://api.weatherapi.com/v1/forecast.json',
                               {"key": "016e19390dba4ad5807184556222205", "q": zipcode, "days": 1,
                                "aqi": "no", "alert": "yes"})

        content = request.json()

        current_weather = content.get("current", False)

        try:
            forecast_day = content.get("forecast", {}).get("forecastday", ())[0]["day"]
        except IndexError as e:
            forecast_day = False

        if current_weather != False:
            message += rf"It currently Feels Like: {current_weather['feelslike_f']} ℉\n"

            if forecast_day != False:
                message += rf"Overall Forecast: {forecast_day['condition']['text']} {icons[forecast_day['condition']['code']]}\n\n"
            else:
                funny_joke = joke()
                message += fr"Sadly we couldn't retrieve the overal forecast for today. :(\n\nHere is a joke in the \
                meantime.\n{funny_joke[0]}\n{funny_joke[1]}\n\n"

        else:
            funny_joke = joke()
            message += fr"Sadly we couldn't retrieve the weather for today. :(\n\nHere is a joke in the meantime.\n" \
                       fr"\n{funny_joke[0]}\n{funny_joke[1]}\n\n"

        self.user.message = message


class News:
    def __init__(self, user):
        self.user = user

    def create_message(self):
        news = gnews.GNews(max_results=5)

        self.user.message = r"Top Headlines\n\n"

        latest = news.get_top_news()

        for article in latest:
            self.user.message += rf"{article['title']}\n\n"

    def add_message(self):
        news = gnews.GNews(max_results=5)

        self.user.message += r"Top Headlines\n\n"

        latest = news.get_top_news()

        for article in latest:
            self.user.message += rf"{article['title']}\n\n"
