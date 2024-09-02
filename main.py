
TOKEN = "?"
import json
import asyncio
import logging
import sys
import time

from aiogram import Bot, Dispatcher, Router, types , F 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart , Command
from aiogram.types import Message , CallbackQuery ,FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMediaGroup
from aiogram.types import InputMediaPhoto
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove

from states1 import sendall
from states1 import photostate # ожидание фотографии чтобы добавить.
from states1 import deletephoto
from states1 import getfeedback
import buttons





admin_id = "6355200375"
group_id = -1001954008760

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()



#photo_filetyan = "AgACAgIAAxkBAAIG6WZ5f9ULu2w_VE7RKmojAzlQ49muAAJe2jEb91zJS65rcv4gK-2kAQADAgADeAADNQQ"
#photo_filecar ="AgACAgIAAxkBAAIG6mZ5gAlOqGiXDTgJ1SSbn-WTrXpvAAJj2jEb91zJS6oFaCGcX4mpAQADAgADeQADNQQ"
# Функция для загрузки данных из JSON файла [users.json]
def load_users():
    try:
        with open('users.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    return data

def save_users(data):
    with open('users.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


photo_path = r"C:\Users\user\Desktop\Tasks Codeforces\tyanka.jpg"
photo = FSInputFile(photo_path)
 #Команда старта , начинается вся работа
@dp.message(Command('start'))
async def getstarted(message: Message):
    user_id = str(message.from_user.id)
    users = load_users()

    # Добавляем пользователя в базу данных, если его там еще нет
    if user_id not in users['users']:
        users['users'][user_id] = {"photos": []}
        save_users(users)
        #json_string = json.dumps(users, ensure_ascii=False, indent=4)
    ##
     #   #await bot.send_message(
        ##            chat_id=group_id,
        ##            text=json_string
         #       )
    await message.answer_photo(photo,"""Привет, <b>{message.from_user.first_name}</b>! 👋

Меня зовут <i>Oblako_29</i>. Я бот, который поможет тебе сохранить важные фотографии.

Этот проект создан для тех, кто хочет легко и удобно хранить свои фотографии в одном месте. Он подойдет каждому, кто ценит свои моменты и хочет иметь возможность быстро к ним возвращаться.

Ты можешь отправлять до 50 фотографий, и я их все сохраню. У тебя также будет возможность редактировать свои фотографии.
""",parse_mode="HTML",reply_markup=buttons.mainkb)
    


#добавление фотографии
def add_photo(user_id, photo_url):
    users = load_users()
    if user_id not in users['users']:
        users['users'][user_id] = {"photos": []}
    
    photo_list = users['users'][user_id]['photos']
    
    # Проверка количества фотографий
    if len(photo_list) < 50:
        photo_id = len(photo_list) + 1
        photo_list.append({"id": photo_id, "url": photo_url})
        save_users(users)
        return f"Фотография добавлена. У вас теперь {len(photo_list)} фотографий."
        
    
    else:
        return "У вас уже 50 фотографий. Невозможно добавить больше."
#удаление фотографии
def delete_photo(user_id, photo_id):
    users = load_users()
    if user_id in users['users']:
        photo_list = users['users'][user_id]['photos']
        photo_list = [photo for photo in photo_list if photo['id'] != photo_id]
        for idx, photo in enumerate(photo_list):
            photo['id'] = idx + 1
        users['users'][user_id]['photos'] = photo_list
        save_users(users)

# Команда добавить фото
@dp.message(F.text.contains("Добавить фотку ✅"))
async def add_photo_command(message: Message , state: FSMContext):
    await message.reply("Пожалуйста, отправьте фотографию.",reply_markup=buttons.otmena)
    await state.set_state(photostate.wait)
# Получение самой фотографии 
@dp.message(photostate.wait, F.photo)
async def photo_received(message: types.Message, state: FSMContext):
    users = load_users()
    user_id = str(message.from_user.id)
    photo_url = message.photo[-1].file_id
    result_message = add_photo(user_id, photo_url)
    await message.answer(result_message,reply_markup=buttons.mainkb)
    json_string = json.dumps(users, ensure_ascii=False, indent=4)
    
    #await bot.send_message(
    #            chat_id=group_id,
    #            text=json_string
    #        )
    await state.clear()
# Узнать номер последней фотографии чтобы понять max id 
def get_last_photo_id(user_id):
    users = load_users()
    photos = users["users"].get(user_id, {}).get("photos", [])
    if photos:
        return photos[-1]["id"]
    else:
        return None






# Удаление фотки 
@dp.message(F.text.contains("Удалить фотку ❌"))
async def handle_delete_photo(message: Message, state: FSMContext):
    await message.answer("Пожалуйста укажите номер фотографии которую хотите удалить.", reply_markup=buttons.otmena)
    await state.set_state(deletephoto.delphoto)

@dp.message(deletephoto.delphoto)
async def processofdeleting(message: Message, state: FSMContext):
    users = load_users()
    if message.text == "Отмена ❌":
        await message.answer("Вы отменили действие.", reply_markup=buttons.mainkb)
        await state.clear()
        return
    
    user_id = str(message.from_user.id)
    
    try:
        photo_id = int(message.text)  # инпут самого пользователя какой номер фотографии он хочет удалить.
        last_photo_id = get_last_photo_id(user_id) # последнее существующее id в "photos"
        
        if last_photo_id is None: # Если нету вообще фоток то он пишет вот так.
            await message.answer("У вас нет сохраненных фотографий.", reply_markup=buttons.mainkb)
            await state.clear()
        elif photo_id < 1 or photo_id > last_photo_id:
            await message.answer("Пожалуйста, укажите корректный номер фотографии для удаления.", reply_markup=buttons.mainkb)
        else:
            delete_photo(user_id, photo_id)
            await message.reply(f"Фотография с номером {photo_id} удалена.", reply_markup=buttons.mainkb)
            await state.clear()
            json_string = json.dumps(users, ensure_ascii=False, indent=4)
    
            #await bot.send_message(
            #            chat_id=group_id,
            #            text=json_string
            #        )
    
    except ValueError:
        await message.reply("Пожалуйста, укажите корректный номер фотографии для удаления.", reply_markup=buttons.mainkb)
        await state.clear()
    except Exception as e:
        await message.reply(f"Произошла ошибка при удалении фотографии: {e}", reply_markup=buttons.mainkb)
        await state.clear()

@dp.message(F.text.contains("Отмена ❌"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Вы отменили действие.", reply_markup=buttons.mainkb)
    await state.clear()



# Показ всех твоих фоток:
@dp.message(F.text.contains("Мои фотки 🎞"))
async def handle_my_photos(message: Message):
    user_id = str(message.from_user.id)
    users = load_users()
    
    if user_id in users['users'] and users['users'][user_id]['photos']:
        photos = users['users'][user_id]['photos'][:50]  # Ограничиваем до 50 фотографий
        message_text = "Ваши фотографии:\n"
        
        if len(photos) <= 10:
            # Отправляем фотографии группой
            media_group = [InputMediaPhoto(media=photo['url'], caption=f"Объект {photo['id']}") for photo in photos]
            message_text += "\n".join([f"Фотка {photo['id']}" for photo in photos])
            
            await message.reply(message_text)
            await bot.send_media_group(chat_id=message.chat.id, media=media_group)
        else:
            # Отправляем фотографии по одной
            await message.reply(message_text)
            for photo in photos:
                await bot.send_photo(chat_id=message.chat.id, photo=photo['url'], caption=f"Фотка {photo['id']}")
    else:
        await message.reply("У вас нет сохраненных фотографий.")

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@dp.message(Command("sendall"))
async def sendmessagestoall(message: Message,state: FSMContext):
    if str(message.from_user.id) == admin_id:
        await message.answer(f'Здравсвтуйте <b>{message.from_user.first_name}</b> . Хотите ли вы разослать сообщение с фоткой?',parse_mode="HTML",reply_markup=buttons.photoyesorno)
    else:
        await message.answer("Error!")

@dp.callback_query(lambda c: c.data in ["yesphoto", "nophoto"])
async def process_photo_choice(callback: CallbackQuery, state: FSMContext):
    if callback.data ==   "yesphoto":
        await callback.message.answer("Отправьте фотку")
        await state.set_state(sendall.getphoto)
    else:
        await callback.message.answer("Теперь отправьте основной текст!")
        await state.set_state(sendall.gettext)

@dp.message(sendall.getphoto , F.photo)
async def get_photo2(message: Message, state : FSMContext):
    await state.update_data(getphoto=message.photo[-1].file_id)
    await message.answer("Теперь отправьте основной текст!")
    await state.set_state(sendall.gettext)

@dp.message(sendall.gettext)
async def gettext123(message: Message, state: FSMContext):
    await state.update_data(gettext=message.text)
    await message.answer("Продолжить с кнопкой или нет ? ",reply_markup=buttons.buttonyesorno)

# Обработка выбора с кнопкой или без
@dp.callback_query(lambda c: c.data in ["yesbutton", "nobutton"])
async def process_button_choice(callback: CallbackQuery, state: FSMContext):
    if callback.data == "yesbutton":
        await callback.message.answer("Отправьте текст кнопки!")
        await state.set_state(sendall.getbutton)
    else:
        await send_preview(callback.message, state)

# Предпросмотр сообщения
async def send_preview(message, state):
    data = await state.get_data()
    if 'getphoto' in data and data['getphoto']:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=data['getphoto'],
            caption=data['gettext'],
            reply_markup=create_keyboard(data)
        )
    else:
        await message.answer(
            text=data['gettext'],
            reply_markup=create_keyboard(data)
        )
    await message.answer("Начинаем отправлять?", reply_markup=buttons.confirmationyesorno)

@dp.message(sendall.getbutton)
async def getbutton123(message: Message, state: FSMContext):
    await state.update_data(getbutton=message.text)
    await message.answer("Теперь отправьте ссылку, которую кнопка будет содержать:")
    await state.set_state(sendall.getlink)

@dp.message(sendall.getlink)
async def getlink342(message: Message, state: FSMContext):
    await state.update_data(getlink=message.text)
    await send_preview(message, state)





# Создание клавиатуры
def create_keyboard(data):
    if 'getbutton' in data and data['getbutton'] and 'getlink' in data and data['getlink']:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=data['getbutton'], url=data['getlink'])]
            ],
            resize_keyboard=True
        )
    return None


