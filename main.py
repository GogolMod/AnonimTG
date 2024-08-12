import telebot
import sqlite3 as sql

bot = telebot.TeleBot('7081868321:AAEG-R1TCvAJ7Y5YlN64fucKwAvonxbqQmM')

@bot.message_handler(commands=['massage'])
def Massage_start(message):
    global userID_massage
    userID_massage = message.from_user.id
    bot.send_message(message.from_user.id, "Сообщение записывается")
    bot.register_next_step_handler(message, Massage_step1)
def Massage_step1(message):
    text = message.text
    con = sql.connect('save_massage.db')
    with con:
        print("Запись в бд")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `test` (`userID` STRING, `text` STRING)")
        cur.execute(f"INSERT INTO `test` VALUES ('{userID_massage }', '{text}')")
        con.commit()
        cur.close()
    bot.reply_to(message, "Cобщение записанно")
#   bot.register_next_step_handler(message, "")

@bot.message_handler(commands=['Get'])
def get(massage):
    key = '1'
    if key == userID_massage:
        con = sql.connect('record_vidio1.db')
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS `test` (`name` STRING, `surname` STRING, `userID` STRING)")
            cur.execute("SELECT * FROM `test`")
            rows = cur.fetchall()
            row = rows[-1]
            exp = row[1] + " - " + row[0]
            bot.send_message(message.chat.id, exp)
            print(exp)

            print("Последние видио")
            con.commit()
            cur.close()











@bot.message_handler(commands=['save'])
def start_save(message):
    bot.send_message(message.from_user.id, "Отправте видео")
    bot.register_next_step_handler(message, save_vidio)
def save_vidio(message):

    global Vidio
    Vidio = message.text
    if "https://youtu.be/" in Vidio:
        bot.send_message(message.chat.id, 'Отправте его название')
        bot.register_next_step_handler(message, save_name)
    elif "https://youtube.com/shorts/" in Vidio:
        bot.send_message(message.chat.id, 'Шортсы нелзя')
    else:
        bot.send_message(message.chat.id, 'не верная ссылка')
def save_name(message):
    userID = message.from_user.id
    name_vidio = message.text
    con = sql.connect('record_vidio1.db')
    with con:
        print("Запись в бд")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `test` (`vidio` STRING, `name` STRING, `userID` STRING)")
        cur.execute(f"INSERT INTO `test` VALUES ('{Vidio}', '{name_vidio}', '{userID}')")
        con.commit()
        cur.close()
    print("записанно")
    bot.send_message(message.chat.id, "Записанно")

@bot.message_handler(commands=['receive'])
def send_vidio(message):
    userID = message.from_user.id
    con = sql.connect('record_vidio1.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `test` (`name` STRING, `surname` STRING, `userID` STRING)")
        cur.execute("SELECT * FROM `test`")
        rows = cur.fetchall()
        for row in rows:
            if row[2] == userID:
                name = row[1]
                vidio_bd = row[0]
                exp = name + " - " + vidio_bd
                print(exp)
                bot.send_message(message.chat.id, exp)
        print("выдача базы")
        con.commit()
        cur.close()

@bot.message_handler(commands=['newr'])
def send_vidio(message):
    con = sql.connect('record_vidio1.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `test` (`name` STRING, `surname` STRING, `userID` STRING)")
        cur.execute("SELECT * FROM `test`")
        rows = cur.fetchall()
        row = rows[-1]
        exp = row[1] + " - " + row[0]
        bot.send_message(message.chat.id, exp)
        print(exp)

        print("Последние видио")
        con.commit()
        cur.close()

@bot.message_handler(commands=['help','start'])
def send_vidio(message):
    bot.send_message(message.from_user.id, "/save - сохраняет видио \n/receive - выводит сахранные видио\n/newr - выводит последние видио")

bot.infinity_polling()

