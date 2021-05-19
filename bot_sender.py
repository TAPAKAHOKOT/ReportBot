
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
# ? TODO: add language chooser
# // TODO: make a beautiful working time output
# TODO: add opportunity to add working period throught telegram
# TODO: add opportunity for editing periods
# TODO: add opportunity for deleting periods
# TODO: add opportunity for watching old dates
# // TODO: add weeks works hours autocounter
# TODO: add emoji into keyboard
# TODO: add graphics and statistics of working time bv
# // TODO: add admin keyboard
# TODO: add help command
# TODO: make a video about the capabilities of the bot
# TODO: add table in database with user settings
# // * TODO: improve code by adding logs
# * TODO: add logging for another files
# * TODO: improve work.py file code
# * TODO: improve all code by adding annotations

# <<<<<<<<<<<<<<<<<< Start >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
	global keyboard
	work_time =  get_work_time(settings, message.from_user["id"])
	w, s, t = "Начать работать" if not work_time.is_working else "Закончить работать", work_time.status.title(), "#" + work_time.tag
	await message.answer("Запуск основной клавиатуры", reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))

# <<<<<<<<<<<<<<<<<< main >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='main', ignore_case=True))
async def cmd_start(message: types.Message):
	logging.info("Start main message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

	global keyboard
	work_time =  get_work_time(settings, message.from_user["id"])

	# print(message.from_user["id"], message.from_user["username"])

	w, s, t = "Начать работать" if not work_time.is_working else "Закончить работать", work_time.status.title(), "#" + work_time.tag
	print(s, w, t)
	logging.info("Sended %s for (%s <=> %s)" % ("Openning main keyboard", message.from_user["id"], message.from_user["username"]))
	await message.answer("Openning main keyboard", reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))
	logging.info("End main message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

# <<<<<<<<<<<<<<<<<< submain >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(commands=["admin"])
async def cmd_start(message: types.Message):
	logging.info("Start submain message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
	global keyboard
	if message.from_user["id"] == settings.my_id:
		logging.info("Sended %s for (%s <=> %s)" % ("Openning submain keyboard", message.from_user["id"], message.from_user["username"]))
		await message.answer("Openning submain keyboard", reply_markup=keyboard.get_submain())
	else:
		logging.info("Sended %s for (%s <=> %s)" % ("Error 403: access is denied", message.from_user["id"], message.from_user["username"]))
		await message.answer("Error 403: access is denied")
	logging.info("End submain message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

# <<<<<<<<<<<<<<<<<< Рабочая клавиатура >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='рабочая клавиатура', ignore_case=True))
async def cmd_start(message: types.Message):
	logging.info("Start рабочая клавиатура message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
	global keyboard
	logging.info("Sended %s for (%s <=> %s)" % ("Openning work keyboard", message.from_user["id"], message.from_user["username"]))
	await message.answer("Openning work keyboard", reply_markup=keyboard.get_work())
	logging.info("End рабочая клавиатура message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

# <<<<<<<<<<<<<<<<<< Доп. >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='доп.', ignore_case=True))
async def cmd_start(message: types.Message):
	logging.info("Start Доп. message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
	global keyboard
	logging.info("Sended %s for (%s <=> %s)" % ("Openning dop. keyboard", message.from_user["id"], message.from_user["username"]))
	await message.answer("Openning dop. keyboard", reply_markup=keyboard.get_dop_work())
	logging.info("End Доп. message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

# <<<<<<<<<<<<<<<<<< Настройки >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='настройки', ignore_case=True))
async def cmd_start(message: types.Message):
	global keyboard
	if message.from_user["id"] == settings.my_id:
		await message.answer(settings.settings_info_line.replace(": ", "   >>>   "), reply_markup=keyboard.get_settings())
	else:
		await message.answer("Error 403: access is denied")

# <<<<<<<<<<<<<<<<<< Отправить >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отправить', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	if message.from_user["id"] == settings.my_id:
		await message.answer("Start loading message")
		feadback = send_otchet()

		if feadback != "None":
			await message.answer(feadback)
			await message.answer("Check your settings:\n     " + settings.settings_info_line.replace(": ", "   >>>   ").replace("\n", "\n     "))
		else:
			await message.answer("Message Send")
			settings.settings_info["File Send"] = "1"
			settings.settings_info_line = update_info_line()
	else:
		await message.answer("Error 403: access is denied")

# <<<<<<<<<<<<<<<<<< Начать работать >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='начать работать', ignore_case=True))
async def cmd_start(message: types.Message):
	logging.info("Start начать работать message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	w, s, t = "Закончить работать", work_time.status.title(), "#" + work_time.tag

	# keyboard.update_keyboard_main("Закончить работать", work_time.status.title())
	# keyboard.update_keyboard_work("Закончить работать")
	mes = work_time.start_working()
	logging.info("Sended %s for (%s <=> %s)" % (mes, message.from_user["id"], message.from_user["username"]))
	await message.answer(mes, reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))
	logging.info("End начать работать message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

# <<<<<<<<<<<<<<<<<< Закончить работать >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='закончить работать', ignore_case=True))
async def cmd_start(message: types.Message):
	logging.info("Start закончить работать message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	w, s, t = "Начать работать", work_time.status.title(), "#" + work_time.tag

	# keyboard.update_keyboard_main("Начать работать", work_time.status.title())
	# keyboard.update_keyboard_work("Начать работать")
	mes = work_time.end_working(message.from_user["id"])
	logging.info("Sended %s for (%s <=> %s)" % (mes, message.from_user["id"], message.from_user["username"]))
	await message.answer(mes, reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))
	logging.info("End закончить работать message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

# <<<<<<<<<<<<<<<<<< Studying >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='studying', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	work_time.set_status("working")

	w, s, t = "Начать работать" if not work_time.is_working else "Закончить работать", work_time.status.title(), "#" + work_time.tag

	# keyboard.update_keyboard_main("Начать работать" if not work_time.is_working else "Закончить работать", "Working")
	await message.answer("Status => Working", reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))

# <<<<<<<<<<<<<<<<<< Working >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='working', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	work_time.set_status("studying")

	w, s, t = "Начать работать" if not work_time.is_working else "Закончить работать", work_time.status.title(), "#" + work_time.tag

	# keyboard.update_keyboard_main("Начать работать" if not work_time.is_working else "Закончить работать", "Studying")
	await message.answer("Status => Studying", reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))

# <<<<<<<<<<<<<<<<<< Выбрать тэг >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals=['Tag: #reading', 'Tag: #coding', 'Tag: #listening', 'Tag: #reporting', 'Tag: #testing'], ignore_case=True))
async def cmd_start(message: types.Message):
	await message.answer("Openning work tag keyboard", reply_markup=keyboard.get_work_tag())

# <<<<<<<<<<<<<<<<<< #Tags >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals=['#reading', '#coding', '#listening', '#reporting', '#testing'], ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	w, s = "Начать работать" if not work_time.is_working else "Закончить работать", work_time.status.title()
	t = message.text

	work_time.set_tag(message.text[1:])
	await message.answer("Tag changed to: #" + work_time.tag, reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))

# <<<<<<<<<<<<<<<<<< Отработанные часы >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отработанные часы', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])

	if work_time.is_working:
		await message.answer(work_time.get_current_working_info())
	else:
		await message.answer(work_time.get_finfo_day_sum(message.from_user["id"]))

# <<<<<<<<<<<<<<<<<< Отработанные часы (прошлая неделя) >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отработанные часы (прошлая неделя)', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	await message.answer(work_time.get_finfo_day_sum(message.from_user["id"], True))

# <<<<<<<<<<<<<<<<<< Отработанные периоды >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отработанные периоды', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	await message.answer(work_time.get_finfo_day_intervals(message.from_user["id"]))

# <<<<<<<<<<<<<<<<<< Отработанные периоды (прошлая неделя) >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='отработанные периоды (прошлая неделя)', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	work_time =  get_work_time(settings, message.from_user["id"])
	await message.answer(work_time.get_finfo_day_intervals(message.from_user["id"], True))

# <<<<<<<<<<<<<<<<<< Кулькулятор >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='кулькулятор', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	if message.from_user["id"] == settings.my_id:
		await message.answer("Enter expression in python ")
		settings.calculate_readline = True
	else:
		await message.answer("Error 403: access is denied")

# <<<<<<<<<<<<<<<<<< living time >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='living time', ignore_case=True))
async def cmd_start(message: types.Message):
	if message.from_user["id"] == settings.my_id:
		cur_time = time.time()

		res_str = ""
		res = int(cur_time - start_time)

		symb = [" d    ", " : ", " : ", ""]
		for i, k in enumerate([24*3600, 3600, 60, 1]):
			res_str += str(res // k)
			res_str += symb[i]
			res -= (res // k) * k
		
		await message.answer(res_str)
	else:
		await message.answer("Error 403: access is denied")

# <<<<<<<<<<<<<<<<<< binance info >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='binance info', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	if message.from_user["id"] == settings.my_id:
		prices = settings.client.get_all_tickers()

		
		line = "No any matches"
		for inf in prices:
			if inf['symbol'] == settings.settings_info["Binance Currency"]:
				line = settings.settings_info["Binance Currency"] + " last cost is " + str(inf['price'])
				break

		await message.answer(line)
	else:
		await message.answer("Error 403: access is denied")

# <<<<<<<<<<<<<<<<<< Погода >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='погода', ignore_case=True))
async def cmd_start(message: types.Message):
	global settings
	if message.from_user["id"] == settings.my_id:
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
	else:
		await message.answer("Error 403: access is denied")

# <<<<<<<<<<<<<<<<<< Another >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler()
async def echo(message: types.Message):
	global settings, keyboard

	work_time =  get_work_time(settings, message.from_user["id"])
	w, s, t = "Начать работать" if not work_time.is_working else "Закончить работать", work_time.status.title(), "#" + work_time.tag

	canonical_command = message.text
	command = canonical_command.lower()
	
	if settings.change_settings and message.from_user["id"] == settings.my_id:
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
			await message.answer(settings.settings_info_line, reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))
			write_into_file()
		else:
			await message.answer("Back to main", reply_markup=keyboard.get_main(s, w, t, message.from_user["id"]))

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

	work_time =  get_work_time(settings, callback_query.from_user["id"])
	w, s, t = "Начать работать" if not work_time.is_working else "Закончить работать", work_time.status.title(), "#" + work_time.tag

	data = callback_query.data
	
	settings.change_settings = False

	if data != 'Main':
		
		settings.settings_info[settings.changing_settings] = data

		settings.settings_info_line = update_info_line()

		await settings.bot.answer_callback_query(callback_query.id)
		await settings.bot.send_message(callback_query.from_user.id, settings.settings_info_line, reply_markup=keyboard.get_main(s, w, t, callback_query.from_user["id"]))

		write_into_file()

	else:
		await settings.bot.send_message(callback_query.from_user.id, "Back to main", reply_markup=keyboard.get_main(s, w, t, callback_query.from_user["id"]))


start_time = time.time()
if __name__ == "__main__":
	executor.start_polling(settings.dp, skip_updates=True, on_startup=on_startup)