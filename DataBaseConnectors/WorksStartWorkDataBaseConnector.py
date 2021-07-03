from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import logging

class WorksStartWorkDataBaseConnector(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.table_name = "start_working_time"
        self.add_row_query = """INSERT INTO start_working_time (user_id, start_time) VALUES (%s, %s)"""

        self.tagf = lambda t: "\'" + t + "\'"

        create_table_query = '''CREATE TABLE IF NOT EXISTS {}
                                    (user_id INT PRIMARY KEY NOT NULL,
                                    start_time TIMESTAMP NOT NULL); '''.format(self.table_name)

        self.create_table(self.table_name, create_table_query)


    def get_all_rows(self) -> list:
        self.cursor.execute("SELECT * FROM %s" % (self.table_name))
        return self.cursor.fetchall()
    

    def delete_row(self, u_id: int):
        self.cursor.execute("DELETE FROM %s WHERE user_id=%s" % (self.table_name, u_id))