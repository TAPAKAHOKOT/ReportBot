from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import datetime
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class WorksStartWorkDataBaseConnector(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.table_name = "start_wowrking_time"
        self.add_row_query = """INSERT INTO start_wowrking_time (user_id, start_time) VALUES (%s, %s)"""

        self.tagf = lambda t: "\'" + t + "\'"

        create_table_query = '''CREATE TABLE IF NOT EXISTS {}
                                    (user_id INT PRIMARY KEY NOT NULL,
                                    start_time TIMESTAMP NOT NULL); '''.format(self.table_name)

        self.create_table(self.table_name, create_table_query)


    def get_all_rows(self, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE user_id=%s AND status=%s ORDER BY start_time" %\
            (self.select_columns, self.table_name, u_id, self.tagf(status)))
        return self.cursor.fetchall()
    

    def delete_row(self, u_id: int):
        self.cursor.execute("DELETE FROM %s WHERE user_id=%s" % (self.table_name, u_id))