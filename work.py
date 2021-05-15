import datetime

from time import sleep, time_ns
from typing import Sequence

from pysql_database import DataBaseConnector

class Work:
    def __init__(self):
        self.timeformat = "%H.%M.%S"
        self.dateformat = "%d.%m.%Y"
        
        self.is_working = False

        self.start_date_working = None
        self.end_date_working = None
        self.start_time_working = None

        self.tag = "testing"
        self.status = "studying"

        self.db = DataBaseConnector()

    def saving_data(self, u_id: int):
        self.db.add_row(u_id, self.tag, self.status, self.start_time_working, self.end_time_working)

    def start_working(self) -> str:
        if self.is_working:
            return "You are already working from {} {}".format(self.start_date_working, self.start_time_working)
        self.is_working = True 
        self.start_time_working = self.get_current_time()
        self.start_date_working = self.get_current_day()

        return "Start working time: " + self.start_time_working.strftime(self.timeformat) + " #" + self.tag
    
    def end_working(self, u_id: int) -> str:
        if not self.is_working:
            return "You aren't working now"
        self.is_working = False
        self.end_time_working = self.get_current_time()
        self.end_date_working = self.get_current_day()

        self.saving_data(u_id)

        return "End working time: {}\nWorking time: {}".format(self.end_time_working.strftime(self.timeformat), str(self.get_difference()).split(".")[0])

    def get_current_day(self) -> datetime.datetime:
        return datetime.datetime.today()
    def get_current_time(self) -> datetime.datetime:
         return datetime.datetime.now()

    def get_time_from(self, line) -> datetime.datetime:
        start, end = line.split("-")

        start = datetime.datetime.strptime(start, self.timeformat)
        end = datetime.datetime.strptime(end, self.timeformat)

        return [start, end]
    
    def get_day_from(self, line) -> datetime.datetime:
        return datetime.datetime.strptime(line, self.dateformat)
    
    def get_difference_betwen(self, s_time, e_time):
        return e_time - s_time if e_time > s_time \
            else e_time - s_time + datetime.timedelta(1)

    def get_difference(self) -> datetime.timedelta:
        return self.end_time_working - self.start_time_working
    
    def get_day_time_formated(self, s_time=None, e_time=None) -> str:
        if not s_time: s_time = self.start_time_working
        if not e_time: e_time = self.end_time_working
        return s_time.strftime(self.timeformat) + " - " + e_time.strftime(self.timeformat)
    
    def get_current_working_info(self):
        if not self.is_working:
            return "You aren't working now"
        delta = str(self.get_difference_betwen(self.start_time_working, self.get_current_time())).split(".")[0]
        return "Start working time: {}\nTime delta: {}".format(self.start_time_working.strftime(self.timeformat), delta)
    
    def get_finfo_day_intervals(self, u_id: int, last_week: bool = False):
        res = "<<<" + self.status.title() + ">>>\n"
        arr = {}
        if last_week:
            info = self.db.get_last_week_rows(u_id, self.status)
        else:
            info = self.db.get_this_week_rows(u_id, self.status)
        s_date = None
        for row in info:
            if s_date is None or s_date.date() != row[2].date():
                s_date = row[2]
                arr[s_date] = {}
            if not (row[1] in arr[s_date].keys()): arr[s_date][row[1]] = []
            delta = str(self.get_difference_betwen(row[2], row[3])).split(".")[0]
            arr[s_date][row[1]].append(self.get_day_time_formated(row[2], row[3]) + " => " + delta)
        
        for key, val in arr.items():
            arr[key] = {k: v for k, v in sorted(val.items(), key=lambda item: item[0])}
        
        for key, val in arr.items():
            res += str(key.strftime(self.dateformat)) + "\n" + "-"*10 + "\n"

            for k, v in val.items():
                res += " "*4 + "#" + k + "\n"
                for el in v:
                    res += " "*8 + el + "\n"
            res += "\n"
        return res if res != "" else "None"
    
    def get_finfo_day_sum(self, u_id: int, last_week: bool = False):
        res = "<<<" + self.status.title() + ">>>\n"
        arr = {}
        if last_week:
            info = self.db.get_last_week_rows(u_id, self.status)
        else:
            info = self.db.get_this_week_rows(u_id, self.status)
        s_date = None
        for row in info:
            if s_date is None or s_date.date() != row[2].date():
                s_date = row[2]
                arr[s_date] = {}
            if not (row[1] in arr[s_date].keys()): arr[s_date][row[1]] = []
            delta = self.get_difference_betwen(row[2], row[3])
            arr[s_date][row[1]].append(delta)
        
        for key, val in arr.items():
            arr[key] = {k: v for k, v in sorted(val.items(), key=lambda item: item[0])}
        
        alltimesum = datetime.timedelta()
        for key, val in arr.items():
            res += str(key.strftime(self.dateformat)) + "\n" + "-"*10 + "\n"

            timesum = datetime.timedelta()
            tagtimesum = None

            for k, v in val.items():
                if not tagtimesum is None: res += " "*8 + "TAG SUM >> " + str(tagtimesum).split(".")[0] + "\n"
                tagtimesum = datetime.timedelta()
                res += " "*4 + "#" + k + "\n"
                for el in v:

                    tagtimesum += el
                    timesum += el
                    alltimesum += el
            res += " "*8 + "TAG SUM >> " + str(tagtimesum).split(".")[0] + "\n"
            res += " "*4 + "DAY SUM >> " + str(timesum).split(".")[0] + "\n"
            res += "\n"
        res += "WEEK SUM >> " + str(alltimesum).split(".")[0] + "\n"
        return res if res != "" else "None"


# w = Work("csv_data/data.csv")
# print(w.get_finfo_day_intervals(472914986))
# print(w.get_finfo_day_sum(472914986))