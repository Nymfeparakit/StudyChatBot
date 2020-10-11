import main
import json

TEACHER_CODE = "qweqwe"


def teacher_auth(update, context):
    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверно заданы параметры команды /teach_auth")
        return

    entered_code = context.args[0]
    if entered_code == TEACHER_CODE:
        query = f"insert into users (id, class, surname) " \
                f"values({update.message.from_user.id}, 't', '')"
        main.execute_query(query)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Вы успешно авторизованы в качестве преподавателя!")

def get_user_id_by_surname(surname):
    query = f"select id from users where surname='{surname}'"
    return main.execute_query(query)[0]["id"]

def get_test_result(update, context):
    if len(context.args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверно заданы параметры команды /result")
        return

    test_id = context.args[0]
    surname = context.args[1]

    context.bot.send_message(chat_id=update.effective_chat.id, text="check auth...")
    check_id = update.message.from_user.id
    #context.bot.send_message(chat_id=update.effective_chat.id,
                             #text=check_id)

    query = f"select class from users where id={check_id}"
    check_res = main.execute_query(query)[0]["class"]
    #print("check_res: ", check_res)
    if (check_res != "t"):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"У вас нет соответсвующих прав доступа")
        return

    user_id = get_user_id_by_surname(surname)
    query = f"select result from performed_tests " \
            f"where user_id={user_id} and test_id='{test_id}'"
    result = json.loads(main.execute_query(query)[0]["result"])
    if len(result) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Данные не найдены")
        return

    success_percentage = round(sum(result)/len(result)*100,1)
    context.bot.send_message(chat_id=update.effective_chat.id,
                         text=result)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Тест выполнен на {success_percentage}%")





