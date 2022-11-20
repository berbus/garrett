from django.db import models
from .service import Service


class JiraIssue(models.Model):
    jira_id = models.CharField(primary_key=True, max_length=64)
    jira_key = models.CharField(max_length=64, unique=True)
    services = models.ManyToManyField(Service, related_name='jira_issues')

    def __repr__(self):
        return f'JiraIssue<{self.jira_id}, {self.jira_key}>'

    def __str__(self):
        return f'JiraIssue<{self.jira_id}, {self.jira_key}>'
