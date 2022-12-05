import uuid

from django.db import models

from .threat_model import ThreatModel


class TMParticipant(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    threat_model = models.ForeignKey(ThreatModel,
                                     on_delete=models.CASCADE,
                                     related_name='participants')

    def __repr__(self):
        return f'ThreatModel<{self.title}, {self.oid}>'

    def __str__(self):
        return f'ThreatModel<{self.title}, {self.oid}>'
