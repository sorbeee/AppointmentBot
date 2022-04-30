from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('⁉ Допомога ⁉')
b2 = KeyboardButton('Адміністратор🧑🏼‍💻')
b3 = KeyboardButton('Клієнт🤳🏻')
b5 = KeyboardButton('Працівник👨‍🔧')
b4 = KeyboardButton('Зв\'язатися з розробниками📲')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)

kb_start.add(b1)
kb_start.add(b2).insert(b3).insert(b5)
kb_start.add(b4)
