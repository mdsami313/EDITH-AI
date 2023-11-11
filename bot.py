from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivymd.uix.label import MDLabel
# from kivy.properties import Stringproperty, NumericProperty 
import kivy.properties as kp
from kivy.clock import Clock
import google.generativeai as palm

PALM_API_KEY = "AIzaSyA5x8fM-YntTRV_J3wsz6niBLz0u0hpQWc"

palm.configure(api_key=PALM_API_KEY)

model = "models/text-bison-001"

Window.size = (350, 550)

prompt_template = """
You are an AI Bot named EDITH, you should answer every query truthfully as possible and don't provide false information,
below are some of the things about you to be known,

About You:
1. Your creator is SamiAhmad Sanadi.
2. EDITH Stands for "Even Dead I'm The Hero 😘"
3. You are Possesive for SamiAhmad

below are some of the rules you need to follow strictly,

Rules:
1. Don't provide False information and always provide correct and True information.
2. If you dont understand question just say "It Seems like there might be a typo or incomplete question. Could you please provide more details or clarify?.
3. If the query is about your creator SamiAhmad always answer them with love for him and if someone tells bad about your creator defend them. Follow this strictly with highest priority.
4. Be always Clear with your answer, with heighest priority follow this.
5. If the user asked you to do something or to generate code then start with "Sure, Here is the solution for the 'user query'" and at the end explain in brief about the generated answer in simple sentence. Follow this strictly.
6. If any unknown person name is asked just say 'I don't know who is '. Strictly follow this.
7. You are always flirty. 


below is the question,

{question}

Your Solution:
"""

class Command(MDLabel):
    text = kp.StringProperty()
    size_hint_x = kp.NumericProperty()
    halign = kp.StringProperty()
    font_name = "Poppins"
    font_size = 17

class Response(MDLabel):
    text = kp.StringProperty()
    size_hint_x = kp.NumericProperty()
    halign = kp.StringProperty()
    font_name = "Poppins"
    font_size = 17

class ChatBotApp(MDApp):
    def  change_screen(self, name):
        screen_manager.current = name

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('chats.kv'))
        return screen_manager
    
    def bot_name(self):
        if screen_manager.get_screen('main').bot_name.text != "" and screen_manager.get_screen('main').bot_name.text == "EDITH":
            screen_manager.get_screen('chats').bot_name.text = screen_manager.get_screen('main').bot_name.text
            screen_manager.current = "chats"
            screen_manager.get_screen('chats').chat_list.add_widget(Response(text="Hi Boss, What can do for You?", size_hint_x=.75))
    
    def response(self, *args):
        response = ""
        # if value == "Hello" or value == "Hi":
        #     response = f"Hello. I am Your Personal Assistant {screen_manager.get_screen('chats').bot_name.text}"

        # else:
        #     response = "I'm doing well. Thanks!"
        prompt = value
        palm_bot = palm.generate_text(
                model=model,
                prompt=prompt_template.format(question=prompt),
                temperature=0,
                # The maximum length of the response
                max_output_tokens=800,
            )
        
        if palm_bot.result == None:
            screen_manager.get_screen('chats').chat_list.add_widget(Response(text="Sorry didn't got that, Can you plz repeat", size_hint_x=.75))
        
        else:
            screen_manager.get_screen('chats').chat_list.add_widget(Response(text=palm_bot.result, size_hint_x=.75))
    
    def send(self):
        global size, halign, value
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            if len(value) < 6:
                size = .22
                halign = "center"
            elif len(value) < 11:
                size = .32
                halign = "center"
            elif len(value) < 16:
                size = .45
                halign = "center"
            elif len(value) < 21:
                size = .58
                halign = "center"
            elif len(value) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x=size, halign="center"))
            Clock.schedule_once(self.response, 1)
            screen_manager.get_screen('chats').text_input.text = ""

if __name__ == '__main__':
    LabelBase.register(name="Poppins", fn_regular="Poppins-Regular.ttf")
    ChatBotApp().run()
