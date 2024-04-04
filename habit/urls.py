from rest_framework.routers import DefaultRouter
from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitViewSet, GoodHabitCreateAPIView, GoodHabitListAPIView, GoodHabitRetrieveAPIView, \
    GoodHabitUpdateAPIView, GoodHabitDestroyAPIView

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = [

    # GoodHabit
    path('good_habits/create/', GoodHabitCreateAPIView.as_view(), name='good_habit_create'),
    path('good_habits/', GoodHabitListAPIView.as_view(), name='good_habit_list'),
    path('good_habits/<int:pk>/', GoodHabitRetrieveAPIView.as_view(), name='good_habit_retrieve'),
    path('good_habits/update/<int:pk>/', GoodHabitUpdateAPIView.as_view(), name='good_habit_update'),
    path('good_habits/delete/<int:pk>/', GoodHabitDestroyAPIView.as_view(), name='good_habit_delete'),

] + router.urls