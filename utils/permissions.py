from rest_framework.permissions import BasePermission, AllowAny


class IsAnonymous(BasePermission):
    """Allows access only to anonymous users."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_anonymous)


class CheckAuthenticatedElseIsAnonymous(BasePermission):
    """Allow permissions based on request method.
    `/api/authorize/`

    If GET:
        Allow anyone (to check if they're authenticated or not)
    If POST:
        Allow only Anonymous users to login
    """

    message = "You are already Authorized"

    def has_permission(self, request, view):
        if request.method == "GET":
            return AllowAny().has_permission(request, view)
        elif request.method == "POST":
            return IsAnonymous().has_permission(request, view)
