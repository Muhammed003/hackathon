from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAllowAny(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
                request.user == obj.author or
                request.user == request.user.is_staff
        )


class IsReviewAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticate and request.user == obj.author



