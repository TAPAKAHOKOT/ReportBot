
from keyboard_tg import Keyboard

from update_weather import *
from functions_tg import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import math as m

import time

from threading import Thread
from datetime import datetime

keyboard = Keyboard(settings)

async def on_startup(x):
	asyncio.create_task(send())

# ! TODO: add autosave working time into json file every 2 minutes
# ? TODO: translate all features in english
# TODO: add autocreating csv-file for every month like csv_data_05_2021
# TODO: add opportunity to add working period throught telegram
# TODO: add opportunity for editing periods
# TODO: add opportunity for deleting periods
# * TODO: improve code by adding logs
# * TODO: improve work.py file code
# * TODO: improve all code by adding annotations

# <<<<<<<<<<<<<<<<<< Start >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
	global keyboard
	await message.answer("Запуск основной клавиатуры", reply_markup=keyboard.get_main())

# <<<<<<<<<<<<<<<<<< main >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='main', ignore_case=True))
async def cmd_start(message: types.Message):
	global keyboard
	await message.answer("Openning main keyboard", reply_markup=keyboard.get_main())

# <<<<<<<<<<<<<<<<<< submain >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='submain', ignore_case=True))
async def cmd_start(message: types.Message):
	global keyboard
	await message.answer("Openning submain keyboard", reply_markup=keyboard.get_submain())

# <<<<<<<<<<<<<<<<<< Рабочая клавиатура >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='рабочая клавиатура', ignore_case=True))
async def cmd_start(message: types.Message):
	global keyboard
	await message.answer("Openning work keyboard", reply_markup=keyboard.get_work())

# <<<<<<<<<<<<<<<<<< Настройки >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='настройки', ignore_case=True))
async def cmd_start(message: types.Message):
	global keyboard
	await message.answer(settings.settings_info_line.replace(": ", "   >>>   "), reply_markup=keyboard.get_settings())

# <<<<<<<<<<<<<<<<<< Отправить >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отправить', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	await message.answer("Start loading message")
	feadback = send_otchet()

	if feadback != "None":
		await message.answer(feadback)
		await message.answer("Check your settings:\n     " + settings.settings_info_line.replace(": ", "   >>>   ").replace("\n", "\n     "))
	else:
		await message.answer("Message Send")
		settings.settings_info["File Send"] = "1"
		settings.settings_info_line = update_info_line()

# <<<<<<<<<<<<<<<<<< Начать работать >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='начать работать', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	keyboard.update_keyboard_main("Закончить работать")
	await message.answer(settings.work_time.start_working(), reply_markup=keyboard.get_main())

# <<<<<<<<<<<<<<<<<< Закончить работать >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='закончить работать', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	keyboard.update_keyboard_main("Начать работать")
	await message.answer(settings.work_time.end_working(), reply_markup=keyboard.get_main())

# <<<<<<<<<<<<<<<<<< Отработанные часы >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отработанные часы', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	if settings.work_time.is_working:
		await message.answer(settings.work_time.get_current_working_info())
	else:
		await message.answer(settings.work_time.get_finfo_day_sum())

# <<<<<<<<<<<<<<<<<< Отработанные периоды >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отработанные периоды', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	await message.answer(settings.work_time.get_finfo_day_intervals())

# <<<<<<<<<<<<<<<<<< Кулькулятор >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='кулькулятор', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	await message.answer("Enter expression")
	settings.calculate_readline = True

