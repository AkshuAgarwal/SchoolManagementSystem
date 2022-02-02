from __future__ import annotations

from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_staff
