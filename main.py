import sqlite3
import telebot
from telebot import types

mybot = telebot.TeleBot('токен скрыт')
conn = sqlite3.connect('events.db', check_same_thread=False)
cursor = conn.cursor()


@mybot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = types.KeyboardButton("Сегодня")
    tomorrow = types.KeyboardButton("Завтра")
    menu.add(today, tomorrow)
    mess = f'Привет \U0001F44B, <b>{message.from_user.first_name}</b> \n\nЯ бот от EventsTime!\nЯ верю в нашу идею того, что события объединяют\U0001F917 \n\nМогу показать тебе интересные и бесплатные события в Санкт-Петербурге\U0001F3D9 \n\nВыбирай когда'
    mybot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=menu)


# noinspection DuplicatedCode
@mybot.message_handler()
def func(message):
    global i
    i = -1
    while True:
        i += 1
        if message.text == "Сегодня":
            cursor.execute("SELECT name,note,link,pic FROM event WHERE datey = date('now')")
            data = cursor.fetchall()
            if len(data) == 0:
                mybot.send_message(message.chat.id, '⚠Технические шоколадки⚠ \n   Мероприятия не добавлены ')
                break
            else:
                try:
                    mybot.send_photo(message.chat.id, f"{data[i][3]}",
                                     f'<b>■ {data[i][0]} ■</b>  \n{data[i][1]} \n\n🔎Ссылка на регистрацию \n{data[i][2]}',
                                     parse_mode='html')
                except:
                    break
        elif message.text == "Завтра":
            cursor.execute("SELECT name,note,link,pic FROM event WHERE datey = date('now','+1 day')")

            data = cursor.fetchall()
            if len(data) == 0:
                mybot.send_message(message.chat.id, '⚠Технические шоколадки⚠ \n   Мероприятия не добавлены ')
                break
            else:
                try:
                    mybot.send_photo(message.chat.id, f"{data[i][3]}",
                                     f'<b>■ {data[i][0]} ■</b>  \n{data[i][1]} \n\n🔎Ссылка на регистрацию \n{data[i][2]}',
                                     parse_mode='html')
                except:
                    break
        else:
            try:
                mybot.send_message(message.chat.id, "я тебя не понимаю \U0001F615 \nпопробуй /start", parse_mode='html')
                break
            except:
                break


mybot.polling(none_stop=True)
