import time
from datetime import datetime

from aiogram.types import message
from Keyboard import Keyboard

from functions_tg import *
from DataBaseConnectors.BackupDBC import BackupDBC
from DataBaseConnectors.CustomerDBC import CustomerDBC

from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import executor, types
from aiogram.dispatcher.filters import Text

keyboard = Keyboard(settings)
callback = settings.callback

async def on_startup(x):
    asyncio.create_task(send())

# // ! TODO: add autosave working time into db every 2 minutes
# ! TODO: add autotest for db classes
# ! TODO: add comments in all new files
# // ! TODO: add saving work statuses between reloading server
# // ! TODO: add password crypting
# // ~ TODO: add getters and setters, add encapsulation
# // ~ TODO: add inheritance into db classes
# // ? TODO: translate all features in english
# ? TODO: add language chooser +-
# ? TODO: add settings for users
# TODO: add 'hide' callback button (with saving hidden data in db)
# TODO: add remainder constructor
# TODO: delete extra databases and functional
# TODO: add opportunity to remove part from work interval
# TODO: add foreign keys in db's
# TODO: add UTC choice
# // TODO: make a beautiful working time output
# // TODO: add opportunity to add working period throught telegram
# TODO: add opportunity for editing periods +-
# // TODO: add opportunity for deleting periods
# TODO: add opportunity for watching old dates
# TODO: add opportunity for watching all available dates
# // TODO: add weeks works hours autocounter
# TODO: add stickers
# // TODO: add emoji into keyboard +-
# TODO: add graphics and statistics of working time bd
# // TODO: add admin keyboard
# // TODO: add help command
# TODO: make a video about the capabilities of the bot +-
# // TODO: add table in database with user settings
# // TODO: add border between studing and working tags
# TODO: change names of db, tables, change structure of tables 
# // TODO: (ex: make ser_id the primary key)
# // TODO: files rebase
# // TODO: add user's cpecific tags
# // TODO: add user's tag history
# // TODO: add table in database with user statuses
# // * TODO: improve code by adding logs
# // * TODO: add logging for another files
# // * TODO: improve work.py file code
# * TODO: improve all code by adding annotations

# <<<<<<<<<<<<<<<<<< Start >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    cust_db = CustomerDBC(settings.db_data)
    customer = cust_db.get_customer(message.from_user["id"])
    work = get_work_time(settings, message.from_user["id"])
    w = "Start working" if not work.get_is_working() else "Stop working"
    await message.answer("Running main keyboard", reply_markup=keyboard.get_main(w))

    if not customer:
        cust_db.add_row(message.from_user["id"], message.from_user["username"])
        utc_choice = InlineKeyboardMarkup(row_width=3)
        for utc in settings.all_locations:
            utc_b = InlineKeyboardButton(
                    text="UTC" + utc,
                    callback_data=callback.location_callback.new(
                        status="set",
                        UTC=utc.replace(":", ".")
                    ))
            utc_choice.insert(utc_b)
        utc_choice.insert(
            InlineKeyboardButton(
                text="Back",
                callback_data=callback.location_callback.new(
                        status="back",
                        UTC="None"
                    )
            )
        )
        await message.answer("Configure your UTC settings or all the time will be displayed by UTC+3", reply_markup=utc_choice)


# <<<<<<<<<<<<<<<<<< Settings >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(commands=["settings"])
async def cmd_settings(message: types.Message):
    settings_choice = InlineKeyboardMarkup(row_width=1)
    for el in callback.settings_btns_callback:
        settings_choice.insert(el)
    await message.answer("Select the setting you want", reply_markup=settings_choice)


