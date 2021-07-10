from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import logging

class CustomerDBC(DataBaseConnector):
    def __init__(self,  set_dict: dict):
        super().__init__(set_dict)

        self.tabel_name = "customer"
        self.add_row_query = """INSERT INTO customer (customer_id, name_customer) VALUES (%s, %s)"""
        create_table_query = """CREATE TABLE IF NOT EXISTS customer(
                                customer_id INT PRIMARY KEY,
                                name_customer VARCHAR(64),
                                time_zone interval DEFAULT '3 hours');"""
        self.create_table(self.tabel_name, create_table_query)
    

    def get_customer(self, customer_id) -> list:
        self.cursor.execute("SELECT customer_id FROM customer WHERE customer_id=%s" % customer_id)
        return self.cursor.fetchall()

    def set_time_zone(self, customer_id: int, interval: str):
        self.cursor.execute("UPDATE customer SET time_zone = '%s' WHERE customer_id = %s" % (interval, customer_id))
    
    def get_time_zone(self, customer_id: int):
        self.cursor.execute("SELECT time_zone FROM customer WHERE customer_id=%s" % customer_id)
        return self.cursor.fetchall()[0][0]