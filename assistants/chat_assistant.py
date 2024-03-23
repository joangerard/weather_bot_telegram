from openai import OpenAI
from utils.message_type import MessageType
from utils.type import Type

class ChatAssistant():
    def __init__(self, role, model, tools=[]):
        self.client = OpenAI()
        self.messages = []
        self.tools = tools
        self.max_tokens = 180
        self.temperature = 0.2
        self._set_role(role)
        self._set_model(model)
    
    def _set_model(self, model):
        self.model = model

    def _set_role(self, role):
        self.messages = []
        self.messages.append({
            "role": "system", 
            "content": role
        })
        
    def _answer(self, choice) -> MessageType:
        if choice.finish_reason == 'tool_calls':
            function_to_call = choice.message.tool_calls[0].function
            return MessageType(type=Type.FUNC_CALL, content=function_to_call)
        else:
            assistant_message = choice.message
            self.messages.append(assistant_message)
            return MessageType(type=Type.MESSAGE, content=assistant_message.content)
    
    def send_message(self, message) -> MessageType:
        self.messages.append({
            "role":"user", 
            "content": message
        })

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            tools=self.tools
        )

        # print('debug: finish_reason', completion.choices[0].finish_reason)

        return self._answer(completion.choices[0])
    
    def add_context_as_assistant(self, message):
        self.messages.append({
            "role":"assistant", 
            "content": message
        })

    def send_message_wo_func_exec(self, message) -> MessageType:
        self.messages.append({
            "role":"user", 
            "content": message
        })

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        assitant_message = completion.choices[0].message
        self.messages.append(assitant_message)
        return assitant_message.content

