
import datetime
from time import sleep
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

class WorkTagHistoryDataBaseConnector:
	def __init__(self):
		self.user = "postgres"
		self.password = "4608"
		self.host="127.0.0.1"
		self.port="5432"
		self.db_name = "my_test_py_database"
		self.tag_history_tabel_name = "users_tag_history"

		self.create_table(self.tag_history_tabel_name)

		self.connection = psycopg2.connect(user=self.user,
										password=self.password,
										host=self.host,
										port=self.port,
										database=self.db_name)
		self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		self.cursor = self.connection.cursor()
	
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
						call_time TIMESTAMP NOT NULL);'''.format(name)

			cursor.execute(query)
			connection.commit()
		except (Exception, Error) as error:
			logging.error("Create table %s error: %s" % (name, error))
		finally:
			if connection:
				cursor.close()
				connection.close()
				logging.info("Connection closed for table %s" % name)
	
	def add_row(self, user_id: int, tag: str, call_time: datetime.datetime):
		logging.info("Start adding user tag in tag history for %s: succesfull" % user_id)

		self.cursor.execute("SELECT MAX(id) from %s" % self.tag_history_tabel_name)
		max_id = self.cursor.fetchall()[0][0]
		max_id = 0 if max_id is None else max_id

		insert_query = """ INSERT INTO users_tag_history (id, user_id, tag, call_time) VALUES (%s, %s, %s, %s)"""  
		inp_tuple = (max_id+1, user_id, tag, call_time)

		self.cursor.execute(insert_query, inp_tuple)
		self.connection.commit()
		logging.info("End adding user in tag history tag for %s: succesfull" % user_id)
	
	def get_user_tag_history(self, user_id: int):
		query = "SELECT tag, call_time FROM %s WHERE user_id=%s ORDER BY call_time DESC" % (self.tag_history_tabel_name, user_id)

		self.cursor.execute(query)
		res = ""
		for el in self.cursor.fetchall():
			res += "#" + el[0] + "\n"
		return res
	
	def delete_last_tag_from_history(self, user_id: int):
		query = """DELETE FROM users_tag_history
					WHERE user_id=%s AND call_time=(
						SELECT call_time 
						FROM users_tag_history
						ORDER BY call_time
						LIMIT 1
					)""" % user_id

		self.cursor.execute(query)
	
	def get_count_of_history(self, user_id: int):
		query = "SELECT COUNT(*) FROM users_tag_history WHERE user_id=%s" % user_id
		self.cursor.execute(query)
		return self.cursor.fetchall()[0][0]
				

w = WorkTagHistoryDataBaseConnector()

w.delete_last_tag_from_history(123)
w.delete_last_tag_from_history(123)
w.delete_last_tag_from_history(123)

print(w.get_user_tag_history(123))