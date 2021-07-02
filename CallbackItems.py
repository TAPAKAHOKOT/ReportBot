from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
class CallbackItems:
    def __init__(self):
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
            
