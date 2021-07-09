from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import logging

class StateStorageDBC(DataBaseConnector):
    def __init__(self,  set_dict: dict):
        super().__init__(set_dict)
        
        self.tabel_name = "state_storage"
        self.add_row_query = """INSERT INTO state_storage(customer_id, name_tag, name_status) VALUES (%s, %s, %s)"""
        create_table_query = """CREATE TABLE IF NOT EXISTS state_storage(
                                customer_id INT PRIMARY KEY,
                                name_tag VARCHAR(128),
                                name_status VARCHAR(32));"""
        self.create_table(self.tabel_name, create_table_query)
    

    def get_user_state(self, customer_id: int) -> list:
        self.cursor.execute(f"SELECT name_tag, name_status FROM {self.tabel_name} WHERE user_id={customer_id}")
        return self.cursor.fetchall()
    

    def set_tag(self, customer_id: int, tag: str):
        self.cursor.execute(f"UPDATE {self.tabel_name} SET tag='{tag}'' WHERE user_id={customer_id}")
    
    
    def set_status(self, customer_id: int, status: str):
        self.cursor.execute(f"UPDATE {self.tabel_name} SET status='{status}'' WHERE user_id={customer_id}")