import uuid

from django.db import models
from .service import Service


class JiraIssue(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jira_id = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=64)
    services = models.ManyToManyField(Service, related_name='jira_issues')

    def __repr__(self):
        return f'JiraIssue<{self.oid}, {self.jira_id}>'

    def __str__(self):
        return f'JiraIssue<{self.oid}, {self.jira_id}>'
