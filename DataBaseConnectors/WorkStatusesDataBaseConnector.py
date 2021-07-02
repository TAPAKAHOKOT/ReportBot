from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class WorkStatusesDataBaseConnector(DataBaseConnector):
    def __init__(self,  set_dict: dict):
        super().__init__(set_dict)
        
        self.tabel_name = "users_work_statuses"
        self.add_row_query = """INSERT INTO users_work_statuses (user_id, tag, status) VALUES (%s, %s, %s)"""

        create_table_query = '''CREATE TABLE IF NOT EXISTS {}
                        (id INT PRIMARY KEY NOT NULL,
                        user_id INT NOT NULL,
                        tag TEXT NOT NULL,
                        status TEXT NOT NULL); '''.format(self.tabel_name)

        self.create_table(self.tabel_name, create_table_query)
    

    def get_user_status(self, user_id: int) -> list:
        query = "SELECT tag, status FROM %s WHERE user_id=%s" % (self.tabel_name, user_id)

        self.cursor.execute(query)
        return self.cursor.fetchall()
    

    def set_tag(self, user_id:int, tag:str):
        self.cursor.execute("UPDATE {} SET tag=%s WHERE user_id=%s".format(self.tabel_name), 
                    (tag, user_id))
    
    
    def set_status(self, user_id:int, status:str):
        self.cursor.execute("UPDATE {} SET status=%s WHERE user_id=%s".format(self.tabel_name), 
                    (status, user_id))
                