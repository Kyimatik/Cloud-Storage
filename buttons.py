from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove

#Самые главные кнопки.
mainkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить фотку ✅"),
            KeyboardButton(text="Удалить фотку ❌")
        ],
        [
            KeyboardButton(text="Мои фотки 🎞")
        ],
        [
            KeyboardButton(text="Инструкция 📜")
        ]
    ],
    resize_keyboard=True
)


otmena = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена ❌")
        ]
        
    ],
    resize_keyboard=True
)

# Фото да или нет
photoyesorno = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да",callback_data="yesphoto")
        ],
        [
            InlineKeyboardButton(text="Нет",callback_data="nophoto")
                                
        ]
    ],
    resize_keyboard=True
)
# Кнопка Да или нет
buttonyesorno = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да",callback_data="yesbutton")
        ],
        [
            InlineKeyboardButton(text="Нет",callback_data="nobutton")
                                
        ]
    ],
    resize_keyboard=True
)
# Подтверждение
confirmationyesorno = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да",callback_data="yesconfirm")
        ],
        [
            InlineKeyboardButton(text="Нет",callback_data="noconfirm")
                                
        ]
    ],
    resize_keyboard=True
)