import config
import text
import cd
import db

import time
import random
import telebot
from datetime import datetime

bot = telebot.TeleBot(config.token)
cooldown = config.cooldown
chatIDs = []


def convertTime(x): return time.strftime("%d.%m.%Y %H:%M", time.localtime(x))


def chkList(id):
    ret = -1
    for chat in range(len(chatIDs)):
        if chatIDs[chat].chatID == id:
            ret = chat
    return ret


def shipping(message):
    chatIDs.append(cd.cooldownTime(message.chat.id, message.date))
    users = db.get_data()
    rnd = random.randint(0, db.get_count()-1)
    left_dog_hand = users[rnd][1]
    rnd = random.randint(0, db.get_count()-1)
    right_dog_hand = users[rnd][1]
    bot.send_message(message.chat.id, "Море волнуется раз")
    bot.send_message(message.chat.id, "Море волнуется два")
    bot.send_message(message.chat.id, "Море волнуется три")
    bot.send_message(message.chat.id, "И в любовной паре замирают " +
                     left_dog_hand + " + " + right_dog_hand + " = ♥️")
    text.out_white(convertTime(message.date) + " | " +
                   message.from_user.first_name + " " + message.from_user.last_name +
                   ": " + left_dog_hand + " + " + right_dog_hand + " = <3")


@bot.message_handler(commands=["shipper"])
def ship(message):
    num = chkList(message.chat.id)
    now = message.date
    if num < 0:
        shipping(message)
    else:
        if chatIDs[num].lastMessageTime + int(cooldown*60*60) < now:
            chatIDs.pop(num)
            shipping(message)


@bot.message_handler(commands=["adduser"])
def add(message):
    if message.from_user.id == config.admin_id:
        db.set_data(message.text.split(' ')[1])
        bot.send_message(
            message.chat.id, "в БД добавлен юзер " + message.text.split(' ')[1])
        text.out_green(convertTime(message.date) + " | " + message.from_user.first_name +
                       " " + message.from_user.last_name + " add user " + message.text.split(' ')[1])


@bot.message_handler(commands=["draw"])
def draw(message):
    if message.from_user.id == config.admin_id:
        bot.send_message(message.chat.id, str(db.get_data()))
        text.draw_data()


@bot.message_handler(commands=["cd"])
def coold(message):
    if message.from_user.id == config.admin_id:
        global cooldown
        cooldown = float(message.text.split(' ')[1])
        text.out_yelow("cooldown changed to " + str(cooldown) + " h")
        bot.send_message(message.chat.id, "кулдаун изменен")


@bot.message_handler(commands=["rmuser"])
def rm(message):
    if message.from_user.id == config.admin_id:
        db.delete_data(message.text.split(' ')[1])
        bot.send_message(
            message.chat.id, "из БД удален юзер " + message.text.split(' ')[1])
        text.out_red(convertTime(message.date) + " | " + message.from_user.first_name +
                     " " + message.from_user.last_name + " remove user " + message.text.split(' ')[1])


if __name__ == '__main__':
    text.out_yelow("ShipperChan online")
    while True:
        try:
            bot.infinity_polling(True)
        except Exception as e:
            text.out_red(e)
            time.sleep(15)
