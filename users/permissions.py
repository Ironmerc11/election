
from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
    


class IsAdminOrSuperUser(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_admin))
    