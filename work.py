import csv
import datetime

from time import sleep
from typing import Sequence

class Work:
    def __init__(self, filename: str):
        self.filename = filename

        self.timeformat = "%H.%M.%S"
        self.dateformat = "%d.%m.%Y"
        
        self.is_working = False

        self.start_date_working = None
        self.end_date_working = None
        self.start_time_working = None
        
        self.csv_data = self.read_csv()

    def test_write_csv(self):
        with open(self.filename, "w") as file:
            writer = csv.DictWriter(file, ["Day", "WorkIntervals"])

            writer.writeheader()
            writer.writerows([{"Day": "12.05.2021", "WorkIntervals": ["14.00.10-15.00.25", "15.10.45-16.14.57"]},
                            {"Day": "13.05.2021", "WorkIntervals": ["14.00.30-15.00.13", "15.10.00-16.14.03"]}])
    
    def write_csv(self, new_data):
        with open(self.filename, "w") as file:
            writer = csv.DictWriter(file, ["Day", "WorkIntervals"])

            writer.writeheader()
            writer.writerows(new_data)

    def read_csv(self) -> list:
        res = []
        with open(self.filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Day"] = self.get_day_from(row["Day"])
                row["WorkIntervals"] = [
                    self.get_time_from(t) for t in row["WorkIntervals"].replace("'", "").strip('][').split(', ')
                ]

                res.append(row)
        return res

    def saving_data(self):
        date_founded = False
        self.csv_data = self.read_csv()
        new_data = []
        for row in self.csv_data:
            if row["Day"].date() == self.start_date_working.date():
                date_founded = True
                row["WorkIntervals"].append([self.start_date_working, self.end_date_working])

            row["Day"] = row["Day"].strftime(self.dateformat)
            for k, el in enumerate(row["WorkIntervals"]):
                row["WorkIntervals"][k] = self.get_day_time_formated(el[0], el[1])
            new_data.append(row)

        if not date_founded:
            new_data.append({"Day": self.start_date_working.strftime(self.dateformat),
                            "WorkIntervals": [self.get_day_time_formated(self.start_time_working, self.end_time_working)]})

        self.write_csv(new_data)
        self.csv_data = self.read_csv()

    def start_working(self) -> str:
        if self.is_working:
            return "You are already working from {} {}".format(self.start_date_working, self.start_time_working)
        self.is_working = True 
        self.start_time_working = self.get_current_time()
        self.start_date_working = self.get_current_day()

        return "Start working time: " + self.start_time_working.strftime(self.timeformat)
    
    def end_working(self) -> str:
        if not self.is_working:
            return "You aren't working now"
        self.is_working = False
        self.end_time_working = self.get_current_time()
        self.end_date_working = self.get_current_day()

        self.saving_data()

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
    
    def get_day_working_time_sum(self, working_time) -> datetime.timedelta:
        timesum = datetime.timedelta()
        for t in working_time:
            timesum += self.get_difference_betwen(*t)
        return timesum
    
    def get_finfo_day_sum(self) -> str:
        res = ""
        for row in self.csv_data:
            res += "-" * 10 + "\n"
            res += row["Day"].strftime(self.dateformat) + ":\n"
            res += " "*4 + str(self.get_day_working_time_sum(row["WorkIntervals"])) + "\n\n"
        return res if res else "None"

    def get_finfo_day_intervals(self) ->str:
        res = ""
        for row in self.csv_data:
            res += "\n" + "-" * 10 + "\n"
            res += row["Day"].strftime(self.dateformat) + ":\n"
            for k, el in enumerate(row["WorkIntervals"]):
                res += " "*4 + str(self.get_day_time_formated(*el)) + " => " + str(self.get_difference_betwen(*el)).split(".")[0] + "\n"
            res += " "*4 + "Time sum: " + str(self.get_day_working_time_sum(row["WorkIntervals"])) + "\n"
        return res if res else "None"
    
    def get_day_time_formated(self, s_time=None, e_time=None) -> str:
        if not s_time: s_time = self.start_time_working
        if not e_time: e_time = self.end_time_working
        return s_time.strftime(self.timeformat) + "-" + e_time.strftime(self.timeformat)
    
    def get_current_working_info(self):
        if not self.is_working:
            return "You aren't working now"
        delta = str(self.get_difference_betwen(self.start_time_working, self.get_current_time())).split(".")[0]
        return "Start working time: {}\nTime delta: {}".format(self.start_time_working.strftime(self.timeformat), delta)