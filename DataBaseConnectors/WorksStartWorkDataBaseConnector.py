
import datetime
from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class WorksStartWorkDataBaseConnector(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.table_name = "start_wowrking_time"

        self.tagf = lambda t: "\'" + t + "\'"

        self.create_table(self.table_name)
    

    def create_table(self, name, query=None):
        logging.info("Start creating table %s" % name)
        try:
            
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.db_name)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = connection.cursor()

            if query is None:
                create_table_query = '''CREATE TABLE {}
                                    (user_id INT PRIMARY KEY NOT NULL,
                                    start_time TIMESTAMP NOT NULL); '''.format(name)
            else:
                create_table_query = query

            cursor.execute(create_table_query)
            connection.commit()
        except (Exception, Error) as error:
            logging.error("Create table %s error: %s" % (name, error))
        finally:
            if connection:
                cursor.close()
                connection.close()
                logging.info("Connection closed for table %s" % name)


    def add_row(self, user_id: int, start_time: datetime.datetime):
        logging.info("Start adding row [u_id=%s, start_time=%s]" % (user_id, str(start_time)))

        insert_query = """ INSERT INTO works_times (user_id, start_time) VALUES (%s, %s)"""   
        self.cursor.execute(insert_query, (user_id, start_time))

        self.connection.commit()
        logging.info("End adding row for %s: succesfull" % user_id)
    

    def get_all_rows(self, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE user_id=%s AND status=%s ORDER BY start_time" %\
            (self.select_columns, self.table_name, u_id, self.tagf(status)))
        return self.cursor.fetchall()
    

    def delete_row(self, u_id: int):
        self.cursor.excecute("DELETE FROM %s WHERE user_id=%s", (self.table_name, u_id))


    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
    
    
    def test_clear_table(self):
        self.cursor.execute("DELETE FROM %s" % self.table_name)
