import uuid

from django.db import models


class Requirement(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    readable_id = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=512, blank=True)

    owasp_level = models.IntegerField(default=0)
    owasp_section = models.IntegerField(default=0)

    def __repr__(self):
        return f'Requirement<{self.readable_id}, {self.oid}>'

    def __str__(self):
        return f'Requirement<{self.readable_id}, {self.oid}>'
