from assistants.chat_assistant import ChatAssistant
import json


class LatLonAssistant():
    def __init__(self, model) -> None:
        self.model = model

    def get_lat_long(self, location: str):
        role = 'Vas a recibir una dirección y tu funcion es \
                devolver las coordenadas terrestres de esta dirección: la latitud y longitud de \
                dicha ciudad/pais en formato json.  \
                Por ejemplo si recibes: cochabamba, bolivia deberías retornar: \
                {\
                "latitude": -17.3895,\
                "longitude": -66.1568\
                }\
                \
                No aumentar ninguna información extra\
                en caso de que no conozcas dichas coordenadas puedes retornar un json como este:\
                {\
                "latitude": 0,\
                "longitude": 0\
                }\
        '
        assistant_lat_long = ChatAssistant(role=role, model=self.model)
        lat_lon = json.loads(assistant_lat_long.send_message_wo_func_exec(f"dirección: {location}"))

        return (lat_lon['latitude'], lat_lon['longitude'])
