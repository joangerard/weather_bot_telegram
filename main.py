from assistants.open_ai_chatbot import OpenAIChatbot

open_ai_chatbot = OpenAIChatbot()

while True:
    msg = input()
    print(open_ai_chatbot.interact(msg))
    