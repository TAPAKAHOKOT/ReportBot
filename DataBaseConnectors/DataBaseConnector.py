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
    

    def update_db(self):
        query = """CREATE TABLE IF NOT EXISTS customer(
                    customer_id INT PRIMARY KEY,
                    name_customer VARCHAR(64),
                    time_zone interval DEFAULT '3 hours'
                );

                INSERT INTO customer(customer_id)
                    SELECT DISTINCT user_id
                    FROM works_times
                    WHERE user_id NOT IN (SELECT customer_id FROM customer);

                CREATE TABLE IF NOT EXISTS tag(
                    tag_id SERIAL PRIMARY KEY,
                    name_tag VARCHAR(128),
                    customer_id INT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customer (customer_id) 
                );

                INSERT INTO tag(name_tag, customer_id)
                    SELECT u.tag, user_id
                    FROM users_tags u
                    WHERE (u.tag, user_id) NOT IN (SELECT name_tag, customer_id FROM tag);

                CREATE TABLE IF NOT EXISTS term(
                    term_id SERIAL PRIMARY KEY,
                    customer_id INT NOT NULL,
                    name_tag VARCHAR(128),
                    name_status VARCHAR(32),
                    start_time TIMESTAMP WITHOUT TIME ZONE,
                    end_time TIMESTAMP WITHOUT TIME ZONE
                );

                INSERT INTO term(customer_id, name_tag, name_status, start_time, end_time)
                    SELECT user_id, tag, status, start_time, end_time
                    FROM works_times
                    WHERE (user_id, tag, status, start_time, end_time) NOT IN (
                        SELECT term_id, name_tag, name_status, start_time, end_time FROM term);

                UPDATE term
                SET name_tag = concat('#', name_tag)
                WHERE name_tag NOT LIKE '#%';

                CREATE TABLE IF NOT EXISTS state_storage(
                    customer_id INT PRIMARY KEY,
                    name_tag VARCHAR(128),
                    name_status VARCHAR(32)
                );

                INSERT INTO state_storage(customer_id, name_tag, name_status)(
                    SELECT user_id, tag, status
                    FROM users_work_statuses
                    WHERE user_id NOT IN (SELECT customer_id FROM state_storage)
                );

                CREATE TABLE IF NOT EXISTS backup(
                    customer_id INT PRIMARY KEY,
                    start_time TIMESTAMP WITHOUT TIME ZONE,
                    FOREIGN KEY (customer_id) REFERENCES customer (customer_id) 
                );

                INSERT INTO backup(customer_id, start_time)
                    SELECT user_id, start_time
                    FROM start_working_time
                    WHERE user_id NOT IN (SELECT customer_id FROM backup);"""


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