#!/usr/bin/env python3
"""
WNC Trail Weather Check
Uses Open-Meteo (open-meteo.com) — free, no API key required.
"""

import json
import urllib.request
from datetime import datetime, timedelta

LOCATIONS = [
    {"name": "Brevard, NC",     "lat": 35.2337, "lon": -82.7343},
    {"name": "Asheville, NC",   "lat": 35.5951, "lon": -82.5515},
    {"name": "Bryson City, NC", "lat": 35.4279, "lon": -83.4488},
    {"name": "Waynesville, NC", "lat": 35.4890, "lon": -82.9874},
]

WMO_CODES = {
    0:  "Clear sky",          1:  "Mainly clear",       2:  "Partly cloudy",
    3:  "Overcast",           45: "Fog",                48: "Rime fog",
    51: "Light drizzle",      53: "Drizzle",            55: "Dense drizzle",
    61: "Light rain",         63: "Rain",               65: "Heavy rain",
    71: "Light snow",         73: "Snow",               75: "Heavy snow",
    77: "Snow grains",        80: "Light showers",      81: "Showers",
    82: "Heavy showers",      85: "Snow showers",       86: "Heavy snow showers",
    95: "Thunderstorm",       96: "Thunderstorm w/ hail", 99: "Thunderstorm w/ heavy hail",
}


def degrees_to_cardinal(deg):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(deg / 45) % 8]


def fetch_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,relative_humidity_2m,uv_index"
        "&daily=temperature_2m_min,temperature_2m_max"
        "&hourly=precipitation"
        "&temperature_unit=fahrenheit"
        "&precipitation_unit=inch"
        "&wind_speed_unit=mph"
        "&timezone=America%2FNew_York"
        "&past_days=1"
        "&forecast_days=2"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read())


def last_24h_rain(data):
    now = datetime.now()
    cutoff = now - timedelta(hours=24)
    total = 0.0
    for t, p in zip(data["hourly"]["time"], data["hourly"]["precipitation"]):
        dt = datetime.fromisoformat(t)
        if cutoff <= dt <= now and p:
            total += p
    return round(total, 2)


def daily_index(data, date_str):
    try:
        return data["daily"]["time"].index(date_str)
    except ValueError:
        return None


def print_location(name, data):
    today_str    = datetime.now().strftime("%Y-%m-%d")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    ti = daily_index(data, today_str)
    tn = daily_index(data, tomorrow_str)

    if ti is None:
        print(f"\n  {name}: Could not locate today in forecast data.")
        return

    daily      = data["daily"]
    temp       = data["current"]["temperature_2m"]
    conditions = WMO_CODES.get(data["current"]["weather_code"], f"Code {data['current']['weather_code']}")
    wind_speed = data["current"]["wind_speed_10m"]
    wind_dir   = degrees_to_cardinal(data["current"]["wind_direction_10m"])
    humidity   = data["current"]["relative_humidity_2m"]
    uv         = data["current"]["uv_index"]
    today_high = daily["temperature_2m_max"][ti]

    # Tonight's low = tomorrow's daily min; fall back to today's if unavailable
    overnight_low = daily["temperature_2m_min"][tn] if tn is not None else daily["temperature_2m_min"][ti]

    rain_24h    = last_24h_rain(data)

    freeze_thaw = overnight_low < 32 and today_high > 35

    w = 44
    print(f"\n{'=' * w}")
    print(f"  {name}")
    print(f"{'=' * w}")
    print(f"  Current Temp:   {temp:.0f}°F")
    print(f"  Conditions:     {conditions}")
    print(f"  Wind:           {wind_speed:.0f} mph {wind_dir}")
    print(f"  Humidity:       {humidity:.0f}%")
    print(f"  UV Index:       {uv:.1f}")
    print(f"  Overnight Low:  {overnight_low:.0f}°F")
    print(f"  Rain (24h):     {rain_24h:.2f}\"")
    if freeze_thaw:
        print(f"  Freeze-Thaw:    YES  (high {today_high:.0f}° / low {overnight_low:.0f}°F)")
    else:
        print(f"  Freeze-Thaw:    No")


def main():
    print(f"\nWNC Weather — {datetime.now().strftime('%A, %B %d at %-I:%M %p')}")
    for loc in LOCATIONS:
        try:
            data = fetch_weather(loc["lat"], loc["lon"])
            print_location(loc["name"], data)
        except Exception as e:
            print(f"\n  Error fetching {loc['name']}: {e}")
    print()


if __name__ == "__main__":
    main()
