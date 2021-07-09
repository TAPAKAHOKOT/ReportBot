from DataBaseConnectors.DataBaseConnector import DataBaseConnector
import logging

class WorkTagsDataBaseConnector(DataBaseConnector):
    def __init__(self, set_dict: dict):
        super().__init__(set_dict)

        self.tabel_name = "tag"
        self.add_row_query = """INSERT INTO tag(name_tag, customer_id) VALUES (%s, %s)"""
        create_table_query = """CREATE TABLE IF NOT EXISTS tag(
                                tag_id SERIAL PRIMARY KEY,
                                name_tag VARCHAR(128),
                                customer_id INT NOT NULL,
                                FOREIGN KEY (customer_id) REFERENCES customer (customer_id));"""
        self.create_table(self.tabel_name, create_table_query)
    

    def get_tags(self, customer_id: int) -> list:
        self.cursor.execute(f"SELECT name_tag, customer_id FROM {self.tabel_name} WHERE customer_id={customer_id} ORDER BY tag_id DESC")
        return [el[0] for el in self.cursor.fetchall()]
    

    def delete_last_tag(self, customer_id: int):
        query = """DELETE FROM {table}
                    WHERE user_id={id} AND tag_id=(
                        SELECT tag_id 
                        FROM {table}
                        WHERE customer_id={id}
                        ORDER BY tag_id
                        LIMIT 1
                    )""".format(table=self.tabel_name, id=customer_id)
        self.cursor.execute(query)
    
    
    def get_count(self, customer_id: int) -> int:
        query = f"SELECT COUNT(tag_id) FROM {self.tabel_name} WHERE customer_id={customer_id}"
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]