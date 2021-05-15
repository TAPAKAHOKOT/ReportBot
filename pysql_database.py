
import datetime
from time import sleep
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DataBaseConnector:
	def __init__(self):
		self.user = "postgres"
		self.password = "4608"
		self.host="127.0.0.1"
		self.port="5432"
		self.db_name = "my_test_py_database"
		self.works_table_name = "works_times"

		self.create_db()
		self.create_table()

		self.connection = psycopg2.connect(user=self.user,
										password=self.password,
										host=self.host,
										port=self.port,
										database=self.db_name)
		self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		self.cursor = self.connection.cursor()

		self.tagf = lambda t: "\'" + t + "\'"
		self.this_week_asking = """(start_time >= date_trunc('week', CURRENT_TIMESTAMP) 
		and start_time < date_trunc('week', CURRENT_TIMESTAMP + interval '1 week'))"""
		self.last_week_asking = """(start_time >= date_trunc('week', CURRENT_TIMESTAMP - interval '1 week') 
		and start_time < date_trunc('week', CURRENT_TIMESTAMP))"""
		self.select_columns = "user_id, tag, start_time, end_time"

	def create_db(self):
		try:
			connection = psycopg2.connect(user=self.user,
										password=self.password,
										host=self.host,
										port=self.port)
			connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

			cursor = connection.cursor()
			sql_create_database = 'create database ' + self.db_name
			cursor.execute(sql_create_database)
		except (Exception, Error) as error:
			print(error)
		finally:
			if connection:
				cursor.close()
				connection.close()
	
	def create_table(self):
		try:

			connection = psycopg2.connect(user=self.user,
										password=self.password,
										host=self.host,
										port=self.port,
										database=self.db_name)
			connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

			cursor = connection.cursor()

			create_table_query = '''CREATE TABLE {}
								  (id INT PRIMARY KEY NOT NULL,
								  user_id INT NOT NULL,
								  tag TEXT NOT NULL,
								  status TEXT NOT NULL,
								  start_time TIMESTAMP NOT NULL,
								  end_time TIMESTAMP NOT NULL); '''.format(self.works_table_name)

			cursor.execute(create_table_query)
			connection.commit()
		except (Exception, Error) as error:
			print(error)
		finally:
			if connection:
				cursor.close()
				connection.close()
	
	def add_row(self, user_id: int, tag: str, status: str, start_time: datetime.datetime, end_time: datetime.datetime):
		self.cursor.execute("SELECT MAX(id) from %s" % self.works_table_name)
		max_id = self.cursor.fetchall()[0][0]
		max_id = 0 if max_id is None else max_id

		insert_query = """ INSERT INTO works_times (id, user_id, tag, status, start_time, end_time) VALUES (%s, %s, %s, %s, %s, %s)"""   
		inp_tuple = (max_id+1, user_id, tag, status, start_time, end_time)
		self.cursor.execute(insert_query, inp_tuple)

		self.connection.commit()
	
	def get_all_rows(self, u_id: int, status: str):
		self.cursor.execute("SELECT %s FROM %s WHERE user_id=%s AND status=%s ORDER BY start_time" %\
			(self.select_columns, self.works_table_name, u_id, self.tagf(status)))
		return self.cursor.fetchall()
	
	def get_all_rows_by_tag(self, tag: str, u_id: int, status: str):
		self.cursor.execute("SELECT %s FROM %s WHERE tag=%s AND user_id=%s AND status=%s ORDER BY start_time" %\
			(self.select_columns, self.works_table_name, self.tagf(tag), u_id, self.tagf(status)))
		return self.cursor.fetchall()

	def get_this_week_rows(self, u_id: int, status: str):
		self.cursor.execute("SELECT %s FROM %s WHERE %s AND user_id=%s AND status=%s ORDER BY start_time" %\
			(self.select_columns, self.works_table_name, self.this_week_asking, u_id, self.tagf(status)))
		return self.cursor.fetchall()

	def get_this_week_rows_by_tag(self, tag: str, u_id: int, status: str):
		self.cursor.execute("SELECT %s FROM %s WHERE tag=%s AND %s AND user_id=%s AND status=%s GROUP BY start_time ORDER BY start_time" %\
			(self.select_columns, self.works_table_name, self.tagf(tag), self.this_week_asking, u_id, self.tagf(status)))
		return self.cursor.fetchall()
	
	def get_last_week_rows(self, u_id: int, status: str):
		self.cursor.execute("SELECT %s FROM %s WHERE %s AND user_id=%s AND status=%s ORDER BY start_time" %\
			(self.select_columns, self.works_table_name, self.last_week_asking, u_id, self.tagf(status)))
		return self.cursor.fetchall()

	def get_last_week_rows_by_tag(self, tag: str, u_id: int, status: str):
		self.cursor.execute("SELECT %s FROM %s WHERE tag=%s AND %s AND user_id=%s AND status=%s GROUP BY start_time ORDER BY start_time" %\
			(self.select_columns, self.works_table_name, self.tagf(tag), self.last_week_asking, u_id, self.tagf(status)))
		return self.cursor.fetchall()
	
	def close_connection(self):
		if self.connection:
			self.cursor.close()
			self.connection.close()
	
	def test_clear_table(self):
		self.cursor.execute("DELETE FROM %s" % self.works_table_name)
	
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