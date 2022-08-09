import datetime
import uuid

from django.db import models

from .security_test import SecurityTest
from .requirement import Requirement


class TestCase(models.Model):

    class TestStatus(models.TextChoices):
        PENDING = 'PENDING'
        FAIL = 'FAIL'
        SUCCESS = 'SUCCESS'

    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_date = models.DateField(('Date'), default=datetime.date.today)
    description = models.TextField(default='', blank=True)
    status = models.CharField(max_length=10,
                              choices=TestStatus.choices,
                              default=TestStatus.PENDING)

    security_test = models.ForeignKey(SecurityTest,
                                      on_delete=models.CASCADE,
                                      related_name='tests')
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)

    def __repr__(self):
        return f'TestCase<{self.status}, {self.oid}>'

    def __str__(self):
        return f'TestCase<{self.status}, {self.oid}>'
