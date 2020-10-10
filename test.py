from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
import pymysql
from pymysql.cursors import DictCursor

HOST = 'sql7.freesqldatabase.com'
USER = 'sql7369890'
PASSWORD = 'bjJP6JdVrq'
DB = 'sql7369890'
CHARSET = 'utf8mb4'

def sched(update, context):
	class_name = context.args[0]
	week_day = context.args[1]
	context.bot.send_message(chat_id=update.effective_chat.id, text="Math\nLiterature")
	user_id = update.message.from_user.id
	context.bot.send_message(chat_id=update.effective_chat.id, text=user_id)

def set_group(update, context):
	group_name = context.args[0]
	connection = pymysql.connect(
		host=HOST,
		user=USER,
		password=PASSWORD,
		db=DB,
		charset=CHARSET,
		cursorclass=DictCursor
	)

	context.bot.send_message(chat_id=update.effective_chat.id, text="getting your id")
	user_id = update.message.from_user.id

	with connection.cursor() as cursor:
		query = f"insert into `users` (id, class) values ({user_id}, '{group_name}')"
		print("executing query")
		cursor.execute(query)
		connection.commit()

	connection.close()
	context.bot.send_message(chat_id=update.effective_chat.id, text="inserted")


if __name__ == '__main__':
	updater = Updater(token='1089747994:AAGy05lbD93Tjov6dFEiKxRNrRz0jikARQQ', use_context=True)
	dispatcher = updater.dispatcher
	sched_handler = CommandHandler('sched', sched)
	group_handler = CommandHandler('setgroup', set_group)
	dispatcher.add_handler(sched_handler)
	dispatcher.add_handler(group_handler)
	updater.start_polling()