from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated


class IsAnonymous(BasePermission):
    """Allows access only to anonymous users."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_anonymous)


class CheckAuthenticatedElseIsAnonymous(BasePermission):
    """Allow permissions based on request method.
    `/auth/authorize/`

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


class TimetableRoutePermission(BasePermission):
    """Manage Permissions of Timetable View based on request method.
    `/api/timetable/`

    If GET:
        Allow Authenticated Users of any type
    If POST:
        Allow only Teachers, Management and Admins (users with user_type=`t`, `m`, `a`)
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return IsAuthenticated().has_permission(request, view)
        elif request.method == "POST":
            return bool(request.user.is_anonymous is not True and request.user.user_type in ("t", "m", "a"))
