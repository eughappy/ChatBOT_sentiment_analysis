from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

start_buttons = ReplyKeyboardMarkup(keyboard = 
    [[KeyboardButton(text="/help"), KeyboardButton(text="/register")],
    [KeyboardButton(text="/start_analysis"), KeyboardButton(text="/exit") ]],
    resize_keyboard = True)

analysis_button = InlineKeyboardMarkup(inline_keyboard = 
    [[InlineKeyboardButton(text = "Analysis", callback_data="analysis")],
    [InlineKeyboardButton(text = "Exit",callback_data="exit")]],
    )

get_number_button = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text="Let us know ur number.", request_contact = True)]], resize_keyboard = True)