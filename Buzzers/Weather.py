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


def add_to_message(zipcode):
    req = requests.get("https://api.weatherapi.com/v1/forecast.json", params={"key":"016e19390dba4ad5807184556222205", "q":f"{zipcode}","aqi":"no", "alerts":"no"})

    text = req.json()

    current_feelslike_f = text.get("current").get("feelslike_f")
    current_condition = text.get("current").get("condition").get("text")
    current_code = text.get("current").get("condition").get("code")
    current_icon = icons[current_code]

    percent_snow = text.get("forecast").get("forecastday")[0]["day"]["daily_chance_of_snow"]
    percent_rain = text.get("forecast").get("forecastday")[0]["day"]["daily_chance_of_rain"]
    daily_min = text.get("forecast").get("forecastday")[0]["day"]["mintemp_f"]
    daily_max = text.get("forecast").get("forecastday")[0]["day"]["maxtemp_f"]

    message = rf"It currently feels like {current_feelslike_f} ℉.\n"\
                rf"Overall forecast: {current_condition} {current_icon}\n"\
                rf"Min. temperature: {daily_min} ℉\n"\
                rf"Max. temperature: {daily_max} ℉\n\n"

    return message
