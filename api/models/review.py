import datetime
import uuid

from django.db import models

from .service import Service
from .jira_issue import JiraIssue


class Review(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    creation_date = models.DateField(default=datetime.date.today)
    completion_date = models.DateField(default=None, null=True)

    services = models.ManyToManyField(Service, blank=True)
    jira_issue = models.OneToOneField(JiraIssue, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'Review<{self.title}, {self.oid}>'

    def __str__(self):
        return f'Review<{self.title}, {self.oid}>'
