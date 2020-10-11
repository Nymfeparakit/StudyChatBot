from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
import pymysql
from pymysql.cursors import DictCursor
import tests_check
import teacher
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

HOST = 'sql7.freesqldatabase.com'
USER = 'sql7369890'
PASSWORD = 'bjJP6JdVrq'
DB = 'sql7369890'
CHARSET = 'utf8mb4'

def get_weekday_name_from_number(day_num):
	return {0: "Monday",
			1: "Tuesday",
			2: "Wednesday",
			3: "Thursday",
			4: "Friday",
			5: "Saturday",
			6: "Sunday"}.get(day_num, "Nonday")

def get_weekday_from_short_name(day_name):
	if day_name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
		return day_name

	return {"Mon": "Monday",
			"Tue": "Tuesday",
			"Wed": "Wednesday",
			"Thu": "Thursday",
			"Fri": "Friday",
			"Sat": "Saturday",
			"Sun": "Sunday"}.get(day_name, "Nonday")

def sched(update, context):
	if len(context.args) == 1:
		arg = context.args[0]
		if arg == "today":
			msg_date = update.message.date
			week_day = get_weekday_name_from_number(msg_date.weekday())
			group_name = get_group(update.message.from_user.id)
			subjects_list = get_schedule_for_weekday(week_day, group_name)
			if len(subjects_list) == 0:
				context.bot.send_message(chat_id=update.effective_chat.id, text="Данные не найдены")
			context.bot.send_message(chat_id=update.effective_chat.id, text=subjects_list)
		else:
			week_day = get_weekday_from_short_name(context.args[0])
			if week_day == "Nonday":
				context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное название дня недели")
				return
			group_name = get_group(update.message.from_user.id)
			subj_list = get_schedule_for_weekday(week_day, group_name)
			if len(subj_list) == 0:
				context.bot.send_message(chat_id=update.effective_chat.id, text="Данные не найдены")
				return
			context.bot.send_message(chat_id=update.effective_chat.id, text=subj_list)
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Неверно заданы параметры команды /sched")


def help(update, context):
	help_text =  "Список команд:\n" \
		   "/setgroup <Класс> - Указать свой класс\n" \
		   "/group - Узнать свой класс\n" \
		   "/sched today - Расписание на сегодня\n" \
		   "/sched <День недели> - Расписание на день недели\n" \
			"*** Для преподавателей ***\n" \
		   "/teach_auth <Код> - Авторизация в качестве преподавателя\n" \
		   "/result <Номер теста> <Фамилия ученика> - Узнать результаты тестов ученика\n" \
		   "****************************\n" \
		   "Для проверки теста приложите его фотографию\n"
	context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def execute_query(query):
	connection = pymysql.connect(
		host=HOST,
		user=USER,
		password=PASSWORD,
		db=DB,
		charset=CHARSET,
		cursorclass=DictCursor
	)

	try:
		result = []
		with connection.cursor() as cursor:
			cursor.execute(query)
			for row in cursor:
				result.append(row)
			connection.commit()
	except:
		connection.close()
	connection.close()
	return result

def get_schedule_for_weekday(weekday, group):
	query = f"select subject from sched where date='{weekday}' and class='{group}'"
	subjects = execute_query(query)
	subjects_list = '\n'.join([subj_dict['subject'] for subj_dict in subjects])
	return subjects_list

def get_group(user_id):
	query = f"select class from users where id={user_id}"
	group = execute_query(query)[0]['class']
	return group

def show_user_group(update, context):
	if len(context.args) != 0:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Неверно заданы параметры команды /group")
		return
	group_name = get_group(update.message.from_user.id)
	context.bot.send_message(chat_id=update.effective_chat.id, text=f"{group_name}")

def set_group(update, context):
	if len(context.args) != 1:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Неверно заданы параметры команды /setgroup")
		return
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


def start(update, context):
	keyboard = [
		[
			InlineKeyboardButton("Option 1", callback_data='1'),
			InlineKeyboardButton("Option 2", callback_data='2'),
		],
		[InlineKeyboardButton("Option 3", callback_data='3')],
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	update.message.reply_text('Please choose:', reply_markup=reply_markup)


if __name__ == '__main__':
	updater = Updater(token='1089747994:AAGy05lbD93Tjov6dFEiKxRNrRz0jikARQQ', use_context=True)
	dispatcher = updater.dispatcher
	sched_handler = CommandHandler('sched', sched)
	group_handler = CommandHandler('group', show_user_group)
	get_group_handler = CommandHandler('setgroup', set_group)
	test_img_handler = MessageHandler(Filters.photo, tests_check.load_test_results)
	auth_teacher_handler = CommandHandler('teach_auth', teacher.teacher_auth)
	get_test_result_handler = CommandHandler('result', teacher.get_test_result)
	help_handler = CommandHandler('help', help)
	dispatcher.add_handler(sched_handler)
	dispatcher.add_handler(group_handler)
	dispatcher.add_handler(get_group_handler)
	dispatcher.add_handler(test_img_handler)
	dispatcher.add_handler(auth_teacher_handler)
	dispatcher.add_handler(get_test_result_handler)
	dispatcher.add_handler(help_handler)
	# updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.start_polling()