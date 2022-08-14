import datetime
import uuid

from django.db import models

from .service import Service
from .template import Template
from .review import Review


class SecurityTest(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    creation_date = models.DateField(default=datetime.date.today)
    completion_date = models.DateField(default=None, null=True)

    services = models.ManyToManyField(Service, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'SecurityTest<{self.title}, {self.oid}>'

    def __str__(self):
        return f'SecurityTest<{self.title}, {self.oid}>'
