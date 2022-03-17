import uuid

from django.db import models

from restricted_endpoint_access.models.permission import Permission


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    permissions = models.ManyToManyField("restricted_endpoint_access.Permission", related_name="roles")

    def permission_exists(self, method, name):
        return self.permissions.filter(name=name, method=method).exists()

    def attach_permission(self, method, name):
        self.permissions.add(Permission.objects.filter(method=method, name=name).first())

    def detach_permission(self, method, name):
        if self.permission_exists(method, name):
            self.permissions.remove(Permission.objects.filter(method=method, name=name).first())