# <<<<<<<<<<<<<<<<<< Help >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(commands=["help"])
async def cmd_start(message: types.Message):
    work = get_work_time(settings, message.from_user["id"])
    w = "Start working" if not work.get_is_working() else "Stop working"

    mes = "👋Hi there, using this bot you can count your working or studying time🕑\n"
    mes += "Try it❗ (touch 'Start working' button)\n\n"
    mes += "At any time you can change yor status from working to stutying and vice versa👀\n"
    mes += "To do it, touch 'Status/Tag' button\n\n"
    mes += "Also you can get hours worked reports, otouch 'Work reports'🐠\n\n"
    mes += "After all, you can easily add/delete hours worked manually🌚 (touch 'Add/delete period')"

    await message.answer(mes, reply_markup=keyboard.get_main(w))


# <<<<<<<<<<<<<<<<<< main >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='main', ignore_case=True))
async def cmd_start(message: types.Message):
    logging.info("Start main message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

    work = get_work_time(settings, message.from_user["id"])

    w = "Start working" if not work.get_is_working() else "Stop working"
    logging.info("Sended %s for (%s <=> %s)" % ("Openning main keyboard", message.from_user["id"], message.from_user["username"]))
    await message.answer("Openning main keyboard", reply_markup=keyboard.get_main(w))
    logging.info("End main message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))


# <<<<<<<<<<<<<<<<<< stat >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='stat', ignore_case=True))
async def get_stat(message: types.Message):
    work = get_work_time(settings, message.from_user["id"])
    if settings.my_id == message.from_user["id"]:
        await message.answer("There are {} works".format(len(settings.work_time_dict.keys())))


# <<<<<<<<<<<<<<<<<< Work reports >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='work reports', ignore_case=True))
async def cmd_start(message: types.Message):
    logging.info("Start Work reports message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))

    choose = InlineKeyboardMarkup(row_width=2)
    choose.insert(callback.reports_btn_callback["last_week"])
    choose.insert(callback.reports_btn_callback["this_week"])
    choose.insert(callback.reports_btn_callback["last_week_d"])
    choose.insert(callback.reports_btn_callback["this_week_d"])

    logging.info("End Work reports message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
    await message.answer("Choose worked time report period", reply_markup=choose)


# <<<<<<<<<<<<<<<<<< Start working >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='start working', ignore_case=True))
async def cmd_start(message: types.Message):
    logging.info("Start Start working message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
    work = get_work_time(settings, message.from_user["id"])
    w = "Stop working"

    mes = work.start_working()
    logging.info("Sended %s for (%s <=> %s)" % (mes, message.from_user["id"], message.from_user["username"]))
    await message.answer(mes, reply_markup=keyboard.get_main(w))
    logging.info("End Start working message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))


# <<<<<<<<<<<<<<<<<< Stop working >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='stop working', ignore_case=True))
async def cmd_start(message: types.Message):
    logging.info("Start Stop working message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))
    work = get_work_time(settings, message.from_user["id"])
    w = "Start working"

    mes = work.end_working(message.from_user["id"])
    logging.info("Sended %s for (%s <=> %s)" % (mes, message.from_user["id"], message.from_user["username"]))
    await message.answer(mes, reply_markup=keyboard.get_main(w))
    logging.info("End Stop working message handler by (%s <=> %s)" % (message.from_user["id"], message.from_user["username"]))


# <<<<<<<<<<<<<<<<<< #Tags >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(startswith='#', ignore_case=True))
async def cmd_start(message: types.Message):
    work = get_work_time(settings, message.from_user["id"])
    w = "Start working" if not work.get_is_working() else "Stop working"

    work.set_tag(message.text)
    await message.answer("Tag changed to: " + work.get_tag(), reply_markup=keyboard.get_main(w))


# <<<<<<<<<<<<<<<<<< Меню изменения статуса или тэга >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals="Status/Tag", ignore_case=True))
async def cmd_start(message: types.Message):
    work = get_work_time(settings, message.from_user["id"])
    s, t = work.get_status(), work.get_tag()

    set_callback = InlineKeyboardMarkup(row_width=2)
    set_callback.insert(callback.get_tag_btn_callback("Tag -> " + t))
    set_callback.insert(callback.statuses_btn_callback[s])

    await message.answer("Click to change", reply_markup=set_callback)


# <<<<<<<<<<<<<<<<<< Изменение тэга >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.work_settings_callback.filter(parameter="tag"))
async def callback_work_report(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])
    s, t = work.get_status(), work.get_tag()
    if ("Tag -> " in callback_data["value"]):
        mes = "\n\nChoose a tag or write your tag in chat\n(# + tag name)"
        tags = work.tag_db.get_tags(work.user_id)

        set_callback = InlineKeyboardMarkup(row_width=3)
        for tag in tags:
            set_callback.insert(callback.get_tag_btn_callback(tag))
        set_callback.insert(callback.get_tag_btn_callback("Back"))
    elif ("Back" == callback_data["value"]):
        mes = "\nback"
        set_callback = InlineKeyboardMarkup(row_width=2)
        set_callback.insert(callback.get_tag_btn_callback("Tag -> " + t))
        set_callback.insert(callback.statuses_btn_callback[s])
    else:
        mes = "\nTag changed to " + callback_data["value"]
        work.set_tag(callback_data["value"])

        set_callback = InlineKeyboardMarkup(row_width=2)
        set_callback.insert(callback.get_tag_btn_callback("Tag -> " + callback_data["value"]))
        set_callback.insert(callback.statuses_btn_callback[s])
    
    await call.message.edit_text(call.message.text + mes, reply_markup=set_callback)


# <<<<<<<<<<<<<<<<<< Изменение статуса >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.work_settings_callback.filter(parameter="status"))
async def callback_work_report(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])
    s, t = work.get_status(), work.get_tag()

    if (callback_data["value"] == "working"):
        work.set_status("studying")
        mes = "\nStatus changed to 'Studying'"
        s = "Studying"
    elif (callback_data["value"] == "studying"):
        work.set_status("working")
        mes = "\nStatus changed to 'Working'"
        s = "Working"

    set_callback = InlineKeyboardMarkup(row_width=2)
    set_callback.insert(callback.get_tag_btn_callback("Tag -> " + t))
    set_callback.insert(callback.statuses_btn_callback[s])

    await call.message.edit_text(call.message.text + mes, reply_markup=set_callback)


# <<<<<<<<<<<<<<<<<< Отчёт об отработанных часах >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.work_reports_callback.filter(status="period_report"))
async def callback_work_report(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])

    choose = InlineKeyboardMarkup(row_width=2)
    choose.insert(callback.reports_btn_callback["last_week"])
    choose.insert(callback.reports_btn_callback["this_week"])
    choose.insert(callback.reports_btn_callback["last_week_d"])
    choose.insert(callback.reports_btn_callback["this_week_d"])

    if (callback_data["period"] == "this_week"):
        await call.message.edit_text(work.get_finfo_day_sum(call.from_user["id"]), reply_markup=choose)
    elif (callback_data["period"] == "this_week_d"):
        await call.message.edit_text(work.get_finfo_day_intervals(call.from_user["id"])[0], reply_markup=choose)
    elif (callback_data["period"] == "last_week"):
        await call.message.edit_text(work.get_finfo_day_sum(call.from_user["id"], True), reply_markup=choose)
    elif (callback_data["period"] == "last_week_d"):
        await call.message.edit_text(work.get_finfo_day_intervals(call.from_user["id"], last_week=True)[0], reply_markup=choose)
    # await call.message.edit_reply_markup(reply_markup=choose)


# <<<<<<<<<<<<<<<<<< Меню выбора нужного UTC  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.settings_callback.filter(status="utc"))
async def utc_settings_callback(call: types.CallbackQuery, callback_data: dict):
    utc_choice = InlineKeyboardMarkup(row_width=3)
    for utc in settings.all_locations:
        utc_b = InlineKeyboardButton(
                text="UTC" + utc,
                callback_data=callback.location_callback.new(
                    status="set",
                    UTC=utc.replace(":", ".")
                ))
        utc_choice.insert(utc_b)
    utc_choice.insert(
        InlineKeyboardButton(
            text="Back",
            callback_data=callback.location_callback.new(
                    status="back",
                    UTC="None"
                )
        )
    )
    await call.message.edit_text("Configure your UTC settings or all the time will be displayed by UTC+3", reply_markup=utc_choice)


# <<<<<<<<<<<<<<<<<< Возврат к настройкам пользователя  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.location_callback.filter(status="back"))
async def back_utc_callback(call: types.CallbackQuery, callback_data: dict):
    settings_choice = InlineKeyboardMarkup(row_width=1)
    for el in callback.settings_btns_callback:
        settings_choice.insert(el)
    await call.message.edit_text("Select the setting you want", reply_markup=settings_choice)


# <<<<<<<<<<<<<<<<<< Установка UTC пользователя  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.location_callback.filter(status="set"))
async def utc_callback(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])
    utc = callback_data["UTC"]
    utc = utc.replace(".", ":") + ":0" if "." in utc else utc + ":0:0"
    work.customer_db.set_time_zone(call.from_user["id"], utc)

    settings_choice = InlineKeyboardMarkup(row_width=1)
    for el in callback.settings_btns_callback:
        settings_choice.insert(el)

    await call.message.edit_text("UTC changed to UTC{}\n\nSelect the setting you want".format(callback_data["UTC"]), reply_markup=settings_choice)    


# <<<<<<<<<<<<<<<<<< Меню удаления и добавления отработанных периодов >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals="Add/delete period", ignore_case=True))
async def cmd_start(message: types.Message):
    choose = InlineKeyboardMarkup(row_width=1)
    choose.insert(callback.add_delete_period_btn_callback["Add"])
    choose.insert(callback.add_delete_period_btn_callback["Delete"])

    await message.answer("You can add or delete hours worked record", reply_markup=choose)


# <<<<<<<<<<<<<<<<<< Выбор отработанного периода для удаления >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.add_delete_work_period.filter(status="Delete"), )
async def choose_period_to_delete(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])
    res = work.get_finfo_day_intervals(call.from_user["id"], for_del=True)

    delete_callback = InlineKeyboardMarkup(row_width=int(res[1]**0.5 if res[1] != 0 else 1))
    if (res[1] == 0):
        delete_callback.insert(callback.get_delete_work_btn_callback("Back"))
        await call.message.edit_text("Nothing to delete", reply_markup=delete_callback)
    else:
        for k in range(1, res[1] + 1):
            delete_callback.insert(callback.get_delete_work_btn_callback(k))
        delete_callback.insert(callback.get_delete_work_btn_callback("Back"))
        
        await call.message.edit_text("SELECT NUMBER OF THE LINE TO DELETE\n\n" + res[0], reply_markup=delete_callback)


# <<<<<<<<<<<<<<<<<< Удаление отработанного периода  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.delete_work_time_callback.filter(deleting="y"))
async def save_day_date_callback(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])
    if (callback_data["id"] == "Back"):
        choose = InlineKeyboardMarkup(row_width=1)
        choose.insert(callback.add_delete_period_btn_callback["Add"])
        choose.insert(callback.add_delete_period_btn_callback["Delete"])
        await call.message.edit_text("You can add or delete hours worked record", reply_markup=choose)
    else:
        res_d = work.delete_interval(call.from_user["id"], int(callback_data["id"]))

        res = work.get_finfo_day_intervals(call.from_user["id"], for_del=True)
        delete_callback = InlineKeyboardMarkup(row_width=int(res[1]**0.5 if res[1] != 0 else 1))

        if (res[1] == 0):
            delete_callback.insert(callback.get_delete_work_btn_callback("Back"))
            await call.message.edit_text("Nothing to delete", reply_markup=delete_callback)
        else:
            for k in range(1, res[1] + 1):
                delete_callback.insert(callback.get_delete_work_btn_callback(k))
            delete_callback.insert(callback.get_delete_work_btn_callback("Back"))
            
            await call.message.edit_text("Row [{}] deleted\n\n".format(res_d) + "SELECT NUMBER OF THE LINE TO DELETE\n\n" + res[0], reply_markup=delete_callback)

        # await call.message.edit_text("Row [{}] deleted".format(res))


# <<<<<<<<<<<<<<<<<< Назад в меню удаления и добавления из конструктора добавления  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.date_callback.filter(time_unit="Back"))
async def callback_work_report(call: types.CallbackQuery, callback_data: dict):
    choose = InlineKeyboardMarkup(row_width=1)
    choose.insert(callback.add_delete_period_btn_callback["Add"])
    choose.insert(callback.add_delete_period_btn_callback["Delete"])
    await call.message.edit_text("You can add or delete hours worked record", reply_markup=choose)


# <<<<<<<<<<<<<<<<<< Добавление отработанного периода >>>>>>>>>>>>>>>>>>
tr_val = lambda v: str(v) if len(str(v)) == 2 else "0" + str(v)
@settings.dp.callback_query_handler(callback.add_delete_work_period.filter(status="Add"))
async def callback_work_report(call: types.CallbackQuery, callback_data: dict):
    today = datetime.datetime.today()
    days = InlineKeyboardMarkup(row_width=5)
    for k in range(1, today.day + 1):
        days.insert(callback.days_btn_callback[k])
    days.insert(callback.date_back_callback)

    await call.message.edit_text("Choose the start working time using the constructor\nThis is a date and time constructor, pick the day you want", 
                                    reply_markup=days)


# <<<<<<<<<<<<<<<<<< Добавление дня в конструкторе добавления отработанного периода  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.date_callback.filter(time_unit="day"))
async def callback_work_report(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])

    today = datetime.datetime.today()
    work.date_callback_constructor = "{2}.{1}.{0}".format(today.year, tr_val(today.month), tr_val(callback_data.get("val")))
    
    hours = InlineKeyboardMarkup(row_width=6)
    if (int(callback_data.get("val")) == today.day):
        h = today.hour + 1
    else:
        h = 24

    for k in range(h):
        hours.insert(callback.hours_btn_callback[k])
    
    await call.message.edit_text("Date: {}\nNow choose the hour you want".format(work.date_callback_constructor), reply_markup=hours)


