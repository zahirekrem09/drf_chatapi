from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from django.contrib.auth import authenticate


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        from user_control.views import decodeJWT
        user = decodeJWT(request.META['HTTP_AUTHORIZATION'])
        if not user:
            return False
        request.user = user
        if request.user and request.user.is_authenticated:
            from user_control.models import CustomUser
            CustomUser.objects.filter(id=request.user.id).update(
                is_online=timezone.now())
            return True
        return False


class IsAuthenticatedOrReadCustom(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            from user_control.models import CustomUser
            CustomUser.objects.filter(id=request.user.id).update(
                is_online=timezone.now())
            return True
        return False
