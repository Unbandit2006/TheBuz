from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import requests
import time
import os

if __name__ == "__main__":
    os.chdir("Buzzers/Weather")

# Day or night file associations
file_assc = {
    1000: ["Images/Sunny_TimTrad.jpg", "Images/Clear_KenCheung.jpg"], # Sunny/Clear
    1003: ["Images/PartlyCloudy_JohanRydberg.jpg", "Images/PartlyCloudy_AnanduVinod.jpg"], # Partly Cloudy
    1006: ["Images/Cloudy_ArtemAnokhin.jpg", "Images/Cloudy_JasonBlackeye.jpg"], # Cloudy
    1009: ["Images/Overcast_WilliamBout.jpg", "Images/Overcast_JJJordan.jpg"], # Overcast
    1030: ["Images/Mist_SimonBerger.jpg", "Images/Mist_ArtemKovalev.jpgz"], # Mist
    1063: ["Images/PatchyRain_KevinErdvig.jpg", "Images/PatchyRain_ToddDiemer.jpg"], # Patchy rain possible
    1066: ["Images/PatchySnow_MarcKleen.jpg", "Images/PatchySnow_OsmanRana.jpg"], # Patchy snow possible
    1069: ["Images/", "Images/"], # Patchy sleet possible
    1072: ["Images/", "Images/"], # Patchy freezing drizzle possible
    1187: ["Images/", "Images/"], # Thundery outbreaks possible
    1114: ["Images/", "Images/"], # Blowing snow
    1117: ["Images/", "Images/"], # Blizzard
    1135: ["Images/", "Images/"], # Fog
    1147: ["Images/", "Images/"], # Freezing fog
    1150: ["Images/", "Images/"], # Patchy light drizzle
    1153: ["Images/", "Images/"], # Light drizzle
    1168: ["Images/", "Images/"], # Freezing drizzle
    1171: ["Images/", "Images/"], # Heavy freezing drizzle
    1180: ["Images/", "Images/"], # Patchy light rain
    1183: ["Images/", "Images/"], # Light rain
    1186: ["Images/", "Images/"], # Moderate rain at times
    1189: ["Images/", "Images/"], # Moderate rain
    1192: ["Images/", "Images/"], # Heavy rain at times
    1905: ["Images/", "Images/"], # Heavy rain
    1198: ["Images/", "Images/"], # Light freezing rain
    1201: ["Images/", "Images/"], # Moderate or heavy freezing rain
    1204: ["Images/", "Images/"], # Light sleet
    1207: ["Images/", "Images/"], # Moderate or heavy sleet
    1210: ["Images/", "Images/"], # Patchy light snow
    1213: ["Images/", "Images/"], # Light snow
    1216: ["Images/", "Images/"], # Patchy moderate snow
    1219: ["Images/", "Images/"], # Moderate snow
    1222: ["Images/", "Images/"], # Patchy heavy snow
    1225: ["Images/", "Images/"], # Heavy snow
    1237: ["Images/", "Images/"], # Ice pellets
    1240: ["Images/", "Images/"], # Light rain shower
    1243: ["Images/", "Images/"], # Moderate or heavy rain shower
    1246: ["Images/", "Images/"], # Torrential rain shower
    1249: ["Images/", "Images/"], # Light sleet showers
    1252: ["Images/", "Images/"], # Moderate or heavy sleet showers
    1255: ["Images/", "Images/"], # Light snow showers
    1258: ["Images/", "Images/"], # Moderate or heavy snow showers
    1261: ["Images/", "Images/"], # Light showers of ice pellets
    1264: ["Images/", "Images/"], # Moderate or heavy showers of ice pellets
    1273: ["Images/", "Images/"], # Patchy light rain with thunder
    1276: ["Images/", "Images/"], # Moderate or heavy rain with thunder
    1279: ["Images/", "Images/"], # Patchy light snow with thunder
    1282: ["Images/", "Images/"], # Moderate or heavy snow with thunder
}

