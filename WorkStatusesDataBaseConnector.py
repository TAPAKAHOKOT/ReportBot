
from DataBaseConnector import DataBaseConnector
from Settings import Settings
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class WorkStatusesDataBaseConnector(DataBaseConnector):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        
        self.user_status_tabel_name = "users_work_statuses"

        # self.create_table(self.user_status_tabel_name)

    
    def create_table(self, name):
        logging.info("Start creating table %s" % name)
        try:
            
            connection = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.db_name)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = connection.cursor()

            query = '''CREATE TABLE {}
                        (id INT PRIMARY KEY NOT NULL,
                        user_id INT NOT NULL,
                        tag TEXT NOT NULL,
                        status TEXT NOT NULL); '''.format(name)

            cursor.execute(query)
            connection.commit()
        except (Exception, Error) as error:
            logging.error("Create table %s error: %s" % (name, error))
        finally:
            if connection:
                cursor.close()
                connection.close()
                logging.info("Connection closed for table %s" % name)
    

    def add_row(self, user_id: int, tag: str, status: str):
        logging.info("Start adding user status for %s: succesfull" % user_id)

        self.cursor.execute("SELECT MAX(id) from %s" % self.user_status_tabel_name)
        max_id = self.cursor.fetchall()[0][0]
        max_id = 0 if max_id is None else max_id

        insert_query = """ INSERT INTO users_work_statuses (id, user_id, tag, status) VALUES (%s, %s, %s, %s)"""  
        inp_tuple = (max_id+1, user_id, tag, status)

        self.cursor.execute(insert_query, inp_tuple)
        self.connection.commit()
        logging.info("End adding user status for %s: succesfull" % user_id)
    

    def get_user_status(self, user_id: int) -> list:
        query = "SELECT tag, status FROM %s WHERE user_id=%s" % (self.user_status_tabel_name, user_id)

        self.cursor.execute(query)
        return self.cursor.fetchall()
    

    def set_tag(self, user_id:int, tag:str):
        self.cursor.execute("UPDATE users_work_statuses SET tag=%s WHERE user_id=%s", 
                    (tag, user_id))
    
    
    def set_status(self, user_id:int, status:str):
        self.cursor.execute("UPDATE users_work_statuses SET status=%s WHERE user_id=%s", 
                    (status, user_id))
                