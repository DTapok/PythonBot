import sqlite3

sqlite_conn = sqlite3.connect("bot_db.sqlite")
querry = '''CREATE TABLE table1 (user_id INTEGER,message_id INTEGER PRIMARY KEY)'''

cursor = sqlite_conn.cursor()
cursor.execute(querry)
sqlite_conn.commit()

querry = '''CREATE TABLE table2 (message_id INTEGER PRIMARY KEY , message TEX)'''
cursor = sqlite_conn.cursor()
cursor.execute(querry)
sqlite_conn.commit()

cursor.close()
sqlite_conn.close()

