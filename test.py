from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler


def sched(update, context):
	class_name = context.args[0]
	week_day = context.args[1]
	context.bot.send_message(chat_id=update.effective_chat.id, text="Math\nLiterature")

if __name__ == '__main__':
	updater = Updater(token='1089747994:AAGy05lbD93Tjov6dFEiKxRNrRz0jikARQQ', use_context=True)
	dispatcher = updater.dispatcher
	sched_handler = CommandHandler('sched', sched)
	dispatcher.add_handler(sched_handler)
	updater.start_polling()