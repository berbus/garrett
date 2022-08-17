import datetime
import uuid

from django.db import models


class Service(models.Model):

    class ServiceStatus(models.TextChoices):
        SIGNED_OFF = 'SIGNED_OFF'
        NOTIFICATION = 'NOTIFICATION'
        THREAT_MODEL = 'THREAT MODEL'
        TESTING = 'TESTING'

    class Meta:
        unique_together = ('confluence_parent_id', 'confluence_space')

    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    creation_date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=20,
                              choices=ServiceStatus.choices,
                              default=ServiceStatus.SIGNED_OFF)

    confluence_parent_id = models.IntegerField(null=True)
    confluence_space = models.CharField(max_length=64, null=True)

    def __repr__(self):
        return f'Service<{self.oid}, {self.name}>'

    def __str__(self):
        return f'Service<{self.oid}, {self.name}>'
