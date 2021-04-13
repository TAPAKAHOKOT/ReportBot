from aiogram import types

class Keyboard:
	def __init__(self, settings):
		self.settings = settings
		
		# KEYBOARD_MAIN
		self.keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
		self.keyboard_main.add(types.KeyboardButton(text="Настройки"), types.KeyboardButton(text="Отправить"))
		self.keyboard_main.add(types.KeyboardButton(text="Кулькулятор"), types.KeyboardButton(text="Погода"))
		self.keyboard_main.add(types.KeyboardButton(text="Living time"), types.KeyboardButton(text="Binance Info"))

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

		# self.keyboard_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
		# set_keys = [*self.settings.settings_info.keys()]
		# for k in range(len(set_keys)//3):
		# 	self.keyboard_settings.add(types.KeyboardButton(text=set_keys[k*3]), types.KeyboardButton(text=set_keys[k*3 + 1]), types.KeyboardButton(text=set_keys[k*3 + 2]))
		
		# if (len(set_keys) % 3 == 1): 
		# 	self.keyboard_settings.add(types.KeyboardButton(text=set_keys[-1]))
		# elif (len(set_keys) % 3 == 2): 
		# 	self.keyboard_settings.add(types.KeyboardButton(text=set_keys[-2]), types.KeyboardButton(text=set_keys[-1]))
		# self.keyboard_settings.add(types.KeyboardButton(text="Main"))

	def create_keyboard_cities(self):
		cities_history = self.settings.cities_history
		self.keyboard_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)
		for k in range(len(cities_history)//2):
			self.keyboard_cities.add(types.KeyboardButton(text=cities_history[k*2]), types.KeyboardButton(text=cities_history[k*2 + 1]))
		if len(cities_history) % 2 != 0: self.keyboard_cities.add(types.KeyboardButton(text=cities_history[-1]))

		self.keyboard_cities.add(types.KeyboardButton(text="Main"))

	def create_keyboard_binance(self):
		binance_val_list = self.settings.binance_val_list
		self.keyboard_binance = types.ReplyKeyboardMarkup(resize_keyboard=True)
		for k in range(len(binance_val_list)//2):
			self.keyboard_binance.add(types.KeyboardButton(text=binance_val_list[k*2]), types.KeyboardButton(text=binance_val_list[k*2 + 1]))
		if len(binance_val_list) % 2 != 0: self.keyboard_binance.add(types.KeyboardButton(text=binance_val_list[-1]))

		self.keyboard_binance.add(types.KeyboardButton(text="Main"))

	def get_main(self):
		return self.keyboard_main

	def get_bin(self):
		return self.keyboard_bin

	def get_cities(self):
		return self.keyboard_cities

	def get_binance(self):
		return self.keyboard_binance

	def get_settings(self):
		return self.keyboard_settings