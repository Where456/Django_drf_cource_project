from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'Доступ ограничен! Вы не являетесь владельцем записи'

    class IsOwner(permissions.BasePermission):
        """ Проверка прав автора публикации"""

        def has_permission(self, request, view):
            """Автор публикации может редактировать и удалять только свои объекты"""
            if request.user == view.get_object().user:
                return request.method in ['PUT', 'PATCH', 'DELETE']

            return False