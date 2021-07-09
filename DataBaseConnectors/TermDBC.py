from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import logging

class TermDBC(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.tabel_name = "term"
        self.add_row_query = """INSERT INTO term(customer_id, name_tag, name_status, start_time, end_time) VALUES (%s, %s, %s, %s, %s)"""
        self.periods = {
            "this_week": """start_time BETWEEN date_trunc('week', CURRENT_TIMESTAMP) AND date_trunc('week', CURRENT_TIMESTAMP +  interval '1 week')""",
            "last_week": """start_time BETWEEN date_trunc('week', CURRENT_TIMESTAMP - interval '1 week') AND date_trunc('week', CURRENT_TIMESTAMP)""",
            "this_month": """start_time BETWEEN date_trunc('month', CURRENT_TIMESTAMP) AND date_trunc('month', CURRENT_TIMESTAMP + interval '1 month')"""
        }
        self.select_columns = """DATE(start_time) date, tag, SUM(end_time - start_time), term_id"""
        create_table_query = """CREATE TABLE IF NOT EXISTS term(
                                term_id SERIAL PRIMARY KEY,
                                customer_id INT NOT NULL,
                                name_tag VARCHAR(128),
                                name_status VARCHAR(32),
                                start_time TIMESTAMP WITHOUT TIME ZONE,
                                end_time TIMESTAMP WITHOUT TIME ZONE);"""
        self.create_table(self.tabel_name, create_table_query)
    

    def get_period_rows(self, period: str, status: str):
        query = f"""SELECT {self.select_columns}
                    FROM term
                    WHERE {self.periods[period]} AND status = '{status}'
                    GROUP BY date, tag
                    ORDER BY date, tag;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    

    def delete_row_by_id(self, id: int):
        self.cursor.execute(f"DELETE FROM {self.tabel_name} WHERE term_id={id}")


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