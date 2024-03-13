import os
import requests

class WeatherAPI():
    def __init__(self) -> None:
        self.api_key = os.environ["OPEN_WEATHER_KEY"]
        self.url = "http://api.openweathermap.org/data/3.0/onecall"
    
    def get_weather(self, lat, long, units):
        url = f"{self.url}?lat={lat}&lon={long}&exclude=minutely,daily&units={units}&appid={self.api_key}"
        req = requests.get(url)
        
        return req.json()