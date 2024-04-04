from celery import shared_task

from habit.models import GoodHabit
from habit.services import MailingHabitService


@shared_task
def send_all_tracker():
    """Отправка списка дел на день в 06:30 каждый день (настройка через admin/)"""
    telegram = MailingHabitService
    MailingHabitService.get_update_and_save_response(telegram)
    MailingHabitService.send_message_all_habit_tracker(telegram)


@shared_task
def send_a_task(good_habit_id):
    """Отправка привычки по расписанию"""
    good_habit = GoodHabit.objects.get(pk=good_habit_id)
    telegram_task = MailingHabitService(good_habit)
    telegram_task.send_message()