def main_image(data):
    # Collect daily & next hour weather
    weather_request = requests.get("http://api.weatherapi.com/v1/forecast.json", {"key":"016e19390dba4ad5807184556222205", "q":{data}, "days":1, "aqi":"no", "alerts":"no"})
    name = weather_request.json().get("location").get("name")
    region = weather_request.json().get("location").get("region")
    day_of_the_week = time.strftime("%A")
    day = time.strftime("%B %d, %Y")

    is_sun_up = bool(weather_request.json().get("forecast").get("forecastday")[0].get("astro").get("is_sun_up"))

    min_temp_c = weather_request.json().get("forecast").get("forecastday")[0].get("day").get("mintemp_c")
    min_temp_f = weather_request.json().get("forecast").get("forecastday")[0].get("day").get("mintemp_f")

    avg_temp_c = weather_request.json().get("forecast").get("forecastday")[0].get("day").get("avgtemp_c")
    avg_temp_f = weather_request.json().get("forecast").get("forecastday")[0].get("day").get("avgtemp_f")

    max_temp_c = weather_request.json().get("forecast").get("forecastday")[0].get("day").get("maxtemp_c")
    max_temp_f = weather_request.json().get("forecast").get("forecastday")[0].get("day").get("maxtemp_f")

    will_it_snow = [bool(weather_request.json().get("forecast").get("forecastday")[0].get("day").get("daily_will_it_snow"))]
    if will_it_snow[0] == True:
        will_it_snow.append(weather_request.json().get("forecast").get("forecastday")[0].get("day").get("daily_chance_it_snow"))

    will_it_rain = [bool(weather_request.json().get("forecast").get("forecastday")[0].get("day").get("daily_will_it_rain"))]
    if will_it_rain[0] == True:
        will_it_rain.append(weather_request.json().get("forecast").get("forecastday")[0].get("day").get("daily_chance_it_rain"))

    current_code = weather_request.json().get("current").get("condition").get("code")
    current_forecast = weather_request.json().get("current").get("condition").get("text")
    current_feels_like_f = weather_request.json().get("current").get("feelslike_f")
    current_feels_like_c = weather_request.json().get("current").get("feelslike_c")
    current_actual_f = weather_request.json().get("current").get("temp_f")
    current_actual_c = weather_request.json().get("current").get("temp_c")

    overall_forecast = weather_request.json().get("forecast").get("forecastday")[0].get("day").get("condition").get("text")

    # Image Generation
    image_path = file_assc.get(current_code, "DefaultImage")[is_sun_up]
    if image_path == "DefaultImage" or image_path == "Image/":
        image = Image.new("RGB", (4987, 3283), (14, 15, 14))
    else:
        image = Image.open(open(image_path, "rb"))

    extra_big_font = ImageFont.truetype("Assets/FiraSans-Bold.ttf", 600)

    big_font = ImageFont.truetype("Assets/FiraSans-Bold.ttf", 350)
    big_font_info = big_font.getmetrics()
    big_font_height = big_font_info[0] + big_font_info[1]

    small_font = ImageFont.truetype("Assets/FiraSans-Bold.ttf", 200)
    small_font_info = small_font.getmetrics()
    small_font_height = small_font_info[0] + small_font_info[1]

    medium_font = ImageFont.truetype("Assets/FiraSans-Bold.ttf", 200)
    medium_font_info = medium_font.getmetrics()
    medium_font_height = medium_font_info[0] + medium_font_info[1]

    if is_sun_up == True:
        default_color = (255, 255, 255)
    else:
        default_color = (0, 0, 0)

    image_draw = ImageDraw.Draw(image)

    line_start = image.width/2-image_draw.textlength( f"{name}, {region}", big_font)/2
    line_end = image.width/2+image_draw.textlength( f"{name}, {region}", big_font)/2

    image_draw.text((line_start, 0), f"{name}, {region}", default_color, big_font)
    image_draw.text((line_start, big_font_height), day_of_the_week, default_color, small_font)
    image_draw.text((line_start, big_font_height+small_font_height), day, default_color, small_font)

    image_draw.text((line_start, big_font_height+small_font_height+small_font_height+180), "Feels like:", default_color, medium_font)
    image_draw.text((line_start, big_font_height+small_font_height+small_font_height+100+medium_font_height), str(int(current_feels_like_f)), default_color, extra_big_font)
    image_draw.text((line_start+image_draw.textlength(str(int(current_feels_like_f)), extra_big_font)+60, big_font_height+small_font_height+small_font_height+210+medium_font_height), "°F", default_color, medium_font)
    image_draw.text((line_start, big_font_height+small_font_height+small_font_height+180+medium_font_height+80+medium_font_height+80+medium_font_height+80), f"Current forecast:\n{current_forecast}", default_color, medium_font)

    draw_string = f"Current: {current_actual_f} °F"
    image_draw.text((line_end-image_draw.textlength(draw_string, medium_font), big_font_height+small_font_height+small_font_height+180), draw_string, default_color, medium_font)
    current_x = line_end-image_draw.textlength(draw_string, medium_font)

    draw_string = f"Max: {max_temp_f} °F"
    image_draw.text((current_x, big_font_height+small_font_height+small_font_height+180+medium_font_height+80), draw_string, default_color, medium_font)

    draw_string = f"Min: {min_temp_f} °F"
    image_draw.text((current_x, big_font_height+small_font_height+small_font_height+180+medium_font_height+80+medium_font_height+80), draw_string, default_color, medium_font)

    draw_string = f"Overall forecast:\n{overall_forecast}"
    image_draw.text((current_x, big_font_height+small_font_height+small_font_height+180+medium_font_height+80+medium_font_height+80+medium_font_height+80), draw_string, default_color, medium_font)

    image.save("temp.jpg")

    return 'temp.jpg'

def main_text(data):
    pass

#Image.open(main_image(10306)).show()
