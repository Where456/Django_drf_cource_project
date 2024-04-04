from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from habit.models import GoodHabit, Habit
from habit.paginations import HabitPagination
from habit.permissions import IsOwner
from habit.serializers import HabitSerializer, GoodHabitSerializer
from habit.services import MailingHabitService
from habit.tasks import send_a_task


# from habit.paginations import HabitPagination
# from habit.permissions import IsOwner
# from habit.serliazers import GoodHabitSerializer
# from habit.services import MailingHabitService
# from habit.tasks import send_a_task


class HabitViewSet(viewsets.mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    Представление модели привычки, которое включает в себя механизм CRUD
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPagination

    def get_queryset(self):
        """Пользователь может видеть только свои приятные привычки с признаком приятной привычки"""
        user = self.request.user
        if user.is_staff:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(user=user, is_pleasant_habit=True, is_published=True)

    def perform_create(self, serializer):
        """При создании приятной привычки присваивается автор"""
        serializer.save(user=self.request.user)


class GoodHabitCreateAPIView(generics.CreateAPIView):
    """
    Создание привычки.
    """
    serializer_class = GoodHabitSerializer

    def perform_create(self, serializer):
        """При создании полезной привычки присваивается автор"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        habit = GoodHabit.objects.get(id=serializer.data['id'])
        if habit.is_published:
            # создание периодической задачи, которая отправляет автору напоминание о выполнении действия
            telegram_message = MailingHabitService(habit)
            telegram_message.create_task()
            # отправка автору сообщения с полезной привычкой
            send_a_task(habit.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GoodHabitListAPIView(generics.ListAPIView):
    """
    Отображение всех привычек.
    """
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    pagination_class = HabitPagination


class GoodHabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Отображение одной привычки.
    """
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()


class GoodHabitUpdateAPIView(generics.UpdateAPIView):
    """
    Изменение привычки.
    """
    serializer_class = GoodHabitSerializer
    queryset = GoodHabit.objects.all()
    permission_classes = [IsOwner]


class GoodHabitDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление привычки.
    """
    queryset = GoodHabit.objects.all()
    permission_classes = [IsOwner]
