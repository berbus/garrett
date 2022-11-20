import uuid

from django.db import models


class JiraTransition(models.Model):

    class GarrettActions(models.TextChoices):
        CREATE_REVIEW = 'CREATE_REVIEW'
        COMPLETE_REVIEW = 'COMPLETE_REVIEW'
        CREATE_THREAT_MODEL = 'CREATE_THREAT_MODEL'
        COMPLETE_THREAT_MODEL = 'COMPLETE_THREAT_MODEL'
        CREATE_TEST = 'CREATE_TEST'
        COMPLETE_TEST = 'COMPLETE_TEST'

    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transition_alias = models.CharField(max_length=64, default='')
    transition_id = models.CharField(max_length=64)
    garrett_action = models.CharField(max_length=21,
                                      choices=GarrettActions.choices,
                                      unique=True)

    def __repr__(self):
        return f'JiraTransition<{self.oid}, {self.garrett_action}->{self.transition_id}>'

    def __str__(self):
        return f'JiraTransition<{self.oid}, {self.garrett_action}->{self.transition_id}>'
