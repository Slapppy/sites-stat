from rest_framework import permissions
from web.models import User, Counter


class IsCreatorAndReadOnly(permissions.BasePermission):
    message = "Данные можно узнать только о своих счетчиках"

    def has_permission(self, request, view):
        counter_id = request.GET.get("id")
        user = User.objects.get(id=request.user.id)
        is_creator = user.counters.filter(id=counter_id)
        return request.method in permissions.SAFE_METHODS and is_creator