# <<<<<<<<<<<<<<<<<< living time >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='living time', ignore_case=True))
async def cmd_start(message: types.Message):
	cur_time = time.time()

	res_str = ""
	res = int(cur_time - start_time)

	symb = [" d    ", " : ", " : ", ""]
	for i, k in enumerate([24*3600, 3600, 60, 1]):
		res_str += str(res // k)
		res_str += symb[i]
		res -= (res // k) * k

	await message.answer(res_str)

# <<<<<<<<<<<<<<<<<< binance info >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='binance info', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	prices = settings.client.get_all_tickers()

	
	line = "No any matches"
	for inf in prices:
		if inf['symbol'] == settings.settings_info["Binance Currency"]:
			line = settings.settings_info["Binance Currency"] + " last cost is " + str(inf['price'])
			break

	await message.answer(line)

# <<<<<<<<<<<<<<<<<< Погода >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='погода', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	await message.answer("Please wait...")

	try:
		res = update_img(settings.settings_info["City"])
		weather_update_time = datetime.today().strftime("%d.%m   %H:%M:%S")

		with open("weather.png", "rb") as file:
			data = file.read()
			if data != None:
				await settings.bot.send_photo(message.chat.id, data)
			else:
				await message.answer("Image load error")
	except:
		await message.answer("Image error")

# <<<<<<<<<<<<<<<<<< Another >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler()
async def echo(message: types.Message):
	global settings, keyboard

	canonical_command = message.text
	command = canonical_command.lower()
	
	if settings.change_settings:
		settings.change_settings = False
		if command != "main":
			settings.settings_info[settings.changing_settings] = command

			if (settings.changing_settings == "City"):
				if command.title() not in settings.cities_history:
					if command.title() != "Main":
						settings.cities_history = [command.title(), *settings.cities_history[:-1]]
				else:
					settings.cities_history.remove(command.title())
					settings.cities_history = [command.title(), *settings.cities_history]
				keyboard.create_keyboard_cities()
			elif (settings.changing_settings == "Binance Currency"):
				settings.settings_info[settings.changing_settings] = command.upper()
				if command.upper() not in settings.binance_val_list:
					if command.title() != "Main":
						settings.binance_val_list = [command.upper(), *settings.binance_val_list[:-1]]
				else:
					settings.binance_val_list.remove(command.upper())
					settings.binance_val_list = [command.upper(), *settings.binance_val_list]
				keyboard.create_keyboard_binance()

			settings.settings_info_line = update_info_line()
			await message.answer(settings.settings_info_line, reply_markup=keyboard.get_main())
			write_into_file()
		else:
			await message.answer("Back to main", reply_markup=keyboard.get_main())

	elif settings.calculate_readline:
		settings.calculate_readline = False
		try:
			output = eval(canonical_command)
		except:
			output = "Code error"
		await message.answer("Result:   '" + str(output) + "'")

	elif message.text in settings.settings_info.keys():
		settings.change_settings = True 

		settings.changing_settings = canonical_command
		changing_settings = settings.changing_settings

		if changing_settings == "City":
			await message.answer("Changing <<" + changing_settings + ">> setting", reply_markup=keyboard.get_cities())
		elif changing_settings == "Binance Currency":
			await message.answer("Changing <<" + changing_settings + ">> setting", reply_markup=keyboard.get_binance())
		elif changing_settings in ["File Send", "Sending Activate"]:
			buttons = types.InlineKeyboardMarkup()
			buttons.add(types.InlineKeyboardButton('1', callback_data = '1'), types.InlineKeyboardButton('0', callback_data = '0'))
			buttons.add(types.InlineKeyboardButton('Main', callback_data = 'Main'))
			await message.answer("Changing <<" + changing_settings + ">> setting", reply_markup=buttons)
		else:
			await message.answer("Changing <<" + changing_settings + ">> setting")
  
@settings.dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
	global settings, keyboard

	data = callback_query.data
	
	settings.change_settings = False

	if data != 'Main':
		
		settings.settings_info[settings.changing_settings] = data

		settings.settings_info_line = update_info_line()

		await settings.bot.answer_callback_query(callback_query.id)
		await settings.bot.send_message(callback_query.from_user.id, settings.settings_info_line, reply_markup=keyboard.get_main())

		write_into_file()

	else:
		await settings.bot.send_message(callback_query.from_user.id, "Back to main", reply_markup=keyboard.get_main())


start_time = time.time()
if __name__ == "__main__":
	executor.start_polling(settings.dp, skip_updates=True, on_startup=on_startup)