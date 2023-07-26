from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователи могут редактировать только свои собственные объекты.
    """

    def has_object_permission(self, request, view, obj):

        # Разрешить просмотр любому пользователю
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить запись только владельцу объекта
        return obj.owner == request.user