# Подтверждение рассылки
@dp.callback_query(lambda c: c.data == "yesconfirm")
async def confirm_send(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    added_keyboards = create_keyboard(data)

    data1 = load_users()

    if 'users' not in data1:
        await callback.message.answer("Ошибка: данные не содержат информации о пользователях.")
        await state.clear()
        return
    
    user_ids = list(data1['users'].keys())
    j = 0

    for i in user_ids:
        try:
            if 'getphoto' in data and data['getphoto']:
                await bot.send_photo(
                    chat_id=i,
                    photo=data['getphoto'],
                    caption=data['gettext'],
                    reply_markup=added_keyboards
                )
            else:
                await bot.send_message(
                    chat_id=i,
                    text=data['gettext'],
                    reply_markup=added_keyboards
                )
            j += 1
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {i}: {e}")
        await asyncio.sleep(0.33)  # Используйте asyncio.sleep вместо time.sleep для асинхронного кода

    await callback.message.answer(f"Количество отправленных рассылок: {j}")
    await state.clear()

@dp.message(F.text.contains("Инструкция 📜"))
async def deliverintruction(message: Message):
    await message.answer_photo("carlol.jpg" ,f"""Привет <b>{message.from_user.first_name}</b>!
У тебя есть три кнопки:
<b>Добавить фотку ✅</b> - просто нажми на кнопку, и бот запросит у тебя фотографию. После этого она будет сохранена.
                               
<b>Удалить фотку ❌</b> - чтобы удалить определенную фотографию, сначала посмотри, под каким номером она идет, а затем отправь этот номер (от 1 до n-фотографий).
                               
<b>Мои фотки 🎞</b> - показывает все твои сохраненные фотографии.

Если у тебя есть какие-то пожелания, используй команду <b>/feedback</b>, и твои пожелания дойдут до основателей.

Приятного использования, дорогой пользователь ❤️.
""",parse_mode="HTML")
   



@dp.message(F.photo)
async def getphotoandid(message: Message):
    ph = message.photo[-1].file_id
    print(ph)

@dp.message(F.text.lower() == "э")
async def getinfoaboutusers(message: Message):
    if str(message.from_user.id) != admin_id:
        await message.answer("Error.")
    else:
        users = load_users()
        user_ids = list(users['users'].keys())
        user_len = len(user_ids)
        await bot.send_message(message.chat.id, f"{user_ids} - <b>Айдишки юзеров</b>\n{user_len} - <b>Кол-во пользователей</b>",parse_mode='HTML')
  

@dp.message(Command("feedback"))
async def getfeedbackfromuser(message: Message, state: FSMContext):
    await message.answer("Отправьте пожелания ниже!")
    await state.set_state(getfeedback.fb)

@dp.message(getfeedback.fb)
async def startdelivering(message: Message , state: FSMContext):
    msg = message.text
    await bot.send_message(group_id,f"Пользователь - @{message.from_user.username}\nОтправил пожелание: \n<b>{msg}</b>",parse_mode="HTML")
    await state.clear()



async def main() -> None:
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())