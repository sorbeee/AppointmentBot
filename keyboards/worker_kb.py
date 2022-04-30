from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Розклад на сьогодні')
b2 = KeyboardButton('Розклад на завтра')
b3 = KeyboardButton('Розклад на конкретну дату')
b11 = KeyboardButton('Назад↩️')
kb_worker = ReplyKeyboardMarkup(resize_keyboard=True).insert(b1).insert(b2).insert(b3).add(b11)