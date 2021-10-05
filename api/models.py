from django.utils import timezone

from django.db import models


class ArtistsFromNewReleases(models.Model):
    """Store the data related to artists from a day's releases."""
    created_at = models.DateField(default=timezone.now)
    artists = models.JSONField(default=None)
