import json
import test
import ocr
def get_test_result(test_id, user_answers):
    correct_ans = get_test_correct_answers(test_id)
    # сравниваем ответы
    test_result = []
    for (correct_answer, user_answer) in zip(correct_ans, user_answers):
        test_result.append(correct_answer == user_answer)
    print("correct answer: ", correct_ans)
    return test_result


def get_test_correct_answers(test_id):
    query = f"select answers from test_keys where id='{test_id}'"
    return test.execute_query(query)[0]["answers"]


def load_test_results(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    user_id = user.id
    # распознали ответы на фото
    # из фото также получаем - фамилия,tests_check.load_test_results класс, дата, номер теста
    surname = 'aaaa'
    group = 'bbbb'
    test_date = 'dddd'
    test_num = 'T5'
    user_answers = "qweryt"
    # определяем правильность ответов
    test_res = json.dumps(get_test_result(test_num, user_answers))
    print("test res:", test_res)
    # загружаем ответы в БД
    query = f"insert into performed_tests (user_id, test_id, date, result) " \
            f"values({user_id}, '{test_num}', '{test_date}', '{test_res}')"
    test.execute_query(query)
