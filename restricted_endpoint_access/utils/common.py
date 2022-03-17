from rest_framework import permissions

from django.urls import resolve

from restricted_endpoint_access.models.permission import Permission


class HasREAPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        method = request.method.lower()
        name = resolve(request.path_info).url_name

        permission = Permission.objects.filter(method=method, name=name).first()
        if permission:
            if not request.user.roles.filter(role__permissions__id=permission.id).exists():
                return False

        return True
