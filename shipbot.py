import config
import telebot
import random

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["shipper"])
def ship(message):
    random.randint(0, 5)
    if message.chat.id == 335524556:
        bot.send_message(message.chat.id, 'это личка?')
    else:
        bot.send_message(message.chat.id, 'ПАПАААА!')
    print(message.chat.id, ": ", message.text, sep='')


if __name__ == '__main__':
    bot.polling(none_stop=True)