# <<<<<<<<<<<<<<<<<< Добавление часов в конструкторе добавления отработанного периода  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.date_callback.filter(time_unit="hour"))
async def save_hour_date_callback(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])
    if work.start_constructor_done:
        mes = "Date: {}\mTime: {} - ".format(
            work.date_callback_constructor,
            work.time_callback_constructor
        )
    else: 
        mes = "Date: {}\nTime ".format(work.date_callback_constructor)

    work.time_callback_constructor = tr_val(callback_data.get("val"))
    
    mins = InlineKeyboardMarkup(row_width=6)
    for k in range(60):
        mins.insert(callback.mins_btn_callback[k])
    
    await call.message.edit_text(mes + "{}.\nNow choose the right minute".format(
                                                                        work.time_callback_constructor
                                                                    ), 
                                                            reply_markup=mins)


# <<<<<<<<<<<<<<<<<< Добавление минут в конструкторе добавления отработанного периода  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.date_callback.filter(time_unit="min"))
async def save_min_date_callback(call: types.CallbackQuery, callback_data: dict):
    work = get_work_time(settings, call.from_user["id"])

    work.time_callback_constructor += ":{}".format(tr_val(callback_data.get("val")))

    if not work.start_constructor_done:
        work.callback_start_date_working = work.get_day_from(work.date_callback_constructor)
        work.callback_start_time_working = work.get_one_time_from(work.time_callback_constructor.replace(":", ".") + ".00")
        work.start_constructor_done = True

        today = datetime.datetime.today()
        hours = InlineKeyboardMarkup(row_width=6)

        for k in range(24):
            hours.insert(callback.hours_btn_callback[k])
        
        await call.message.edit_text("Great, now choose the end working time\n" +\
                                    "\n❗❗❗If the start time of work is later than the" +\
                                    " end of work, it will be considered that you" +
                                    " have worked until the next day.❗❗❗\n\nDate: {}\nTime: {}\n".format(
                                                                        work.date_callback_constructor,
                                                                        work.time_callback_constructor),
                                        reply_markup=hours)
    else:
        work.callback_end_time_working = work.get_one_time_from(work.time_callback_constructor.replace(":", ".") + ".00")
        work.start_constructor_done = False
        delta = work.get_difference_betwen(
                work.callback_start_time_working,
                work.callback_end_time_working
            )
        h, m, s = map(int, str(work.customer_db.get_time_zone(work.user_id)).split(":"))
        work.save_spec_data(call.from_user["id"], 
                    datetime.datetime.combine(work.callback_start_date_working.date(), work.callback_start_time_working.time()) - datetime.timedelta(hours=h, minutes=m),
                    datetime.datetime.combine(work.callback_start_date_working.date(), work.callback_start_time_working.time()) + delta - datetime.timedelta(hours=h, minutes=m))

        delete_callback = InlineKeyboardMarkup(row_width=1)
        delete_callback.insert(callback.get_delete_work_btn_callback("Back"))

        await call.message.edit_text("Date: {}\nTime: {}\nInterval: {}\n\nData saved".format(
            work.date_callback_constructor,
            str(work.callback_start_time_working.time())[:-3] + " - " + str(work.callback_end_time_working.time())[:-3],
            str(delta)[:-3]
        ), reply_markup=delete_callback)


