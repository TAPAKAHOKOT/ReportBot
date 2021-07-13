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
        self.select_columns_short = """DATE(start_time + time_zone) date, name_tag, SUM(end_time - start_time)"""
        self.select_columns_full = """name_tag, (start_time + time_zone) st, (end_time + time_zone) et, term_id"""
        create_table_query = """CREATE TABLE IF NOT EXISTS term(
                                term_id SERIAL PRIMARY KEY,
                                customer_id INT NOT NULL,
                                name_tag VARCHAR(128),
                                name_status VARCHAR(32),
                                start_time TIMESTAMP WITHOUT TIME ZONE,
                                end_time TIMESTAMP WITHOUT TIME ZONE);"""
        self.create_table(self.tabel_name, create_table_query)
    

    def get_period_rows(self, customer_id: int, period: str, status: str):
        query = f"""SELECT {self.select_columns_short}
                    FROM term JOIN customer USING(customer_id)
                    WHERE {self.periods[period]} AND name_status='{status}' AND customer_id={customer_id}
                    GROUP BY date, name_tag
                    ORDER BY date, name_tag;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_all_periods_rows(self, customer_id: int, period: str, status: str) -> list:
        query = f"""SELECT {self.select_columns_full}
                    FROM term t, customer c
                    WHERE {self.periods[period]} AND name_status='{status}' AND t.customer_id={customer_id} AND  t.customer_id = c.customer_id
                    ORDER BY DATE(start_time), name_tag, st;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    

    def delete_row_by_id(self, id: int):
        self.cursor.execute(f"DELETE FROM {self.tabel_name} WHERE term_id={id}")