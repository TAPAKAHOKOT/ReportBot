import datetime
import logging
from Settings import Settings

from DataBaseConnectors.BackupDBC import BackupDBC
from DataBaseConnectors.CustomerDBC import CustomerDBC
from DataBaseConnectors.StateStorageDBC import StateStorageDBC
from DataBaseConnectors.TagDBC import TagDBC
from DataBaseConnectors.TermDBC import TermDBC

class Work:
    def __init__(self, settings:Settings, u_id: int) -> None:
        logging.info("Start initing Work for %s" % u_id)

        self.setttings = settings
        self.user_id = u_id

        self.last_online_time = datetime.datetime.now()

        self.timeformat = "%H.%M.%S"
        self.dateformat = "%d.%m.%Y"
        
        self.is_working = False

        self.start_date_working = None
        self.end_date_working = None
        self.start_time_working = None

        self.tag = "testing"
        self.status = "studying"

        self.backup_db = BackupDBC(self.setttings.db_data)
        self.customer_db = CustomerDBC(self.setttings.db_data)
        self.statestorage_db = StateStorageDBC(self.setttings.db_data)
        self.tag_db = TagDBC(self.setttings.db_data)
        self.term_db = TermDBC(self.setttings.db_data)

        self.start_constructor_done = False
        self.date_callback_constructor = ""
        self.time_callback_constructor = ""

        self.callback_start_date_working: datetime.datetime = None
        self.callback_start_time_working: datetime.datetime = None
        self.callback_end_time_working: datetime.datetime = None

        u_data = self.statestorage_db.get_user_state(self.user_id)
        if u_data:
            self.tag = u_data[0][0]
            self.status = u_data[0][1]
        else:
            self.statestorage_db.add_row(self.user_id, self.tag, self.status)

        logging.info("End initing Work")


    def get_is_working(self) -> bool:
        return self.is_working
    

    def get_status(self) -> str:
        return self.status.title()
    

    def get_tag(self) -> str:
        return self.tag


    def set_tag(self, tag: str) -> None:
        tag_lim = 9
        all_tags = self.tag_db.get_tags(self.user_id)
        self.tag = tag
        self.statestorage_db.set_tag(self.user_id, tag)

        if tag not in all_tags:
            tags_num = self.tag_db.get_count(self.user_id)
            while tags_num >= tag_lim:
                self.tag_db.delete_last_tag(self.user_id)
                tags_num = self.tag_db.get_count(self.user_id)

            self.tag_db.add_row(self.user_id, tag)
    

    def set_status(self, status: str) -> None:
        self.status = status
        self.statestorage_db.set_status(self.user_id, status)


    def saving_data(self, u_id: int) -> None:
        logging.info("Start saving_data(...)")
        self.term_db.add_row(u_id, self.tag, self.status, self.start_time_working, self.end_time_working)
        logging.info("End saving_data(...)")
    

    def save_spec_data(self, u_id: int, s: datetime.datetime, e: datetime.datetime) -> None:
        logging.info("save_spec_data saving_data(...)")
        logging.info("start time : {}\nend time: {}".format(s, e))
        self.term_db.add_row(u_id, self.tag, self.status, s, e)
        logging.info("End save_spec_data(...)")


    def start_working(self) -> str:
        logging.info("Start start_working(...)")
        self.last_online_time = datetime.datetime.now()
        if self.is_working:
            logging.info("End start_working(...)")
            return "You are already working from {} {}".format(self.start_date_working, self.start_time_working)
        self.is_working = True 
        self.start_time_working = self.get_current_time()
        self.start_date_working = self.get_current_day()

        self.backup_db.add_row(self.user_id, self.start_time_working)

        logging.info("End start_working(...)")
        return "Start working time: " + self.start_time_working.strftime(self.timeformat).replace(".", ":") + " " + self.tag
        
    
    def end_working(self, u_id: int) -> str:
        logging.info("Start end_working(...)")
        self.last_online_time = datetime.datetime.now()
        if not self.is_working:
            logging.info("End end_working(...)")
            return "You aren't working now"
        self.is_working = False
        self.end_time_working = self.get_current_time()
        self.end_date_working = self.get_current_day()

        self.backup_db.delete_last(self.user_id)

        self.saving_data(u_id)
        logging.info("End end_working(...)")
        return "End working time: {}\nWorking time: {}".format(self.end_time_working.strftime(self.timeformat).replace(".", ":"), str(self.get_difference()).split(".")[0])


    def set_start_working_time(self, t: datetime.datetime):
        logging.info("Start set_start_working_time(...)")
        self.last_online_time = datetime.datetime.now()
        self.is_working = True 
        self.start_time_working = t
        self.start_date_working = t
        logging.info("End set_start_working_time(...)")


    def get_current_day(self) -> datetime.datetime:
        return datetime.datetime.today()


    def get_current_time(self) -> datetime.datetime:
        return datetime.datetime.now()


    def get_time_from(self, line: str) -> datetime.datetime:
        start, end = line.split("-")

        start = datetime.datetime.strptime(start, self.timeformat)
        end = datetime.datetime.strptime(end, self.timeformat)

        return [start, end]
    

    def get_one_time_from(self, line: str) -> datetime.datetime:
        return datetime.datetime.strptime(line, self.timeformat)
    

    def get_day_from(self, line: str) -> datetime.datetime:
        return datetime.datetime.strptime(line, self.dateformat)
    

    def get_difference_betwen(self, s_time, e_time) -> datetime.timedelta:
        return e_time - s_time if e_time > s_time \
            else e_time - s_time + datetime.timedelta(1)


    def get_difference(self) -> datetime.timedelta:
        return self.end_time_working - self.start_time_working
    

    def get_day_time_formated(self, s_time: datetime.datetime = None, e_time: datetime.datetime = None) -> str:
        self.last_online_time = datetime.datetime.now()
        if not s_time: s_time = self.start_time_working
        if not e_time: e_time = self.end_time_working
        return s_time.strftime(self.timeformat) + " - " + e_time.strftime(self.timeformat)
    

    def get_current_working_info(self) -> str:
        self.last_online_time = datetime.datetime.now()
        if not self.is_working:
            return "You aren't working now"
        delta = str(self.get_difference_betwen(self.start_time_working, self.get_current_time())).split(".")[0]
        return "Start working time: {}\nTime delta: {}".format(self.start_time_working.strftime(self.timeformat), delta)
    

    def delete_interval(self, u_id: int, n: int) -> str:
        self.last_online_time = datetime.datetime.now()
        rows = self.term_db.get_all_periods_rows(u_id, "this_week", self.status)
        
        self.term_db.delete_row_by_id(rows[n - 1][-1])

        delta = str(self.get_difference_betwen(rows[n - 1][1], rows[n - 1][2])).split(".")[0]
        line = self.get_day_time_formated(rows[n - 1][1], rows[n - 1][2]) + " => " + delta

        return line


    def get_finfo_day_intervals(self, u_id: int, last_week: bool = False, for_del: bool = False) -> list:
        logging.info("Start get_finfo_day_intervals(...)")
        self.last_online_time = datetime.datetime.now()

        title = ""
        if for_del:
            s = len("Status: " + self.status.title()) - 8
            title += "<<< {}DELETING{} >>>".format(" " * (s//2), " " * (s - s//2))
        title += "\n<<< Status: " + self.status.title() + " >>>\n"

        size, res = 0, ""
        s_date, s_tag = None, None

        rows = self.term_db.get_all_periods_rows(u_id, "last_week", self.status) if last_week\
            else self.term_db.get_all_periods_rows(u_id, "this_week", self.status)
        
        for row in rows:
            if s_date is None or s_date.date() != row[1].date():
                if s_date is not None: res += "\n"
                s_date = row[1]
                s_tag = None
                res += str(s_date.strftime(self.dateformat)) + "\n" + "-"*18 + "\n"

            if s_tag is None or s_tag != row[0]: 
                s_tag = row[0]
                res += " "*4 + s_tag + "\n"

            size += 1
            del_part = " "*6 + "(" + str(size) + ")"
            delta = str(self.get_difference_betwen(row[1], row[2])).split(".")[0]
            line = self.get_day_time_formated(row[1], row[2]) + " => " + delta
            res += " "*6 + line + (del_part if for_del else "") + "\n"

        return [title + res if res != "" else "No records", size]
    
    def get_finfo_day_sum(self, u_id: int, last_week: bool = False, month: bool = False) -> str:
        logging.info("Start get_finfo_day_sum(...)")
        self.last_online_time = datetime.datetime.now()

        title = "\n<<< Status: " + self.status.title() + " >>>\n"
        res = ""

        rows = self.term_db.get_period_rows(u_id, "last_week", self.status) if last_week\
            else self.term_db.get_period_rows(u_id, "this_week", self.status)
        if month: rows = self.term_db.get_period_rows(u_id, "this_month", self.status)

        c_date = None
        daytimesum = datetime.timedelta()
        alltimesum = datetime.timedelta()
        for row in rows:
            date, tag, time_sum = row
            if c_date is None or c_date != date:
                if c_date is not None:
                    res += " "*4 + "DAY SUM >> " + str(daytimesum).split(".")[0] + "\n\n"
                    daytimesum = datetime.timedelta()
                c_date = date
                res += str(c_date.strftime(self.dateformat)) + "\n" + "-"*18 + "\n"
            
            res += " "*4 + tag + "\n"
            res += " "*8 + "TAG SUM >> " + str(time_sum).split(".")[0] + "\n"
            
            daytimesum += time_sum
            alltimesum += time_sum

        if rows:
            res += " "*4 + "DAY SUM >> " + str(daytimesum).split(".")[0] + "\n"
            res += "\n"
            res += "WEEK SUM >> " + str(alltimesum).split(".")[0] + "\n"

        return title + res if res != "" else "No records"