# <<<<<<<<<<<<<<<<<< Отслеживания кликов нумерованного checkout'а  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.checkout_nums_callback.filter(status="reminder_push_up"))
async def check_checkout(call: types.CallbackQuery, callback_data: dict):
    mes, num = call.message.text.split(": ")
    num = int(num.split(" ")[0]) + int(callback_data["val"])

    v = int(callback_data["btns_num"]) - 1

    if v > 0:
        reminder_push_up = InlineKeyboardMarkup(row_width=4)
        for k in range(v): reminder_push_up.insert(callback.get_checkout_push_up_btn_callback(v))

        await call.message.edit_text(mes + ": " + str(num) + " done", reply_markup=reminder_push_up)
    else:
        await call.message.edit_text(mes + ": " + str(num) + " done ✅")


# <<<<<<<<<<<<<<<<<< Отслеживания кликов checkout'а  >>>>>>>>>>>>>>>>>>
@settings.dp.callback_query_handler(callback.checkout_callback.filter(status="reminder"))
async def check_checkout(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_text(call.message.text + "\n\nDone ✅")


# <<<<<<<<<<<<<<<<<< This month worked time >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler(Text(equals='month', ignore_case=True))
async def cmd_start(message: types.Message):
    work = get_work_time(settings, message.from_user["id"])
    await message.answer(work.get_finfo_day_sum(message.from_user["id"], month=True))


# <<<<<<<<<<<<<<<<<< don't understand >>>>>>>>>>>>>>>>>>
@settings.dp.message_handler()
async def get_stat(message: types.Message):
    work = get_work_time(settings, message.from_user["id"])
    await message.answer("Sorry, i don't understand, type /start")


start_time = time.time()
if __name__ == "__main__":
    db = BackupDBC(settings.db_data)
    # ! Need to convert resume_work[1] to datetime.datetime
    resume_work = db.get_all_rows()  

    for row in resume_work:
        create_work_time(settings, row[0], row[1])
    
    executor.start_polling(settings.dp, skip_updates=True, on_startup=on_startup)