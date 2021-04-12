import logging
from binance.client import Client
import codecs
from aiogram import Bot, Dispatcher

class Settings:
	def __init__(self):
		self.b_vers = 2.0
		print("Bot version " + str(self.b_vers))

		self.api_key = 'd0uy6vPg0CbCsPOSAZOborpqMJMWmLwp1trqa8Mz8UeobliYpBTnmZWBauoQZsrc'
		self.api_secret = 'MPDLBUCjFVhYq6zcytoAxvJNX98ilaBbDXbO1ql9RSBla9mC0exMLk9NvANnD3yg'

		self.client = Client(self.api_key, self.api_secret)

		self.my_id = 472914986

		self.token = '1454531950:AAHPgH_Ekh5mXqzoWCu9tSWLvara9pGI6aY'
		logging.basicConfig(level=logging.INFO)
		self.bot = Bot(token=self.token)
		self.dp = Dispatcher(self.bot)

		self.prices = self.client.get_all_tickers()

		self.settings_info = {}
		self.settings_info_line = ""

		self.change_settings = False
		self.changing_settings = "None"

		self.calculate_readline = False

		self.another_set = False
		self.hists =  {'cities': False, 'binance': False}
		self.fill_data()

	def clear_line(self, line):
		return line.replace("\n", "").replace(" ", "")

	def fill_data(self):
		with codecs.open("send_data.txt", encoding = 'utf-8', mode = 'r') as file:
			line = file.readline()
			while line:
				if self.clear_line(line) != "":
					if self.clear_line(line)[0] == "-" or self.another_set:
						if self.clear_line(line)[1] == "1":
							self.another_set = True
							self.hists['cities'] = True
						elif self.clear_line(line)[1] == "2":
							self.hists['cities'] = False
							self.hists['binance'] = True
						else:
							if self.hists['cities']:
								self.cities_history = self.clear_line(line).split(",")
							elif self.hists['binance']:
								self.binance_val_list = self.clear_line(line).split(",")

					else:
						sup_arr = line.split(": ", 1)

						self.settings_info[sup_arr[0]] = self.clear_line(sup_arr[1])
						self.settings_info_line += sup_arr[0] + ":\t" + self.clear_line(sup_arr[1]) + "\n"

				line = file.readline()