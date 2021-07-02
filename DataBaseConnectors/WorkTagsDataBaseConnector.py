from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import datetime
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class WorkTagsDataBaseConnector(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.tabel_name = "users_tags"
        self.add_row_query = """INSERT INTO users_tags (user_id, tag, call_time) VALUES (%s, %s, %s)"""

        create_table_query = '''CREATE TABLE IF NOT EXISTS {}
                        (id INT PRIMARY KEY NOT NULL,
                        user_id INT NOT NULL,
                        tag TEXT NOT NULL,
                        call_time TIMESTAMP NOT NULL);'''.format(self.tabel_name)

        self.create_table(self.tabel_name, create_table_query)
    

    def get_user_tag_history(self, user_id: int) -> list:
        query = "SELECT tag, call_time FROM %s WHERE user_id=%s ORDER BY call_time DESC" % (self.tabel_name, user_id)

        self.cursor.execute(query)
        res = []
        for el in self.cursor.fetchall():
            res.append(el[0])
        return res
    

    def delete_last_tag_from_history(self, user_id: int):
        query = """DELETE FROM {table}
                    WHERE user_id={id} AND call_time=(
                        SELECT call_time 
                        FROM {table}
                        ORDER BY call_time
                        LIMIT 1
                    )""".format(table=self.tabel_name, id=user_id)

        self.cursor.execute(query)
    
    
    def get_count_of_history(self, user_id: int) -> int:
        query = "SELECT COUNT(*) FROM {0} WHERE user_id={1}".format(self.tabel_name, user_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]


                

# w = WorkTagsDataBaseConnector()

# print(w.get_count_of_history(123) == 0)