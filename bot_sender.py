# my token	1454531950:AAHPgH_Ekh5mXqzoWCu9tSWLvara9pGI6aY
# it_reports@bk.ru

from sendShit import *
from update_weather import *

from aiogram import Bot, Dispatcher, executor, types
import aioschedule as schedule
import math as m

import asyncio
import logging
import time
import codecs
from threading import Thread
from datetime import datetime
from binance.client import Client

api_key = 'd0uy6vPg0CbCsPOSAZOborpqMJMWmLwp1trqa8Mz8UeobliYpBTnmZWBauoQZsrc'
api_secret = 'MPDLBUCjFVhYq6zcytoAxvJNX98ilaBbDXbO1ql9RSBla9mC0exMLk9NvANnD3yg'

client = Client(api_key, api_secret)

my_id = 472914986

def n2n(num, n1, n2, res_1 = 0, res_2 = "", arr = []):
	for k in range(10, 36): arr.append(k); arr.append(chr(87 + k).upper())
	for k in range(len(num)):
		nk = num[-1-k].upper()
		res_1 += (n1**k*arr[arr.index(nk) - 1] if nk in arr else n1**k*int(nk))
	while res_1 != 0:
		end, res_1 = res_1%n2, (res_1 - (res_1%n2))//n2
		res_2 += (arr[arr.index(end) + 1] if end in arr else str(end))
	return res_2[::-1]

def update_info_line():
	settings_info["City"] = settings_info["City"].title()
	line = ""
	for key, val in settings_info.items():
		line += key + ": " + val + "\n"
	return line

def write_into_file():
	with codecs.open("send_data.txt", encoding = 'utf-8', mode = 'w') as file:
		file.write(settings_info_line)

		line = "-1\n" + ", ".join(cities_history)
		file.write(line)
		line = "\n-2\n" + ", ".join(binance_val_list)
		file.write(line)

def start_process():
    p1 = Thread(target=send, args=())
    p1.start()
 

token = '1454531950:AAHPgH_Ekh5mXqzoWCu9tSWLvara9pGI6aY'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)

prices = client.get_all_tickers()

async def send():
	global settings_info_line, settings_info
	async def memery_on():
		if settings_info["Sending Activate"] == "1":
			if settings_info["File Send"] == "0":
				await bot.send_message(my_id, "Send report pls!!!")

	async def update_flags():
		global settings_info_line, settings_info

		if (settings_info["File Send"] != "0" or settings_info["Sending Activate"] == "1"):
			settings_info["File Send"] = "0"
			settings_info_line = update_info_line()
			write_into_file()
			await bot.send_message(my_id, "Flags updated")

	async def check_binance():
		global client, settings_info, binance_val_list
		prices = client.get_all_tickers()

		line = ""
		for inf in prices:
			if inf['symbol'] in binance_val_list:
				line += inf['symbol'] + " last cost is " + str(inf['price']) + "\n"

		if line:
			await bot.send_message(my_id, line)

	async def check_sending():
		global settings_info_line, settings_info

		if settings_info["Sending Activate"] == "1":
			if settings_info["File Send"] == "0":
				await bot.send_message(my_id, "Start loading message")
				feadback = send_otchet()

				if feadback != "None":
					await bot.send_message(my_id, feadback)
					await bot.send_message(my_id, "Check your settings:\n     " + settings_info_line.replace(": ", "   >>>   ").replace("\n", "\n     "))

				else:
					await bot.send_message(my_id, "Message Send")
					settings_info["File Send"] = "1"
					settings_info_line = update_info_line()
					write_into_file()

	for k in range(1, 27, 15):
		cur_time = "13:" + str(k)

		schedule.every().monday.at(cur_time).do(memery_on)
		schedule.every().tuesday.at(cur_time).do(memery_on)
		schedule.every().wednesday.at(cur_time).do(memery_on)
		schedule.every().thursday.at(cur_time).do(memery_on)
		schedule.every().friday.at(cur_time).do(memery_on) 

	cur_time = "13:30"

	schedule.every().monday.at(cur_time).do(check_sending)
	schedule.every().tuesday.at(cur_time).do(check_sending)
	schedule.every().wednesday.at(cur_time).do(check_sending)
	schedule.every().thursday.at(cur_time).do(check_sending)
	schedule.every().friday.at(cur_time).do(check_sending) 

	schedule.every().day.at("9:00").do(check_binance)
	schedule.every().day.at("16:00").do(check_binance)
	schedule.every().day.at("23:00").do(check_binance)

	schedule.every().day.at("23:00").do(update_flags)
	while True:
		await schedule.run_pending()
		await asyncio.sleep(60)


