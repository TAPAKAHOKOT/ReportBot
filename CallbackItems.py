from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

class CallbackItems:
    def __init__(self):
        self.editing_callback = CallbackData("edit_on", "edit_val", "editing")
        self.get_editing_btns_callback = lambda v: [
            InlineKeyboardButton(
                text=val,
                callback_data=self.editing_callback.new(
                    edit_val=val + "," + v,
                    editing="y"
                )) for val in ["+20 min", "+1 min", "-1 min", "-20 min", "+60 min", "+5 min", "-5 min", "-60 min"]
        ]

        self.edit_work_time_callback = CallbackData("edit_work_time", "id", "editing")
        self.get_edit_work_btn_callback = lambda val: InlineKeyboardButton(
                                                    text=val,
                                                    callback_data=self.edit_work_time_callback.new(
                                                        id=val,
                                                        editing="y"
                                                    ))

        self.settings_callback = CallbackData("settings", "status")
        self.get_settings_utc_btn_callback = lambda s: InlineKeyboardButton(
                                                            text="Set UTC (UTC%s)" % s,
                                                            callback_data=self.settings_callback.new(
                                                                status="utc"
                                                            )
                                                        )
        self.settings_btns_callback = [
            InlineKeyboardButton(
                text="Set UTC",
                callback_data=self.settings_callback.new(
                    status="utc"
                )
            )
        ]

        self.location_callback = CallbackData("location", "status", "UTC")

        self.checkout_nums_callback = CallbackData("checkout", "status", "val", "btns_num")
        self.get_checkout_push_up_btn_callback = lambda v: InlineKeyboardButton(
                                                                text="25",
                                                                callback_data=self.checkout_nums_callback.new(
                                                                    status="reminder_push_up",
                                                                    val=25,
                                                                    btns_num=v
                                                                ))
        self.checkout_callback = CallbackData("checkout", "status", "action")
        self.checkout_btn_callback = {
            "reminder": InlineKeyboardButton(
                text="Done?",
                callback_data=self.checkout_callback.new(
                    status="reminder",
                    action="done"
                ))
        }


        self.add_delete_work_period = CallbackData("add_delete_work_period", "status")
        self.add_delete_period_btn_callback = {
            "Add": InlineKeyboardButton(
                text="Add",
                callback_data=self.add_delete_work_period.new(
                    status="Add"
                )),
            "Delete": InlineKeyboardButton(
                text="Delete",
                callback_data=self.add_delete_work_period.new(
                    status="Delete"
                )),
            "Edit": InlineKeyboardButton(
                text="Edit",
                callback_data=self.add_delete_work_period.new(
                    status="Edit"
                ))
        }

        self.delete_work_time_callback = CallbackData("delete_work_time", "id", "deleting")
        self.get_delete_work_btn_callback = lambda val: InlineKeyboardButton(
                                                    text=val,
                                                    callback_data=self.delete_work_time_callback.new(
                                                        id=val,
                                                        deleting="y"
                                                    ))

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
        self.date_back_callback = InlineKeyboardButton(
                                    text="Back", 
                                    callback_data=self.date_callback.new(
                                        time_unit="Back",
                                        val=-1
                                    ))

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
            
