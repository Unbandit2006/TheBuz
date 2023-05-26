import Buzzers.Weather as weather
from PIL import Image, ImageDraw, ImageFont

current_weather = weather.get_raw_data("10306")

with Image.open("images\\partly-cloudy.jpg").convert("RGBA") as background:

    txt = Image.new("RGBA", background.size, (255,255,255, 0))

    small_font = ImageFont.truetype("FiraSans-Medium.ttf", 150)
    font = ImageFont.truetype("FiraSans-Medium.ttf", 300)
    big_font = ImageFont.truetype("FiraSans-Medium.ttf", 400)
    bigger_font = ImageFont.truetype("FiraSans-Medium.ttf", 700)

    drawn_text = ImageDraw.Draw(txt)

    f = "°F"

    x = txt.width//2 - big_font.getlength(current_weather.get("Location"))//2
    drawn_text.text((x, 50), text=str(current_weather.get("Location")), font=big_font, fill=(0,0,0,255))
    drawn_text.text((x+25, 450), f"Monday", font=small_font, fill=(0,0,0,255))
    drawn_text.text((x+25, 590), f"May 14, 2023", font=small_font, fill=(0,0,0,255))
    
    drawn_text.text((x, 1000), text="Feels like", font=font, fill=(0,0,0,255))
    drawn_text.text((x, 1300), text=str(int(current_weather.get("CurrentFeelsLikeF"))), font=bigger_font, fill=(0,0,0,255))
    drawn_text.text((x+bigger_font.getlength(str(int(current_weather.get("CurrentFeelsLikeF"))))+30, 1410), f, font=font, fill=(0,0,0,255), )

    drawn_text.text((x+bigger_font.getlength(str(int(current_weather.get("CurrentFeelsLikeF"))))+1600,970), f"Current: {str(int(current_weather.get('CurrentTemp')))} {f}", font=font, fill=(0,0,0,255))
    drawn_text.text((x+bigger_font.getlength(str(int(current_weather.get("CurrentFeelsLikeF"))))+1600,1290), f"Max: {str(int(current_weather.get('Max')))} {f}", font=font, fill=(0,0,0,255))
    drawn_text.text((x+bigger_font.getlength(str(int(current_weather.get("CurrentFeelsLikeF"))))+1600,1610), f"Min: {str(int(current_weather.get('Min')))} {f}", font=font, fill=(0,0,0,255))
    drawn_text.text((x+bigger_font.getlength(str(int(current_weather.get("CurrentFeelsLikeF"))))+1600,1930), "Overall Forecast:", font=font, fill=(0,0,0,255))
    drawn_text.text((x+bigger_font.getlength(str(int(current_weather.get("CurrentFeelsLikeF"))))+1600,2250), f"{str(current_weather.get('CurrentCondition'))}", font=font, fill=(0,0,0,255))
    
    background = Image.alpha_composite(background, txt)

    background.save("C://Users//Danie//Desktop//myImage.png")

