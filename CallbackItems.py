from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
class CallbackItems:
    def __init__(self):
        self.work_settings_callback = CallbackData("work_settings", "parameter", "value")
        self.statuses_btn_callback = {
            "Studying": InlineKeyboardButton(
                text="Status: Studying",
                callback_data=self.work_settings_callback.new(
                    parameter="status",
                    value="studying"
                )),
            "Working": InlineKeyboardButton(
                text="Status: Working",
                callback_data=self.work_settings_callback.new(
                    parameter="status",
                    value="working"
                ))
        }

        self.get_tag_btn_callback = lambda name: InlineKeyboardButton(
                                                    text=name,
                                                    callback_data=self.work_settings_callback.new(
                                                        parameter="tag",
                                                        value=name
                                                    ))

        self.work_reports_callback = CallbackData("report", "period", "status")
        self.reports_btn_callback = {
            "last_week": InlineKeyboardButton(
                text="Last week", 
                callback_data=self.work_reports_callback.new(
                    period="last_week",
                    status="period_report"
                )),
            "last_week_d": InlineKeyboardButton(
                text="Last week (details)", 
                callback_data=self.work_reports_callback.new(
                    period="last_week_d",
                    status="period_report"
                )),
            "this_week": InlineKeyboardButton(
                text="This week", 
                callback_data=self.work_reports_callback.new(
                    period="this_week",
                    status="period_report"
                )),
            "this_week_d": InlineKeyboardButton(
                text="This week (details)", 
                callback_data=self.work_reports_callback.new(
                    period="this_week_d",
                    status="period_report"
                ))
        }

        self.date_callback = CallbackData("date", "time_unit", "val")

        self.days_btn_callback = {
            k: InlineKeyboardButton(
                text=str(k), 
                callback_data=self.date_callback.new(
                    time_unit="day",
                    val=k
                )
            ) for k in range(1, 32)
        }

        self.hours_btn_callback = {
            k: InlineKeyboardButton(
                text=str(k), 
                callback_data=self.date_callback.new(
                    time_unit="hour",
                    val=k
                )
            ) for k in range(24)
        }

        self.mins_btn_callback = {
            k: InlineKeyboardButton(
                text=str(k), 
                callback_data=self.date_callback.new(
                    time_unit="min",
                    val=k
                )
            ) for k in range(60)
        }
            
