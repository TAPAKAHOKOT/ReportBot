from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import logging

class WorksMainDataBaseConnector(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.tabel_name = "works_times"
        self.add_row_query = """INSERT INTO works_times (user_id, tag, status, start_time, end_time) VALUES (%s, %s, %s, %s, %s)"""

        self.tagf = lambda t: "\'" + t + "\'"
        self.this_week_asking = """(start_time >= date_trunc('week', CURRENT_TIMESTAMP) 
        and start_time < date_trunc('week', CURRENT_TIMESTAMP + interval '1 week'))"""
        self.last_week_asking = """(start_time >= date_trunc('week', CURRENT_TIMESTAMP - interval '1 week') 
        and start_time < date_trunc('week', CURRENT_TIMESTAMP))"""
        self.this_month_asking = """(start_time >= date_trunc('month', CURRENT_TIMESTAMP) 
        and start_time < date_trunc('month', CURRENT_TIMESTAMP + interval '1 month'))"""
        self.select_columns = "user_id, tag, start_time, end_time, id"

        create_table_query = '''CREATE TABLE IF NOT EXISTS {}
                                    (id INT PRIMARY KEY NOT NULL,
                                    user_id INT NOT NULL,
                                    tag TEXT NOT NULL,
                                    status TEXT NOT NULL,
                                    start_time TIMESTAMP NOT NULL,
                                    end_time TIMESTAMP NOT NULL); '''.format(self.tabel_name)
        
        self.create_table(self.tabel_name, create_table_query)
    

    def get_all_rows(self, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE user_id=%s AND status=%s ORDER BY start_time" %\
            (self.select_columns, self.tabel_name, u_id, self.tagf(status)))
        return self.cursor.fetchall()
    
    
    def get_all_rows_by_tag(self, tag: str, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE tag=%s AND user_id=%s AND status=%s ORDER BY start_time" %\
            (self.select_columns, self.tabel_name, self.tagf(tag), u_id, self.tagf(status)))
        return self.cursor.fetchall()


    def get_this_week_rows(self, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE %s AND user_id=%s AND status=%s ORDER BY to_char(start_time, 'YYYY-MM-DD'), tag, start_time" %\
            (self.select_columns, self.tabel_name, self.this_week_asking, u_id, self.tagf(status)))
        return self.cursor.fetchall()


    def get_this_week_rows_by_tag(self, tag: str, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE tag=%s AND %s AND user_id=%s AND status=%s GROUP BY start_time ORDER BY start_time" %\
            (self.select_columns, self.tabel_name, self.tagf(tag), self.this_week_asking, u_id, self.tagf(status)))
        return self.cursor.fetchall()
    

    def get_last_week_rows(self, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE %s AND user_id=%s AND status=%s ORDER BY to_char(start_time, 'YYYY-MM-DD'), tag, start_time" %\
            (self.select_columns, self.tabel_name, self.last_week_asking, u_id, self.tagf(status)))
        return self.cursor.fetchall()


    def get_last_week_rows_by_tag(self, tag: str, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE tag=%s AND %s AND user_id=%s AND status=%s GROUP BY start_time ORDER BY start_time" %\
            (self.select_columns, self.tabel_name, self.tagf(tag), self.last_week_asking, u_id, self.tagf(status)))
        return self.cursor.fetchall()
    

    def get_this_month_rows(self, u_id: int, status: str) -> list:
        self.cursor.execute("SELECT %s FROM %s WHERE %s AND user_id=%s AND status=%s ORDER BY start_time" %\
            (self.select_columns, self.tabel_name, self.this_month_asking, u_id, self.tagf(status)))
        return self.cursor.fetchall()
    

    def delete_row_by_id(self, id: int):
        print("DELETE FROM {} WHERE id={}".format(self.tabel_name, id))
        self.cursor.execute("DELETE FROM {} WHERE id={}".format(self.tabel_name, id))


# db = DataBaseConnector()

# db.add_row(472914986, "testing", "studying",
# 	datetime.datetime(2021, 5, 8, 13, 33, 0, 0), 
# 	datetime.datetime(2021, 5, 8, 13, 43, 0, 0))
# db.add_row(472914986, "testing", "studying",
# 	datetime.datetime(2021, 5, 3, 13, 33, 0, 0), 
# 	datetime.datetime(2021, 5, 3, 13, 43, 0, 0))
# db.test_delete_table()
# db.test_clear_table()

# for k in db.get_this_week_rows(1234): print(k)
# print("TAG")
# for k in db.get_this_week_rows_by_tag("testing", 4444): print(k)