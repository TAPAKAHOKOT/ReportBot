from settings_tg import Settings 
from sendShit import *

import aioschedule as schedule
import asyncio
import codecs
from datetime import date
from work import Work

settings = Settings()

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
	if not u_id in settings.work_time_dict.keys():
		settings.work_time_dict[u_id] = Work()
	return settings.work_time_dict[u_id]

async def send():
	global settings
	async def memery_on():
		if settings.settings_info["Sending Activate"] == "1":
			if settings.settings_info["File Send"] == "0":
				await settings.bot.send_message(settings.my_id, "Send report pls!!!")
	
	async def knopa_memery_on():
		await settings.bot.send_message(settings.my_id, "Don't forget to comb Knopa")

	async def update_flags():
		global settings

		if (settings.settings_info["File Send"] != "0" or settings.settings_info["Sending Activate"] == "1"):
			settings.settings_info["File Send"] = "0"
			settings.settings_info_line = update_info_line()
			write_into_file()
			await settings.bot.send_message(settings.my_id, "Flags updated")

	async def check_binance():
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

	async def check_noIp():
		global settings
		today = date.today()

		day = today.strftime("%d")
		if day == settings.settings_info["NoIp"]:
			await settings.bot.send_message(settings.my_id, "Update HostName on NoIp")


	async def check_sending():
		global settings

		if settings.settings_info["Sending Activate"] == "1":
			if settings.settings_info["File Send"] == "0":
				await settings.bot.send_message(settings.my_id, "Start loading message")
				feadback = send_otchet()

				if feadback != "None":
					await settings.bot.send_message(settings.my_id, feadback)
					await settings.bot.send_message(settings.my_id, "Check your settings:\n     " + settings.settings_info_line.replace(": ", "   >>>   ").replace("\n", "\n     "))

				else:
					await settings.bot.send_message(settings.my_id, "Message Send")
					settings.settings_info["File Send"] = "1"
					settings.settings_info_line = update_info_line()
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

	schedule.every().day.at("12:00").do(check_noIp)

	schedule.every().day.at("22:00").do(knopa_memery_on)

	while True:
		await schedule.run_pending()
		await asyncio.sleep(60)
