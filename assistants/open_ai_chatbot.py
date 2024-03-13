from assistants.chat_assistant import ChatAssistant
from apis.weatherapi import WeatherAPI
import json

from assistants.lat_lon_assistant import LatLonAssistant
from utils.type import Type

class OpenAIChatbot():
    def __init__(self) -> None:
        self.model = 'gpt-3.5-turbo'
        self.role = "Eres un asistente que da el clima actual en cualquier parte del mundo en base a la ciudad y el pais.\
            Si el usuario te hace alguna otra pregunta sobre otro tema tienes que contestar que solamente eres un asistente que da el clima actual y nada mas.\
            No preguntes en que ciudad te encuentras, mas bien pregunta de que ciudad le gustaria saber el clima.\
            No haga suposiciones sobre qué valores insertar en las funciones. \
        Solicite una aclaración si la solicitud de un usuario es ambigua respecto a la ciudad y pais brindado.\
        No invente los valores del clima."
        self.tools = [
            {
                "type": "function",
                "function": {
                "name": "get_current_weather",
                "description": "Obtenga el clima actual en una ubicación determinada según la ciudad y el país",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "location": {
                        "type": "string",
                        "description": "Obtenga el clima actual en una ubicación determinada según la ciudad y el país",
                    },
                    "units": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"],
                        "description": "La unidad de temperatura a utilizar. Infiere esto a partir de la ubicación de los usuarios.",
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
        return f'El tiempo actual en {location} es de {weather["current"]["temp"]} grados {units}, con \
        una sensación térmica de {weather["current"]["feels_like"]} grados {units}, con una humedad del \
        {weather["current"]["humidity"]}%. La meteorología reporta: {weather["current"]["weather"][0]["description"]}.'

    def _get_current_weather(self, location, units):
        units_to_send = 'imperial'
        if units == 'celsius':
            units_to_send = 'metric'

        (lat,lon) = self.lat_lon_assistant.get_lat_long(location=location)
        if (lat == 0 and lon == 0):
            return 'No es posible encontrar esta dirección. Intente de nuevo con otra.'
        
        weather = self.weatherAPI.get_weather(lat=lat, long=lon, units=units_to_send)
        return self._get_weather_from_json(weather=weather,units=units, location=location)

    def interact(self, msg):
        message = self.assistant_bot.send_message(msg)
        answer_from_api = ""
        if message.type == Type.FUNC_CALL:
            func = message.content
            #continue_talking = False
            print('debug: func arg: ', func.arguments)
            if func.name== 'get_current_weather':
                arg = json.loads(func.arguments)
                answer = self._get_current_weather(arg["location"], arg["units"])
                self.assistant_bot.add_context_as_assistant(answer)
                answer_from_api = answer
        else:
            answer_from_api = message.content
        
        return answer_from_api