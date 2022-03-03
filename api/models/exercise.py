import datetime
import uuid

from django.db import models

from .service import Service
from .template import Template


class Exercise(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    creation_date = models.DateField(default=datetime.date.today)
    finished = models.BooleanField(default=False)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Exercise<{self.title}, {self.oid}>'

    def __str__(self):
        return f'Exercise<{self.title}, {self.oid}>'
