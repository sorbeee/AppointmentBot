from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('⁉ Допомога ⁉')
b2 = KeyboardButton('Завантажити заклад')
b3 = KeyboardButton('Показати заклади')
b4 = KeyboardButton('Відмінити')
b5 = KeyboardButton('Назад ↩')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b1)
kb_admin.add(b2).insert(b3)
kb_admin.add(b5)
kb_admin_downloading = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_downloading.add(b4)

kb_admin_time = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('30 хвилин')).insert(KeyboardButton('45 хвилин')).insert(KeyboardButton('60 хвилин'))
kb_admin_time.add(b4)
