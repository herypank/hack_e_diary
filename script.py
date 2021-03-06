from datacenter.models import (
    Chastisement, Schoolkid, Mark, Lesson, Commendation)
from sys import exit


def get_schoolkid_info(child_full_name):
    child_info = Schoolkid.objects.get(full_name__contains=child_full_name)
    return child_info


def change_bad_mark(schoolkid_info):
    all_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid_info, points__in=[2, 3])
    for bad_mark in all_bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid_info):
    all_bad_marks = Chastisement.objects.filter(schoolkid=schoolkid_info)
    for bad_mark in all_bad_marks:
        bad_mark.delete()


def create_commendation(schoolkid_info, a_lesson_for_praise,
                        praise_for_the_lesson):
    lessons_info = Lesson.objects.filter(
        group_letter=schoolkid_info.group_letter,
        year_of_study=schoolkid_info.year_of_study,
        subject__title=a_lesson_for_praise).order_by('-date').first()
    if lessons_info is None:
        raise AttributeError
    Commendation.objects.create(
        teacher=lessons_info.teacher,
        subject=lessons_info.subject,
        created=lessons_info.date,
        schoolkid=schoolkid_info,
        text=praise_for_the_lesson)


def fix_everything(child_full_name):
    try:
        schoolkid_info = get_schoolkid_info(child_full_name)
    except Schoolkid.MultipleObjectsReturned:
        exit('Ошибка найдено слишком много учеников.')
    except Schoolkid.DoesNotExist:
        exit('Ошибка имя не найдено.')
    print('Ученик найден')
    remove_chastisements(schoolkid_info)
    change_bad_mark(schoolkid_info)
    texts_commendations = [
        "Молодец!", "Отлично!", "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!", "Прекрасно!",
        "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!",
        "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!",
        "Очень хороший ответ!", "Талантливо!",
        "Ты сегодня прыгнул выше головы!", "Я поражен!",
        "Уже существенно лучше!", "Потрясающе!",
        "Замечательно!", "Прекрасное начало!",
        "Так держать!", "Ты на верном пути!",
        "Здорово!", "Это как раз то, что нужно!", "Я тобой горжусь!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!", "Я вижу, как ты стараешься!",
        "Ты растешь над собой!", "Ты многое сделал, я это вижу!",
        "Теперь у тебя точно все получится!"]
    try:
        count_add_commendation = int(input(
            'Введите сколько комментариев похвалы хотите добавить: '))
    except ValueError:
        exit('Ошибка ввода, введите положительное целое число.')
    for commendation in range(count_add_commendation):
        a_lesson_for_praise = input('Введите предмет для похвалы: ')
        print('Выберите похвалу')
        for num_commendation, commendation in enumerate(
                texts_commendations):
            print(str(num_commendation + 1) + '. ' + commendation)
        try:
            praise_for_the_lesson = texts_commendations[
                int(input('Введите номер похвалы: ')) - 1]
        except (IndexError, ValueError):
            exit('Ошибка ввода, попробуйте снова.')
        try:
            create_commendation(
                schoolkid_info, a_lesson_for_praise, praise_for_the_lesson)
        except AttributeError:
            exit('Ошибка названия предмета. Пример правильного ввода "Краеведение".')
        print('Похвала успешно добавлена.')
    print('Скрипт успешно выполнил работу.',
        'Не забудьте удалить папку hack_e-diary.')
