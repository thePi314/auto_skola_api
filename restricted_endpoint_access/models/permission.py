import uuid

from django.db import models


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=60, null=True, blank=True)
    url_pattern = models.TextField(null=True, blank=True)
