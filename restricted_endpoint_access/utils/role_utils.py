from restricted_endpoint_access.models.role import Role
from restricted_endpoint_access.constants.role import ROLES


class RoleUtils:
    @staticmethod
    def generate_built_in_roles():
        for role in ROLES:
            if not Role.objects.filter(code=role.get("code")):
                Role.objects.create(**role)
            else:
                del role['id']
                Role.objects.filter(code=role.get("code")).update(**role)
