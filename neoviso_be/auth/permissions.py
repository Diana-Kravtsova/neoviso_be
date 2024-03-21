from functools import wraps

from django.contrib.auth.models import Permission
from django.http import JsonResponse

from neoviso_be.response import Response


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)


def user_has_permission(user, perm_name):
    user_permissions = get_user_permissions(user)
    return user_permissions.filter(codename=perm_name).exists()


def has_permission(perm_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and user_has_permission(request.user, perm_name):
                return view_func(request, *args, **kwargs)
            return JsonResponse(Response(message="Permission denied").__dict__, status=403)
        return _wrapped_view
    return decorator
