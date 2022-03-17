from django.contrib.postgres.fields import JSONField
from django.db import models


class UserRoles(models.Model):
    user = models.ForeignKey("api.User", on_delete=models.CASCADE, related_name="roles")
    role = models.ForeignKey("restricted_endpoint_access.Role", on_delete=models.CASCADE, related_name="users")
    created_at = models.DateTimeField(auto_now=True)
    restricted = models.BooleanField(default=False)
    restricted_at = models.DateTimeField(blank=True, null=True)
    metadata = JSONField(null=True, blank=True)
