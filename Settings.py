import logging
from aiogram.types.inline_keyboard import InlineKeyboardButton
from binance.client import Client
import codecs
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_data import CallbackData
import os 
import json

class Settings:
    def __init__(self):
        # ! <<< TESTING >>>
        TESTING = True
        # ! <<< TESTING >>>

        # database connectiong settings
        self.db_user = "postgres"
        self.db_password = "4608"
        self.db_host="127.0.0.1"
        self.db_port="5432"
        self.db_name = "my_test_py_database"
        self.db_data = {"usr": self.db_user,
                        "pwd": self.db_password,
                        "host": self.db_host,
                        "port": self.db_port,
                        "name": self.db_name}

        # Logging settings
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        file_log = logging.FileHandler('logs/Log.log', mode='w')
        console_out = logging.StreamHandler()
        logging.basicConfig(level=logging.INFO, 
                handlers=(file_log, console_out),
                format='%(asctime)s %(levelname)s:%(message)s',
                datefmt='%H:%M:%S')
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        logging.info("Init settigs in the %s mode" % TESTING)

        self.b_vers = 2.0
        print("Bot version " + str(self.b_vers))

        way = "/".join(os.getcwd().replace("\\", "/").split("/")[:-1])

        with open(way + '/botsAPi.txt') as json_file:
            data = json.load(json_file)

        self.api_key = data["b_api_key"]
        self.api_secret = data["b_api_secret"]

        self.client = Client(self.api_key, self.api_secret)

        self.my_id = 472914986
        self.mom_id = 472914986

        self.main_bot_token = data["clear_reports_sender_bot"]
        self.test_bot_token = data["TapakahoBot"]
        self.token = self.test_bot_token if TESTING else self.main_bot_token

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

        self.csv_dir = "csv_data"
        self.csv_filename = "data.csv"

        self.work_time_dict = {}

        logging.info("Settings are initialized")

    def clear_line(self, line):
        return line.replace("\n", "").replace(" ", "")

    def fill_data(self):
        logging.info("Start filling data")
        with codecs.open("data/send_data.txt", encoding = 'utf-8', mode = 'r') as file:
            line = file.readline()
            while line:
                logging.info("Filling line: " + line)
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
        logging.info("End filling data")