clear_line = lambda x: x.replace("\n", "").replace(" ", "")

file = open("send_data.txt", "r")

settings_info = {}
settings_info_line = ""

change_settings = False
changing_settings = "None"

calculate_readline = False

another_set = False
hists =  {'cities': False, 'binance': False}
with codecs.open("send_data.txt", encoding = 'utf-8', mode = 'r') as file:
	line = file.readline()
	while line:
		if clear_line(line) != "":
			if clear_line(line)[0] == "-" or another_set:
				if clear_line(line) == "-1":
					another_set = True
					hists['cities'] = True
				elif clear_line(line) == "-2":
					hists['cities'] = False
					hists['binance'] = True
				else:
					if hists['cities']:
						cities_history = clear_line(line).split(",")
					elif hists['binance']:
						binance_val_list = clear_line(line).split(",")

			else:
				sup_arr = line.split(": ", 1)
				settings_info[sup_arr[0]] = clear_line(sup_arr[1])
				settings_info_line += sup_arr[0] + ":\t" + clear_line(sup_arr[1]) + "\n"

		line = file.readline()

settings_info_line = update_info_line()

keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(types.KeyboardButton(text="Настройки"), types.KeyboardButton(text="Отправить"))
keyboard_main.add(types.KeyboardButton(text="Кулькулятор"), types.KeyboardButton(text="Погода"))
keyboard_main.add(types.KeyboardButton(text="Living time"), types.KeyboardButton(text="Binance Info"))

keyboard_bin = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_bin.add(types.KeyboardButton(text="1"), types.KeyboardButton(text="0"))
keyboard_bin.add(types.KeyboardButton(text="Main"))

