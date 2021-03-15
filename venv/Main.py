import sqlite3
import telebot

bot = telebot.TeleBot('1635667052:AAFx7SLtkxJU04GKVFJGSmH3YfOuiexX1ws')

def add_message(message):
    sql_conn = sqlite3.connect("bot_db.sqlite")
    cursor = sql_conn.cursor()
    user_id = message.from_user.id
    query_check = cursor.execute('''SELECT * FROM table1 WHERE user_id = ?''', (user_id,)).fetchone()
    if(query_check is None):
        message_id = message.from_user.id * 10 + 1
        cursor.execute('''INSERT INTO table1 (user_id, message_id) VALUES (?, ?)''', (user_id, message_id))
        sql_conn.commit()
        cursor.execute('''INSERT INTO table2 (message_id, message) VALUES (?, ?)''', (message_id, record))
        sql_conn.commit()
    else:
        quantity = cursor.execute('''SELECT COUNT(user_id) FROM table1 WHERE user_id = ?''', (user_id,)).fetchone()
        message_id = message.from_user.id * 10 + quantity[0] + 1
        cursor.execute('''INSERT INTO table1 (user_id, message_id) VALUES (?, ?)''', (user_id, message_id))
        cursor.execute('''INSERT INTO table2 (message_id, message) VALUES (?, ?)''', (message_id, record))
        sql_conn.commit()

def show_message(message):
    sql_conn = sqlite3.connect("bot_db.sqlite")
    cursor = sql_conn.cursor()
    user_id = message.from_user.id
    message_id = cursor.execute('''SELECT message_id FROM table1 WHERE user_id = ?''', (user_id,)).fetchall()
    result = []
    for i in list(message_id):
        mess = cursor.execute('''SELECT message FROM table2 WHERE message_id = ?''', (i[0],)).fetchone()
        result.append(mess)
    return result

def delete_message(message, id_message):
    sql_conn = sqlite3.connect("bot_db.sqlite")
    cursor = sql_conn.cursor()
    message_id = message.from_user.id * 10 + int(id_message)
    cursor.execute('''DELETE FROM table2 WHERE message_id = ?''', (message_id,))
    cursor.execute('''DELETE FROM table1 WHERE message_id = ?''', (message_id,))
    sql_conn.commit()
    user_id = message.from_user.id
    message_id = cursor.execute('''SELECT message_id FROM table1 WHERE user_id = ?''', (user_id,)).fetchall()
    quantity = cursor.execute('''SELECT COUNT(user_id) FROM table1 WHERE user_id = ?''', (user_id,)).fetchone()
    mess_id = []
    for i in list(message_id):
        mess_id.append(i[0])
    for i in range(0,quantity[0]):
        mess = message.from_user.id * 10 + i + 1
        cursor.execute('''UPDATE table1 SET message_id = ? WHERE message_id = ?''', (mess,mess_id[i])).fetchone()
        cursor.execute('''UPDATE table2 SET message_id = ? WHERE message_id = ?''', (mess, mess_id[i])).fetchone()
        sql_conn.commit()

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if(message.text == "/start"):
        bot.send_message(message.from_user.id,"Привет, " + message.from_user.first_name + ". Я умею запоминать твои сообщения!")
        bot.send_message(message.from_user.id,"Вот мои команды: \n/show - Повторить сообщения, которые я запомнил. \n/add - Добавить предыдущее сообщение в список. \n/delete Номер сообщения - удалить сообщение. \n/help")
    elif (message.text == "/help"):
        bot.send_message(message.from_user.id,"Вот мои команды: \n/show - Повторить сообщения, которые я запомнил. \n/add - Добавить предыдущее сообщение в список. \n/delete Номер сообщения - удалить сообщение.")
    elif(message.text == "/show"):
        result = show_message(message)
        if not result:
            bot.send_message(message.from_user.id, "У тебя нет сохраненных сообщений")
        else:
            count = 1
            for i in list(result):
                mess = "Сообщение " + str(count) + " - " + str(i[0])
                bot.send_message(message.from_user.id,mess)
                count += 1
        print(type(result))
    elif (message.text == "/add"):
        add_message(message)
    else:
        text = message.text.split()
        if(text[0] == "/delete"):
            delete_message(message, text[1])
        else:
            global record
            record = message.text
bot.polling(none_stop=True)