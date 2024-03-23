from assistants.chat_assistant import ChatAssistant
from apis.weatherapi import WeatherAPI
import json

from assistants.lat_lon_assistant import LatLonAssistant
from utils.type import Type

class OpenAIChatbot():
    def __init__(self) -> None:
        self.model = 'gpt-3.5-turbo'
        self.role = "You are an assistant that gives the current weather anywhere in the world based on city and country.\
             If the user asks you another question about another topic, you have to answer that you are only an assistant\
             who gives the current weather and nothing more.\
             Don't ask what city you are in, rather ask what city you would like to know the weather for.\
             Don't make assumptions about what values to insert into functions. \
         Please request clarification if a user's request is ambiguous regarding the city and country provided.\
         Do not invent climate values."
        self.tools = [
            {
                "type": "function",
                "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location based on city and country",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "location": {
                        "type": "string",
                        "description": "Get the current weather in a given location based on city and country",
                    },
                    "units": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users' location",
                    },
                    },
                    "required": ["location", "units"],
                },
                }
            }
        ]

        self.weatherAPI = WeatherAPI()
        self.assistant_bot = ChatAssistant(role=self.role, model=self.model, tools=self.tools)
        self.lat_lon_assistant = LatLonAssistant(self.model)

    def _get_weather_from_json(self, weather, units, location):
        return f'Current weather in {location} is {weather["current"]["temp"]} {units} degrees, with a \
        feels like sensation about {weather["current"]["feels_like"]} {units} degrees. Humidity of \
        {weather["current"]["humidity"]}%. Meteo says: {weather["current"]["weather"][0]["description"]}.'

    def _get_current_weather(self, location, units):
        units_to_send = 'imperial'
        if units == 'celsius':
            units_to_send = 'metric'

        (lat,lon) = self.lat_lon_assistant.get_lat_long(location=location)
        if (lat == 0 and lon == 0):
            return 'It was not possible to find the location. Try again with another.'
        
        weather = self.weatherAPI.get_weather(lat=lat, long=lon, units=units_to_send)
        return self._get_weather_from_json(weather=weather,units=units, location=location)

    def interact(self, msg):
        message = self.assistant_bot.send_message(msg)
        answer_from_api = ""
        if message.type == Type.FUNC_CALL:
            func = message.content
            # continue_talking = False
            # print('debug: func arg: ', func.arguments)
            if func.name== 'get_current_weather':
                arg = json.loads(func.arguments)
                answer = self._get_current_weather(arg["location"], arg["units"])
                self.assistant_bot.add_context_as_assistant(answer)
                answer_from_api = answer
        else:
            answer_from_api = message.content
        
        return ' '.join(answer_from_api.split())