from datetime import datetime
from aiogram import types
from Settings import Settings
import logging

class Keyboard:
    def __init__(self, settings: Settings):
        logging.info("Start initing Settings")
        self.settings = settings
                
        # KEYBOARD_SUBMAIN
        self.keyboard_submain = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard_submain.add(types.KeyboardButton(text="Binance info"), types.KeyboardButton(text="Living time"))
        self.keyboard_submain.add(types.KeyboardButton(text="Кулькулятор"), types.KeyboardButton(text="Погода"))
        self.keyboard_submain.add(types.KeyboardButton(text="Отправить"), types.KeyboardButton(text="Настройки"))
        self.keyboard_submain.add(types.KeyboardButton(text="Main"))

        # KEYBOARD WORK
        self.keyboard_work = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard_work.add(types.KeyboardButton(text="Last week worked time"), types.KeyboardButton(text="Worked time"))
        self.keyboard_work.add(types.KeyboardButton(text="Last week worked time (details)"), types.KeyboardButton(text="Worked time (details)"))
        self.keyboard_work.add(types.KeyboardButton(text="Main"))

        # KEYBOARD WORK TAG
        self.keyboard_work_tag = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard_work_tag.add(types.KeyboardButton(text="#reading"), types.KeyboardButton(text="#coding"), types.KeyboardButton(text="#listening"))
        self.keyboard_work_tag.add(types.KeyboardButton(text="#reporting"), types.KeyboardButton(text="#testing"), types.KeyboardButton(text="Main"))

        # KEYBOARD_BIN
        self.keyboard_bin = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard_bin.add(types.KeyboardButton(text="1"), types.KeyboardButton(text="0"))
        self.keyboard_bin.add(types.KeyboardButton(text="Main"))

        # KEYBOARD_CITIES
        cities_history = self.settings.cities_history
        self.keyboard_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.create_keyboard_cities()

        # KEYBOARD_BINANCE
        binance_val_list = self.settings.binance_val_list
        self.keyboard_binance = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.create_keyboard_binance()

        # KEYBOARD_SETTINGS
        self.keyboard_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
        set_keys = [*self.settings.settings_info.keys()]
        for k in range(len(set_keys)//2):
            self.keyboard_settings.add(types.KeyboardButton(text=set_keys[k*2]), types.KeyboardButton(text=set_keys[k*2 + 1]))
        if (len(set_keys) % 2 != 0): 
            self.keyboard_settings.add(types.KeyboardButton(text=set_keys[-1]), types.KeyboardButton(text="Main"))
        else:
            self.keyboard_settings.add(types.KeyboardButton(text="Main"))

        logging.info("End initing Settings")

    def create_keyboard_cities(self):
        logging.info("Start create_keyboard_cities()")
        cities_history = self.settings.cities_history
        self.keyboard_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for k in range(len(cities_history)//2):
            self.keyboard_cities.add(types.KeyboardButton(text=cities_history[k*2]), types.KeyboardButton(text=cities_history[k*2 + 1]))
        if len(cities_history) % 2 != 0: self.keyboard_cities.add(types.KeyboardButton(text=cities_history[-1]))

        self.keyboard_cities.add(types.KeyboardButton(text="Main"))
        logging.info("End create_keyboard_cities()")

    def create_keyboard_binance(self):
        logging.info("Start create_keyboard_binance()")
        binance_val_list = self.settings.binance_val_list
        self.keyboard_binance = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for k in range(len(binance_val_list)//2):
            self.keyboard_binance.add(types.KeyboardButton(text=binance_val_list[k*2]), types.KeyboardButton(text=binance_val_list[k*2 + 1]))
        if len(binance_val_list) % 2 != 0: self.keyboard_binance.add(types.KeyboardButton(text=binance_val_list[-1]))

        self.keyboard_binance.add(types.KeyboardButton(text="Main"))
        logging.info("End create_keyboard_binance()")

    def get_main(self, s, w, t, u_id):
        keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_main.add(types.KeyboardButton(text="Tag: %s" % t), types.KeyboardButton(text=s))
        keyboard_main.add(types.KeyboardButton(text="Work reports"), types.KeyboardButton(text=w))

        return keyboard_main
    
    def get_submain(self):
        return self.keyboard_submain
    
    def get_work(self):
        return self.keyboard_work
    
    def get_work_tag(self, work):
        if work.u_tag_db.get_count_of_history(work.user_id) == 0:
            for k in ["#reading", "#coding", "#listening", "#reporting", "#testing"]:
                work.u_tag_db.add_row(work.user_id, k, datetime.now())
        
        tags = work.u_tag_db.get_user_tag_history(work.user_id)
        keyboard_work_tag = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_work_tag.add(types.KeyboardButton(text=tags[0]), types.KeyboardButton(text=tags[1]), types.KeyboardButton(text=tags[2]))
        keyboard_work_tag.add(types.KeyboardButton(text=tags[3]), types.KeyboardButton(text=tags[4]), types.KeyboardButton(text="Main"))
        return keyboard_work_tag

    def get_bin(self):
        return self.keyboard_bin

    def get_cities(self):
        return self.keyboard_cities

    def get_binance(self):
        return self.keyboard_binance

    def get_settings(self):
        return self.keyboard_settings
    