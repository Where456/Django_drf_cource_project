import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import requests
from config.settings import TELEGRAM_BOT_API
from habit.models import GoodHabit
from users.models import User


class MailingHabitService:
    """Сервис рассылки полезных привычек"""
    telegram_api = TELEGRAM_BOT_API
    BASE_URL = f"https://api.telegram.org/bot{telegram_api}"

    def __init__(self, habit):
        self.habit = habit

    def create_task(self):
        """Регистрация периодической задачи для рассылки"""
        crontab = self.crontab_create()
        PeriodicTask.objects.create(crontab=crontab, name=str(self.habit), task='habit_tracker.tasks.send_a_task',
                                    args=json.dumps([self.habit.pk]))

    def crontab_create(self):
        """Создание CRONTAB для выполнения периодических задач"""
        minute = self.habit.time.minute
        hour = self.habit.time.hour

        if self.habit.frequency == 'EVERY DAY':
            day_of_week = '*'

        elif self.habit.frequency == 'EVERY OTHER DAY':
            day_of_week = '*/2'

        elif self.habit.frequency == 'WEEK':
            day_of_week = self.habit.date.weekday()

        schedule, _ = CrontabSchedule.objects.get_or_create(minute=minute, hour=hour, day_of_week=day_of_week,
                                                            day_of_month='*', month_of_year='*')

        return schedule

    def get_update_and_save_response(self):
        """Обновление запросов и сохранение ID чата в БД"""
        response = requests.get(f'{self.BASE_URL}/getUpdates')
        for i in response.json()['result']:
            tg_username = i['message']['from']['username']
            tg_chat_id = i['message']['from']['id']
            if User.objects.filter(tg_username=tg_username).exists():
                user = User.objects.get(tg_username=tg_username)
                user.update_tg_chat_id(tg_chat_id)

    def send_message(self):
        """Отправка сообщения пользователю об одном действии по расписанию"""
        user = self.habit.user
        if user.tg_chat_id:
            data = {"chat_id": user.tg_chat_id, "text": str(self.habit)}
            requests.post(f'{self.BASE_URL}/sendMessage', data=data)

    def send_message_all_habit_tracker(self):
        """Отправка пользователю всего трекера привычек"""
        users = User.objects.all()
        for user in users:
            all_text = 'Планы на сегодня:\n'
            num = 1
            texts = GoodHabit.objects.filter(user=user)
            for text in texts:
                all_text = all_text + f"{num}. " + f"{str(text)}\n"
                num += 1
            data = {"chat_id": user.tg_chat_id, "text": all_text}
            requests.post(f'{self.BASE_URL}/sendMessage', data=data)