import test

TEACHER_CODE = "qweqwe"


def teacher_auth(update, context):
    entered_code = context.args[0]
    if entered_code == TEACHER_CODE:
        query = f"insert into users (id, class, surname) " \
                f"values({update.message.from_user.id}, 't', '')"
        test.execute_query(query)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Вы успешно авторизованы в качестве преподавателя!")
