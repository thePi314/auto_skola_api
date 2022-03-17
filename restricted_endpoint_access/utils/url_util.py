from django.urls import URLPattern, re_path

from restricted_endpoint_access.models.role import Role

class RestrictedURLPattern(URLPattern):
    def __init__(
        self,
        pattern,
        callback,
        default_args=None,
        name=None,
        role_namespaces=None
    ):
        super().__init__(pattern, callback, default_args, name)
        self.name = name
        self.roles = Role.objects.filter(code__in=role_namespaces).all() \
            if role_namespaces and len(role_namespaces) > 0 else []


def rea(
    regex,
    view,
    kwargs=None,
    name=None,
    role_namespaces=None
):
    url_pattern = re_path(regex, view, kwargs, name)
    return RestrictedURLPattern(
        url_pattern.pattern,
        url_pattern.callback,
        default_args=url_pattern.default_args,
        name=url_pattern.name,
        role_namespaces=role_namespaces
    )
