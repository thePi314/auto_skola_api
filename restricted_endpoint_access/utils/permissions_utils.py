from restricted_endpoint_access.models.permission import Permission
from restricted_endpoint_access.models.role import Role


class PermissionUtils:
    @staticmethod
    def clear_permissions():
        Permission.objects.all().delete()

    @staticmethod
    def generate_permissions(routes):
        PermissionUtils.clear_permissions()

        for route in routes:
            PermissionUtils.generate_permission(**route)

    @staticmethod
    def generate_permission(name, route, methods, roles):
        for method in methods:
            permission = Permission.objects.create(
                name=name,
                method=method,
                url_pattern=route
            )

            if roles:
                for role in roles:
                    if not role.permissions.filter(id=permission.id).exists():
                        role.permissions.add(permission)
