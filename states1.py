from aiogram.fsm.state import StatesGroup , State

class photostate(StatesGroup):
    wait = State()

class deletephoto(StatesGroup):
    delphoto = State()


#Отправка рассылки всем пользователям которые есть в базе данных.
class sendall(StatesGroup):
    getphoto = State()
    gettext = State()
    getbutton = State() #
    getlink = State() #


class getfeedback(StatesGroup):
    fb = State()