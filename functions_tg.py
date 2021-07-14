from typing import Text
from Settings import Settings 

from aiogram.types.inline_keyboard import InlineKeyboardMarkup
import aioschedule as schedule
import asyncio
from Work import Work
import datetime

from DataBaseConnectors.CustomerDBC import CustomerDBC

import logging
import sys

TESTING = sys.argv[1] if len(sys.argv) > 1 else "TEST"

TESTING = not (TESTING == "REL")

settings = Settings(TESTING)


def get_work_time(settigns: Settings, u_id, u_un) -> Work:
    logging.info("Start get_work_time(...)")

    cust_db = CustomerDBC(settings.db_data)
    customer = cust_db.get_customer(u_id)

    if not customer:
        cust_db.add_row(u_id, u_un)
    else:
        cust_db.set_name_customer(u_id, u_un)

    if not u_id in settings.work_time_dict.keys():
        logging.info("Created Work() for %s" % u_id)
        settings.work_time_dict[u_id] = Work(settings, u_id)
    logging.info("End get_work_time(...)")
    return [settings.work_time_dict[u_id], customer]


def create_work_time(settings: Settings, u_id, st_time: datetime.datetime):
    logging.info("Start create_work_time(...)")
    w = Work(settings, u_id)
    w.set_start_working_time(st_time)
    settings.work_time_dict[u_id] = w
    logging.info("End create_work_time(...)")


async def send():
    global settings
    callback = settings.callback

    reminder = InlineKeyboardMarkup(row_width=1)
    reminder.insert(callback.checkout_btn_callback["reminder"])

    reminder_push_up = InlineKeyboardMarkup(row_width=4)
    for k in range(4): reminder_push_up.insert(callback.get_checkout_push_up_btn_callback(4))

    async def knopa_memery_on():
        logging.info("Start knopa_memery_on()")
        logging.info("Sended for %s: 'Don't forget to comb Knopa'" % settings.my_id)
        mes = await settings.bot.send_message(settings.my_id, "Don't forget to comb Knopa", reply_markup=reminder)
        await settings.bot.send_message(settings.my_id, "😼")
        await settings.bot.pin_chat_message(settings.my_id, mes.message_id)
        logging.info("End knopa_memery_on()")
    
    async def push_ups_memery_on():
        logging.info("Start push_ups_memery_on()")
        logging.info("Sended for %s: 'Do not forget to push up'" % settings.my_id)
        mes = await settings.bot.send_message(settings.my_id, "Don't forget to push up: 0 done", reply_markup=reminder_push_up)
        await settings.bot.send_message(settings.my_id, "💪")
        await settings.bot.pin_chat_message(settings.my_id, mes.message_id)
        logging.info("End push_ups_memery_on()")
    
    async def mom_memery_on():
        logging.info("Start mom_memery_on()")
        logging.info("Sended for %s: 'Не забудь взвеситься'" % settings.mom_id)
        mes = await settings.bot.send_message(settings.mom_id, "Не забудь взвеситься", reply_markup=reminder)
        await settings.bot.send_message(settings.mom_id, "😏")
        await settings.bot.pin_chat_message(settings.mom_id, mes.message_id)
        logging.info("End mom_memery_on()")

    
    async def check_work_last_online():
        global settings
        for key in list(settings.work_time_dict):
            val = settings.work_time_dict[key]
            t = datetime.datetime.now() - val.last_online_time
            if t > datetime.timedelta(days=5):
                settings.work_time_dict[key].close_connection()
                del settings.work_time_dict[key]

    logging.info("Start initing all schedules")

    schedule.every().day.at("22:00").do(knopa_memery_on)

    schedule.every().day.at("8:00").do(mom_memery_on)
    schedule.every().day.at("20:00").do(mom_memery_on)

    schedule.every().day.at("12:00").do(push_ups_memery_on)

    schedule.every().hour.do(check_work_last_online)

    logging.info("End initing all schedules")

    logging.info("Start running schedules cycle (while True)")
    while True:
        await schedule.run_pending()
        await asyncio.sleep(60)
