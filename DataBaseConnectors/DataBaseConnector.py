import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class DataBaseConnector:
    def __init__(self, set_dict: dict):
        self.add_row_query = ""
        self.table_name = ""

        self.user = set_dict["usr"]
        self.password = set_dict["pwd"]
        self.host = set_dict["host"]
        self.port = set_dict["port"]
        self.db_name = set_dict["name"]

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
    
    def create_table(self, name, query):
        logging.info("Start creating table %s" % name)
        try:
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.db_name)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = connection.cursor()

            cursor.execute(query)
            connection.commit()
        except (Exception, Error) as error:
            logging.error("Create table %s error: %s" % (name, error))
        finally:
            if connection:
                cursor.close()
                connection.close()
                logging.info("Connection closed for table %s" % name)
    
    def add_row(self, *args):
        logging.info("Start adding row [%s]" % " ".join([str(k) for k in args]))
        
        self.cursor.execute(self.add_row_query, args)
        self.connection.commit()

        logging.info("End adding row [%s]" % " ".join([str(k) for k in args]))
    
    def get_all_rows(self) -> list:
        self.cursor.execute("SELECT * FROM %s" % self.table_name)
        return self.cursor.fetchall()
    
    def clear_table(self):
        self.cursor.execute("DELETE FROM %s" % self.tabel_name)
    
    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()