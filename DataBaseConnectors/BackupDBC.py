from DataBaseConnectors.DataBaseConnector import DataBaseConnector

class BackupDBC(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.table_name = "backup"
        self.add_row_query = """INSERT INTO backup(customer_id, start_time) VALUES (%s, %s)"""
        create_table_query = """CREATE TABLE IF NOT EXISTS backup(
                                customer_id INT PRIMARY KEY,
                                start_time TIMESTAMP WITHOUT TIME ZONE,
                                FOREIGN KEY (customer_id) REFERENCES customer (customer_id));"""
        self.create_table(self.table_name, create_table_query)
    

    def delete_last(self, customer_id: int):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE customer_id={customer_id}")