keyboard_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)
def create_keyboard_cities():
	global keyboard_cities
	keyboard_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for k in range(len(cities_history)//2):
		keyboard_cities.add(types.KeyboardButton(text=cities_history[k*2]), types.KeyboardButton(text=cities_history[k*2 + 1]))
	if len(cities_history) % 2 != 0: keyboard_cities.add(types.KeyboardButton(text=cities_history[-1]))

	keyboard_cities.add(types.KeyboardButton(text="Main"))

keyboard_binance = types.ReplyKeyboardMarkup(resize_keyboard=True)
def create_keyboard_binance():
	global keyboard_binance
	keyboard_binance = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for k in range(len(binance_val_list)//2):
		keyboard_binance.add(types.KeyboardButton(text=binance_val_list[k*2]), types.KeyboardButton(text=binance_val_list[k*2 + 1]))
	if len(binance_val_list) % 2 != 0: keyboard_binance.add(types.KeyboardButton(text=binance_val_list[-1]))

	keyboard_binance.add(types.KeyboardButton(text="Main"))

create_keyboard_cities()
create_keyboard_binance()

keyboard_settings = types.ReplyKeyboardMarkup(resize_keyboard=True)
set_keys = [*settings_info.keys()]

for k in range(len(set_keys)//2):
	keyboard_settings.add(types.KeyboardButton(text=set_keys[k*2]), types.KeyboardButton(text=set_keys[k*2 + 1]))
if (len(set_keys) % 2 != 0): keyboard_settings.add(types.KeyboardButton(text=set_keys[-1]))
keyboard_settings.add(types.KeyboardButton(text="Main"))

change_settings = False
calculate_readline = False

async def on_startup(x):
    asyncio.create_task(send())

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Запуск основной клавиатуры", reply_markup=keyboard_main)

@dp.message_handler()
async def echo(message: types.Message):
	global change_settings, settings_info_line, settings_info
	global changing_settings, calculate_readline, cities_history
	global binance_val_list, clinet

	canonical_command = message.text
	command = canonical_command.lower()
	
	if change_settings:
		change_settings = False
		if command != "main":
			settings_info[changing_settings] = command

		if (changing_settings == "City"):
			if command.title() not in cities_history:
				if command.title() != "Main":
					cities_history = [command.title(), *cities_history[:-1]]
			else:
				cities_history.remove(command.title())
				cities_history = [command.title(), *cities_history]
			create_keyboard_cities()
		elif (changing_settings == "Binance Currency"):
			settings_info[changing_settings] = command.upper()
			if command.upper() not in binance_val_list:
				if command.title() != "Main":
					binance_val_list = [command.upper(), *binance_val_list[:-1]]
			else:
				binance_val_list.remove(command.upper())
				binance_val_list = [command.upper(), *binance_val_list]
			create_keyboard_binance()

		settings_info_line = update_info_line()
		await message.answer(settings_info_line, reply_markup=keyboard_main)
		write_into_file()

	elif calculate_readline:
		calculate_readline = False
		try:
			output = eval(canonical_command)
		except:
			output = "Code error"
		await message.answer("Result:   '" + str(output) + "'")
	elif command == "отправить":
		await message.answer("Start loading message")
		feadback = send_otchet()

		if feadback != "None":
			await message.answer(feadback)
			await message.answer("Check your settings:\n     " + settings_info_line.replace(": ", "   >>>   ").replace("\n", "\n     "))
		else:
			await message.answer("Message Send")
			settings_info["File Send"] = "1"
			settings_info_line = update_info_line()
	elif command == "погода":
		await message.answer("Please wait...")

		try:
			res = update_img(settings_info["City"])
			weather_update_time = datetime.today().strftime("%d.%m   %H:%M:%S")

			with open("weather.png", "rb") as file:
				data = file.read()
				if data != None:
					await bot.send_photo(message.chat.id, data)
				else:
					await message.answer("Image load error")
		except:
			await message.answer("Image error")
		
	elif command == "настройки":
		await message.answer(settings_info_line.replace(": ", "   >>>   "), reply_markup=keyboard_settings)
	elif command == "кулькулятор":
		await message.answer("Enter expression")
		calculate_readline = True
	elif command == "living time":
		cur_time = time.time()

		res_str = ""
		res = int(cur_time - start_time)

		symb = [" d    ", " : ", " : ", ""]
		for i, k in enumerate([24*3600, 3600, 60, 1]):
			res_str += str(res // k)
			res_str += symb[i]
			res -= (res // k) * k

		await message.answer(res_str)
	elif command == "binance info":
		prices = client.get_all_tickers()

		line = "No any matches"
		for inf in prices:
			if inf['symbol'] == settings_info["Binance Currency"]:
				line = settings_info["Binance Currency"] + " last cost is " + str(inf['price'])

		await message.answer(line)
	elif command == "main":
		await message.answer("Openning main keyboard", reply_markup=keyboard_main)
	elif message.text in settings_info.keys():
		change_settings = True 
		changing_settings = canonical_command 
		if changing_settings == "City":
			await message.answer("Changing <<" + changing_settings + ">> setting", reply_markup=keyboard_cities)
		if changing_settings == "Binance Currency":
			await message.answer("Changing <<" + changing_settings + ">> setting", reply_markup=keyboard_binance)
		elif changing_settings in ["File Send", "Sending Activate"]:
			buttons = types.InlineKeyboardMarkup()
			buttons.add(types.InlineKeyboardButton('1', callback_data = '1'), types.InlineKeyboardButton('0', callback_data = '0'))
			buttons.add(types.InlineKeyboardButton('Main', callback_data = 'Main'))
			await message.answer("Changing <<" + changing_settings + ">> setting", reply_markup=buttons)
		else:
			await message.answer("Changing <<" + changing_settings + ">> setting")
  
@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
	global change_settings, settings_info, settings_info_line

	data = callback_query.data
	
	change_settings = False

	if data != 'Main':
		
		settings_info[changing_settings] = data

		settings_info_line = update_info_line()

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, settings_info_line, reply_markup=keyboard_main)

		write_into_file()

	else:
		await bot.send_message(callback_query.from_user.id, "Back to main", reply_markup=keyboard_main)


start_time = time.time()
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)