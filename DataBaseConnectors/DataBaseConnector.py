from Settings import Settings
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class DataBaseConnector:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.user = self.settings.db_user
        self.password = self.settings.db_password
        self.host = self.settings.db_host
        self.port = self.settings.db_port
        self.db_name = self.settings.db_name

        self.connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.db_name)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()


    def create_db(self, name):
        logging.info("Start creating database %s" % name)
        try:
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = connection.cursor()
            sql_create_database = 'create database ' + name
            cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            logging.error("Create database %s error: %s" % (name, error))
        finally:
            if connection:
                cursor.close()
                connection.close()
                logging.info("Connection closed for database %s" % name)