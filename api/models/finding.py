import datetime
import uuid

from django.db import models

from .test_case import TestCase
from .security_test import SecurityTest


class Finding(models.Model):

    class Impact(models.TextChoices):
        INFO = 'INFORMATIONAL'
        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'
        CRITICAL = 'CRITICAL'

    class FindingStatus(models.TextChoices):
        PENDING = 'PENDING'
        FIXED = 'FIXED'

    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(default='', blank=True)
    evidence = models.TextField(default='', blank=True)
    creation_date = models.DateField(default=datetime.date.today)
    impact = models.CharField(max_length=13, choices=Impact.choices, default=Impact.INFO)
    status = models.CharField(max_length=7,
                              choices=FindingStatus.choices,
                              default=FindingStatus.PENDING)

    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='findings')
    security_test = models.ForeignKey(SecurityTest,
                                      on_delete=models.CASCADE,
                                      related_name='findings')
