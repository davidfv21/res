from rest_framework import permissions
from .models import Waiter

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            print("HAAAAAAAAAAAA", request.user.waiter.charge )
            return request.user.waiter.charge == Waiter.MANAGER
        except Waiter.DoesNotExist:
            return False

class IsManagerOrAdminTables(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return (request.user.waiter.charge == Waiter.MANAGER or
                    request.user.waiter.charge == Waiter.ADMINTABLES)
        except Waiter.DoesNotExist:
            return False