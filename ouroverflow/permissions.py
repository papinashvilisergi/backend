from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrIsAuthenticated(BasePermission):
    """
    Custom permission to allow read-only access to unauthenticated users.
    Authenticated users can perform all actions.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow read-only methods for everyone
        return request.user and request.user.is_authenticated  # Allow all methods for authenticated users
