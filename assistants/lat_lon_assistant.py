from assistants.chat_assistant import ChatAssistant
import json


class LatLonAssistant():
    def __init__(self, model) -> None:
        self.model = model

    def get_lat_long(self, location: str):
        role = 'You are going to receive an address and your function is \
                return the earth coordinates of this address: the latitude and longitude of \
                said city/country in json format. \
                For example if you receive: cochabamba, bolivia you should return: \
                {\
                "latitude": -17.3895,\
                "longitude": -66.1568\
                }\
                \
                Do not add any extra information\
                In case you don\'t know these coordinates, you can return a json like this:\
                {\
                "latitude": 0,\
                "longitude": 0\
                }\
        '
        assistant_lat_long = ChatAssistant(role=role, model=self.model)
        lat_lon = json.loads(assistant_lat_long.send_message_wo_func_exec(f"dirección: {location}"))

        return (lat_lon['latitude'], lat_lon['longitude'])
