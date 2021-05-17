from aiogram import types
import logging

class Keyboard:
	def __init__(self, settings):
		logging.info("Start initing Settings")
		self.settings = settings
		
		# KEYBOARDS_MAIN
		self.keyboards_main = {"Studying": {"Начать работать": {}, "Закончить работать": {}},
								"Working": {"Начать работать": {}, "Закончить работать": {}}}
		
		for s in ["Studying", "Working"]:
			for w in ["Начать работать", "Закончить работать"]:
				for t in ["#reading", "#coding", "#listening", "#reporting", "#testing"]:
					keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
					keyboard_main.add(types.KeyboardButton(text="Tag: %s" % t), types.KeyboardButton(text=s))
					keyboard_main.add(types.KeyboardButton(text="Рабочая клавиатура"), types.KeyboardButton(text=w))
					self.keyboards_main[s][w][t] = keyboard_main
				
		# KEYBOARD_SUBMAIN
		self.keyboard_submain = types.ReplyKeyboardMarkup(resize_keyboard=True)
		self.keyboard_submain.add(types.KeyboardButton(text="Binance info"), types.KeyboardButton(text="Living time"))
		self.keyboard_submain.add(types.KeyboardButton(text="Кулькулятор"), types.KeyboardButton(text="Погода"))
		self.keyboard_submain.add(types.KeyboardButton(text="Отправить"), types.KeyboardButton(text="Настройки"))
		self.keyboard_submain.add(types.KeyboardButton(text="Main"))

		# KEYBOARD WORK
		self.keyboard_work = types.ReplyKeyboardMarkup(resize_keyboard=True)
		self.keyboard_work.add(types.KeyboardButton(text="Отработанные часы"), types.KeyboardButton(text="Отработанные периоды"))
		self.keyboard_work.add(types.KeyboardButton(text="Отработанные часы (прошлая неделя)"), types.KeyboardButton(text="Отработанные периоды (прошлая неделя)"))
		self.keyboard_work.add(types.KeyboardButton(text="Main"))

		# KEYBOARD DOP WORK
		self.keyboard_dop_work = types.ReplyKeyboardMarkup(resize_keyboard=True)
		self.keyboard_dop_work.add(types.KeyboardButton(text="Отработанные часы (прошлая неделя)"))
		self.keyboard_dop_work.add(types.KeyboardButton(text="Отработанные периоды (прошлая неделя)"))
		self.keyboard_dop_work.add(types.KeyboardButton(text="Main"))

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

		# self.keyboard_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
		# set_keys = [*self.settings.settings_info.keys()]
		# for k in range(len(set_keys)//3):
		# 	self.keyboard_settings.add(types.KeyboardButton(text=set_keys[k*3]), types.KeyboardButton(text=set_keys[k*3 + 1]), types.KeyboardButton(text=set_keys[k*3 + 2]))
		
		# if (len(set_keys) % 3 == 1): 
		# 	self.keyboard_settings.add(types.KeyboardButton(text=set_keys[-1]))
		# elif (len(set_keys) % 3 == 2): 
		# 	self.keyboard_settings.add(types.KeyboardButton(text=set_keys[-2]), types.KeyboardButton(text=set_keys[-1]))
		# self.keyboard_settings.add(types.KeyboardButton(text="Main"))

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
	
	def update_keyboard_main(self, work_status, status):
		# KEYBOARD_MAIN
		# self.keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
		# self.keyboard_main.add(types.KeyboardButton(text="Настройки"), types.KeyboardButton(text=status))
		# self.keyboard_main.add(types.KeyboardButton(text="Рабочая клавиатура"), types.KeyboardButton(text=work_status))
		# self.keyboard_main.add(types.KeyboardButton(text="Submain"))
		pass
	
	def update_keyboard_work(self, work_status):
		# KEYBOARD WORK
		# self.keyboard_work = types.ReplyKeyboardMarkup(resize_keyboard=True)
		# self.keyboard_work.add(types.KeyboardButton(text="Выбрать тэг"), types.KeyboardButton(text={work_status}))
		# self.keyboard_work.add(types.KeyboardButton(text="Отработанные часы"), types.KeyboardButton(text="Отработанные периоды"))
		# self.keyboard_work.add(types.KeyboardButton(text="Main"))
		pass

	def get_main(self, s, w, t, u_id):
		return self.keyboards_main[s][w][t]
	
	def get_submain(self):
		return self.keyboard_submain
	
	def get_work(self):
		return self.keyboard_work
	
	def get_work_tag(self):
		return self.keyboard_work_tag

	def get_dop_work(self):
		return self.keyboard_dop_work

	def get_bin(self):
		return self.keyboard_bin

	def get_cities(self):
		return self.keyboard_cities

	def get_binance(self):
		return self.keyboard_binance

	def get_settings(self):
		return self.keyboard_settings
	