from config import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}

FREQUENCY = [
    ('EVERY DAY', 'раз в день'),
    ('EVERY OTHER DAY', 'через день'),
    ('EVERY WEEK', 'раз в неделю'),
]


class Habit(models.Model):
    """
    Модель привычки
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='создатель привычки',
                             **NULLABLE)
    place = models.CharField(max_length=200, verbose_name='место')
    time = models.DateTimeField(verbose_name='время выполнения привычки')
    action = models.CharField(max_length=200, verbose_name='действие')
    duration = models.PositiveIntegerField(default=120, verbose_name='время на выполнение в секундах')
    is_published = models.BooleanField(default=True, verbose_name='признак публичности привычки')
    is_pleasant_habit = models.BooleanField(default=True, verbose_name='признак приятной привычки')

    def __str__(self):
        return f'я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Добавить привычку'
        verbose_name_plural = 'Настройка привычки'


class GoodHabit(models.Model):
    """
    Модель полезной привычки
    """
    pleasant_habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name='приятная привычка', **NULLABLE)
    reward = models.TextField(verbose_name='вознаграждение после выполнения', **NULLABLE)
    frequency = models.CharField(max_length=100, default='EVERY DAY', choices=FREQUENCY, verbose_name='Периодичность')

    def __str__(self):
        return f'{self.pleasant_habit}'

    class Meta:
        verbose_name = 'Добавить полезную привычку'
        verbose_name_plural = 'полезные привычки'
        ordering = ('pleasant_habit',)
