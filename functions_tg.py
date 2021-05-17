from settings_tg import Settings 
from sendShit import *

import aioschedule as schedule
import asyncio
import codecs
from datetime import date
from work import Work

import logging

settings = Settings()

def n2n(num, n1, n2, res_1=0, res_2="", arr=[]):
	for k in range(10, 36): arr.append(k); arr.append(chr(87 + k).upper())
	for k in range(len(num)):
		nk = num[-1-k].upper()
		res_1 += (n1**k*arr[arr.index(nk) - 1] if nk in arr else n1**k*int(nk))
	while res_1 != 0:
		end, res_1 = res_1%n2, (res_1 - (res_1%n2))//n2
		res_2 += (arr[arr.index(end) + 1] if end in arr else str(end))
	return res_2[::-1]

def update_info_line():
	settings.settings_info["City"] = settings.settings_info["City"].title()
	line = ""
	for key, val in settings.settings_info.items():
		line += key + ": " + val + "\n"
	return line

def write_into_file():
	with codecs.open("send_data.txt", encoding = 'utf-8', mode = 'w') as file:
		file.write(settings.settings_info_line)

		line = "-1\n" + ", ".join(settings.cities_history)
		file.write(line)
		line = "\n-2\n" + ", ".join(settings.binance_val_list)
		file.write(line)

def start_process():
    p1 = Thread(target=send, args=())
    p1.start()

def get_work_time(settigns, u_id):
	logging.info("Start get_work_time(...)")
	if not u_id in settings.work_time_dict.keys():
		logging.info("Created Work() for %s" % u_id)
		settings.work_time_dict[u_id] = Work()
	logging.info("End get_work_time(...)")
	return settings.work_time_dict[u_id]

async def send():
	global settings
	async def memery_on():
		logging.info("Start memory_on()")
		if settings.settings_info["Sending Activate"] == "1":
			if settings.settings_info["File Send"] == "0":
				logging.info("Sended for %s: 'Send report pls!!!'" % settings.my_id)
				await settings.bot.send_message(settings.my_id, "Send report pls!!!")
		logging.info("End memory_on()")
	
	async def knopa_memery_on():
		logging.info("Start knopa_memery_on()")
		logging.info("Sended for %s: 'Don't forget to comb Knopa'" % settings.my_id)
		await settings.bot.send_message(settings.my_id, "Don't forget to comb Knopa")
		logging.info("End knopa_memery_on()")

	async def update_flags():
		logging.info("Start update_flags()")
		global settings

		if (settings.settings_info["File Send"] != "0" or settings.settings_info["Sending Activate"] == "1"):
			settings.settings_info["File Send"] = "0"
			settings.settings_info_line = update_info_line()
			write_into_file()
			logging.info("Sended for %s: 'Flags updated'" % settings.my_id)
			await settings.bot.send_message(settings.my_id, "Flags updated")
		logging.info("End update_flags()")

	async def check_binance():
		logging.info("Start check_binance()")
		global settings
		prices = settings.client.get_all_tickers()

		binFo = {}
		for inf in prices:
			if inf['symbol'] in settings.binance_val_list:
				binFo[inf["symbol"]] = " last cost is " + str(inf['price']) + "\n"

		line = ""
		for key in settings.binance_val_list:
			if key in binFo.keys():
				line += key + binFo[key]

		if line:
			await settings.bot.send_message(settings.my_id, line)
		logging.info("End check_binance()")

	async def check_noIp():
		logging.info("Start check_noIp()")
		global settings
		today = date.today()

		day = today.strftime("%d")
		if day == settings.settings_info["NoIp"]:
			logging.info("Sended for %s: 'Update HostName on NoIp'" % settings.my_id)
			await settings.bot.send_message(settings.my_id, "Update HostName on NoIp")
		logging.info("End check_noIp()")


	async def check_sending():
		logging.info("Start check_sending()")
		global settings

		if settings.settings_info["Sending Activate"] == "1":
			if settings.settings_info["File Send"] == "0":
				logging.info("Sended for %s: 'Start loading message'" % settings.my_id)
				await settings.bot.send_message(settings.my_id, "Start loading message")
				feadback = send_otchet()

				if feadback != "None":
					logging.info("Sended for %s: '%s'" % (settings.my_id, feadback))
					await settings.bot.send_message(settings.my_id, feadback)
					logging.info("Sended for %s: '%s'" % (settings.my_id, "Check your settings:\n     " + settings.settings_info_line.replace(": ", "   >>>   ").replace("\n", "\n     ")))
					await settings.bot.send_message(settings.my_id, "Check your settings:\n     " + settings.settings_info_line.replace(": ", "   >>>   ").replace("\n", "\n     "))

				else:
					logging.info("Sended for %s: '%s'" % (settings.my_id, "Message Send"))
					await settings.bot.send_message(settings.my_id, "Message Send")
					settings.settings_info["File Send"] = "1"
					settings.settings_info_line = update_info_line()
					write_into_file()
		logging.info("End check_sending()")

	logging.info("Start initing all schedules")
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

	schedule.every().day.at("12:00").do(check_noIp)

	schedule.every().day.at("22:00").do(knopa_memery_on)

	logging.info("End initing all schedules")

	logging.info("Start running schedules cycle (while True)")
	while True:
		await schedule.run_pending()
		await asyncio.sleep(60)
