from django.db import models
from django.utils import timezone


class Block(models.Model):
    index = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    prev_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    event_type = models.CharField(max_length=50)
    event_data = models.JSONField()

    class Meta:
        ordering = ["index"]

    def __str__(self):
        return f"Block {self.index} - {self.event_type}"
