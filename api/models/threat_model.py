import datetime
import uuid

from django.db import models

from .review import Review
from .service import Service


class ThreatModel(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    creation_date = models.DateField(default=datetime.date.today)
    completion_date = models.DateField(default=None, null=True)

    summary = models.TextField(default='', blank=True)
    business_logic_text = models.TextField(default='', blank=True)
    boundaries_text = models.TextField(default='', blank=True)

    services = models.ManyToManyField(Service, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'ThreatModel<{self.title}, {self.oid}>'

    def __str__(self):
        return f'ThreatModel<{self.title}, {self.oid}>'
