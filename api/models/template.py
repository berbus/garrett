import uuid

from django.db import models

from .requirement import Requirement


class Template(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)

    requirements = models.ManyToManyField(Requirement, blank=True)
