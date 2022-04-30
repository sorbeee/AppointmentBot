from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton('⁉ Допомога ⁉')
b3 = KeyboardButton('Показати всі заклади')
b11 = KeyboardButton('Назад↩️')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b3)
kb_client.add(b1).insert(b11)

b5 = KeyboardButton('Зареєструватися', request_contact=True)
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)
kb_reg.add(b5).add(b11)
