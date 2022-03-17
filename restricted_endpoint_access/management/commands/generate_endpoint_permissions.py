# python3 manage.py generate_endpoint_permissions
import logging
import inspect

from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern

from restricted_endpoint_access.constants.view_map import METHODS, VIEW_MAP
from restricted_endpoint_access.utils.instance_loader import get_class
from restricted_endpoint_access.utils.role_utils import RoleUtils
from restricted_endpoint_access.utils.permissions_utils import PermissionUtils


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generating permissions"

    def handle(self, *args, **options):
        RoleUtils.generate_built_in_roles()
        PermissionUtils.generate_permissions(collect_urls())


def find_methods(class_):
    methods = []
    for attr in inspect.getmembers(class_):
        if attr[0] in METHODS:
            methods.append(attr[0])
    return methods


def get_view_methods(view_path, actions={}):
    class_ = get_class(view_path)
    default = ""

    parents = list(inspect.getmro(class_))
    while len(parents) > 0:
        current = parents.pop(0)
        if current.__name__ in VIEW_MAP.keys():
            default = current.__name__
            break

    try:
        return list(set(find_methods(class_) + list(actions.keys()) + VIEW_MAP.get(default, [])))
    except Exception as ex:
        pass
    return []


IGNORE_URLS = [ '__debug__/']


def collect_urls(urls=None, root="", data=[]):
    if urls is None:
        urls = get_resolver().url_patterns

    for url in urls:
        if hasattr(url, "url_patterns"):
            if url.pattern._route not in IGNORE_URLS:
                data = collect_urls(url.url_patterns, f"{root}{url.pattern._route}", data)
            continue

        if isinstance(url, URLPattern):
            data.append({
                "name": url.name,
                "route": f"{root}{url.pattern._regex[1:]}",
                "methods": get_view_methods(url.lookup_str, url.callback.__dict__.get('actions', {})),
                "roles": url.__dict__.get('roles', None)
            })
    return data
