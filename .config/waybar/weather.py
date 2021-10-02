#!/usr/bin/env python3

import json
import requests
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ICON_MAP = {
    "01d": " ",
    "02d": " ",
    "03d": " ",
    "04d": " ",
    "09d": "",
    "10d": "",
    "11d": "",
    "13d": "",
    "50d": "",
}


def main():
    apikey = os.getenv("WAYBAR_WEATHER_APIKEY")
    weather_lat = os.getenv("WAYBAR_WEATHER_LAT", "52.52")
    weather_lon = os.getenv("WAYBAR_WEATHER_LON", "13.38")
    weather_units = os.getenv("WAYBAR_WEATHER_UNITS", "metric")
    weather_exclude = os.getenv("WAYBAR_WEATHER_EXCLUDE", "minutely,daily")

    data = {}
    try:
        weather = requests.get(
            "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={units}&exclude={exclude}&appid={apikey}".format(
                **{
                    "apikey": apikey,
                    "lat": weather_lat,
                    "lon": weather_lon,
                    "units": weather_units,
                    "exclude": weather_exclude,
                }
            )
        ).json()
    except Exception as e:
        return print({})

    if weather.get("cod"):
        data["text"] = "[weather] Error {}: {}".format(
            weather.get("cod"), weather.get("message")
        )
        data["class"] = "weather"
        print(json.dumps(data))
        # sys.exit(data["text"])
        sys.exit()

    temp = weather["current"]["temp"]
    icon = ICON_MAP.get(weather["current"]["weather"][0]["icon"], "")
    feels_like = weather["current"]["feels_like"]
    humidity = weather["current"]["humidity"]
    pressure = weather["current"]["pressure"]
    sunrise = datetime.fromtimestamp(
        weather["current"]["sunrise"], ZoneInfo(weather["timezone"])
    ).strftime("%H:%M")
    sunset = datetime.fromtimestamp(
        weather["current"]["sunset"], ZoneInfo(weather["timezone"])
    ).strftime("%H:%M")
    wind_speed = weather["current"]["wind_speed"]

    data["text"] = "{0} {1}°C".format(icon, temp)
    data[
        "tooltip"
    ] = """Feels like {0}°C
Pressure {1}
Humidity {2}
Sunrise {3}
Sunset {4}
Wind speed {5}Km/h
    """.format(
        feels_like, pressure, humidity, sunrise, sunset, wind_speed
    )
    data["class"] = "weather"

    print(json.dumps(data))


if __name__ == "__main__":
    main()

