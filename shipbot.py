import config
import telebot
import random
import cd
import time
import colorama
import enum
import sqlite3 as sl
from datetime import datetime
from datetime import timedelta
from colorama import Fore, Back, Style

bot = telebot.TeleBot(config.token)
con = sl.connect(config.db, check_same_thread=False)
cooldown = config.cooldown
colorama.init()
chatIDs = []


def convertTime(x): return time.strftime("%d.%m.%Y %H:%M", time.localtime(x))


def TimestampMillisec64():
    return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())


def out_red(text):
    print(Fore.RED + text)


def out_green(text):
    print(Fore.GREEN + text)


def out_white(text):
    print(Fore.WHITE + text)


def out_yelow(text):
    print(Fore.YELLOW + text)


def get_data():
    data = con.execute("SELECT * FROM USER").fetchall()
    return data


def get_count():
    count = con.execute("SELECT COUNT(*) FROM USER").fetchone()[0]
    return count


def delete_data(username):
    con.execute("DELETE FROM USER WHERE name = ?", (username,))
    con.commit()


def set_data(username):
    data = get_data()
    con.executemany('INSERT INTO USER (id, name) values(?, ?)',
                    [(data[get_count()-1][0]+1, username)])
    con.commit()


def draw_data():
    out_yelow(str(get_data()))


def chkList(id):
    ret = -1
    for chat in range(len(chatIDs)):
        if chatIDs[chat].chatID == id:
            ret = chat
    return ret


@bot.message_handler(commands=["shipper"])
def ship(message):
    num = chkList(message.chat.id)
    now = TimestampMillisec64()
    if num < 0:
        chatIDs.append(cd.cooldownTime(message.chat.id, message.date))
        users = get_data()
        rnd = random.randint(0, get_count()-1)
        left_dog_hand = users[rnd][1]
        rnd = random.randint(0, get_count()-1)
        right_dog_hand = users[rnd][1]
        bot.send_message(message.chat.id, "Море волнуется раз")
        bot.send_message(message.chat.id, "Море волнуется два")
        bot.send_message(message.chat.id, "Море волнуется три")
        bot.send_message(message.chat.id, "И в любовной паре замирают " +
                         left_dog_hand + " + " + right_dog_hand + " = ♥️")
        out_white(convertTime(message.date) + " | " +
                  message.from_user.first_name + " " + message.from_user.last_name +
                  ": " + left_dog_hand + " + " + right_dog_hand + " = <3")
    else:
        if chatIDs[num].lastMessageTime + int(cooldown*60*60) < now:
            chatIDs.pop(num)


@bot.message_handler(commands=["adduser"])
def add(message):
    if message.from_user.id == config.admin_id:
        set_data(message.text.split(' ')[1])
        bot.send_message(
            message.chat.id, "в БД добавлен юзер " + message.text.split(' ')[1])
        out_green(convertTime(message.date) + " | " + message.from_user.first_name +
                  " " + message.from_user.last_name + " add user " + message.text.split(' ')[1])


@bot.message_handler(commands=["draw"])
def draw(message):
    bot.send_message(message.chat.id, str(get_data()))
    draw_data()


@bot.message_handler(commands=["cd"])
def coold(message):
    if message.from_user.id == config.admin_id:
        cooldown = float(message.text.split(' ')[1])
        out_yelow("cooldown changed to " + str(cooldown) + " h")
        bot.send_message(message.chat.id, "кулдаун изменен")


@bot.message_handler(commands=["rmuser"])
def rm(message):
    if message.from_user.id == config.admin_id:
        delete_data(message.text.split(' ')[1])
        bot.send_message(
            message.chat.id, "из БД удален юзер " + message.text.split(' ')[1])
        out_red(convertTime(message.date) + " | " + message.from_user.first_name +
                " " + message.from_user.last_name + " remove user " + message.text.split(' ')[1])


if __name__ == '__main__':
    out_yelow("ShipperChan online")
    bot.polling(none_stop=True)
