from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """ Проверка прав пользователя"""
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object()