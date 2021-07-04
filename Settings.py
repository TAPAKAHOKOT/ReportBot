import logging
from binance.client import Client
from aiogram import Bot, Dispatcher
from CallbackItems import CallbackItems
import json

class Settings:
    def __init__(self, testing: bool):
        # ! <<< TESTING >>>
        TESTING = testing
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

        self.b_vers = "3.0.6"
        print("Bot version " + str(self.b_vers))

        with open('botsAPi.txt') as json_file:
            data = json.load(json_file)

        self.api_key = data["b_api_key"]
        self.api_secret = data["b_api_secret"]

        self.client = Client(self.api_key, self.api_secret)

        self.my_id = 472914986
        self.mom_id = 966892190

        self.main_bot_token = data["clear_reports_sender_bot"]
        self.test_bot_token = data["TapakahoBot"]
        self.token = self.test_bot_token if TESTING else self.main_bot_token

        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)

        self.work_time_dict = {}

        self.callback = CallbackItems()

        logging.info("Settings are initialized")