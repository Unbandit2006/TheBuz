import requests

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

images = {
    1000: "sunny.png"
}

def add_to_message(zipcode):
    req = requests.get("https://api.weatherapi.com/v1/forecast.json", params={"key":"016e19390dba4ad5807184556222205", "q":f"{zipcode}","aqi":"no", "alerts":"no"})

    text = req.json()

    currentFeelsLikeF = text.get("current").get("feelslike_f")
    currentCondition = text.get("current").get("condition").get("text")
    currentTemp = text.get("current").get("temp_f")
    currentCode = text.get("current").get("condition").get("code")
    currentIcon = icons[currentCode]

    percentSnow = text.get("forecast").get("forecastday")[0]["day"]["daily_chance_of_snow"]
    percentRain = text.get("forecast").get("forecastday")[0]["day"]["daily_chance_of_rain"]
    dailyMin = text.get("forecast").get("forecastday")[0]["day"]["mintemp_f"]
    dailyMax = text.get("forecast").get("forecastday")[0]["day"]["maxtemp_f"]

    message = rf"It currently feels like {currentFeelsLikeF} ℉.<br>"\
                f"Current temperature: {currentTemp} ℉<br>"\
                f"Overall forecast: {currentCondition} {currentIcon}<br>"\
                f"Max. temperature: {dailyMax} ℉<br>"\
                f"Min. temperature: {dailyMin} ℉<br>"

    if int(percentSnow) != 0:
        message += rf"There is a {percentSnow}% chance of snow.<br>Don't forget to dress warm<br><br>"

    if int(percentRain) != 0:
        message += rf"There is a {percentRain}% chance of rain.<br>Don't forget to take your umbrella ☂☂<br><br>"

    return message

def get_raw_data(zipcode: str):
    req = requests.get("https://api.weatherapi.com/v1/forecast.json", params={"key":"016e19390dba4ad5807184556222205", "q":f"{zipcode}","aqi":"no", "alerts":"no"})

    text = req.json()

    location =  text.get("location").get("name") + ", "+ text.get("location").get("region")

    currentFeelsLikeF = text.get("current").get("feelslike_f")
    currentCondition = text.get("current").get("condition").get("text")
    currentTemp = text.get("current").get("temp_f")
    currentCode = text.get("current").get("condition").get("code")
    currentIcon = text.get("current").get("condition").get("icon")

    percentSnow = text.get("forecast").get("forecastday")[0]["day"]["daily_chance_of_snow"]
    percentRain = text.get("forecast").get("forecastday")[0]["day"]["daily_chance_of_rain"]
    dailyMin = text.get("forecast").get("forecastday")[0]["day"]["mintemp_f"]
    dailyMax = text.get("forecast").get("forecastday")[0]["day"]["maxtemp_f"]

    message = {"Location": location, "CurrentFeelsLikeF": currentFeelsLikeF, "CurrentCondition": currentCondition, "CurrentTemp": currentTemp,
               "CurrentCode": currentCode, "CurrentIcon": icons[currentCode], "Min": dailyMin, "Max": dailyMax}

    if int(percentSnow) != 0:
        message["Snow"] = percentSnow

    if int(percentRain) != 0:
        message["Rain"] = percentRain

    return message

