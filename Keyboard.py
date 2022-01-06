from aiogram import types
from Settings import Settings
import logging

class Keyboard:
    def __init__(self, settings: Settings):
        logging.info("Start initing Settings")
        self.settings = settings

        # KEYBOARD WORK
        self.keyboard_work = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard_work.add(types.KeyboardButton(text="Last week worked time"), types.KeyboardButton(text="Worked time"))
        self.keyboard_work.add(types.KeyboardButton(text="Last week worked time (details)"), types.KeyboardButton(text="Worked time (details)"))
        self.keyboard_work.add(types.KeyboardButton(text="Main"))

        # KEYBOARD WORK TAG
        self.keyboard_work_tag = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard_work_tag.add(types.KeyboardButton(text="#reading"), types.KeyboardButton(text="#coding"), types.KeyboardButton(text="#listening"))
        self.keyboard_work_tag.add(types.KeyboardButton(text="#reporting"), types.KeyboardButton(text="#testing"), types.KeyboardButton(text="Main"))
        
        logging.info("End initing Settings")


    def get_main(self, w):
        keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_main.add(types.KeyboardButton(text="Actions with periods"), types.KeyboardButton(text="Status/Tag"))
        keyboard_main.add(types.KeyboardButton(text="Work reports"), types.KeyboardButton(text=w))

        return keyboard_main
    