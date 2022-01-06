import logging
from aiogram import Bot, Dispatcher
from CallbackItems import CallbackItems
from json import load as json_load
from dotenv import load_dotenv
from os import (
    getenv,
    mkdir
)

class Settings:
    def __init__(self):
        load_dotenv()

        # ! <<< TESTING >>>
        TESTING = getenv('TESTING') == 'TRUE'
        # ! <<< TESTING >>>

        # database connectiong settings
        self.db_user = getenv('DB_USER')
        self.db_password = getenv('DB_PASSWORD')
        self.db_host = getenv('DB_HOST')
        self.db_port = getenv('DB_PORT')
        self.db_name = getenv('DB_NAME')
        self.db_data = {
            "usr": self.db_user,
            "pwd": self.db_password,
            "host": self.db_host,
            "port": self.db_port,
            "name": self.db_name
        }

        # Logging settings
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            mkdir("logs")
        except FileExistsError:
            pass

        file_log = logging.FileHandler('logs/Log.log', mode='w')
        console_out = logging.StreamHandler()
        logging.basicConfig(level=logging.INFO, 
                handlers=(file_log, console_out),
                format='%(asctime)s %(levelname)s:%(message)s',
                datefmt='%H:%M:%S')
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        logging.info("Init settigs in the %s mode" % TESTING)

        self.b_vers = "3.0.6"
        logging.info("Bot version " + str(self.b_vers))

        with open('botsAPi.txt') as json_file:
            data = json_load(json_file)

        self.my_id = 472914986
        self.mom_id = 966892190

        self.main_bot_token = data["clear_reports_sender_bot"]
        self.test_bot_token = data["TapakahoBot"]
        self.token = self.test_bot_token if TESTING else self.main_bot_token

        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)

        self.work_time_dict = {}

        self.callback = CallbackItems()

        self.all_locations = ["-10", "-8", "-7", "-6", "-5", "-4", "-3:30", "+0", 
                                "+1", "+2", "+3", "+8", "+9:30", "+10"]

        logging.info("Settings are initialized")