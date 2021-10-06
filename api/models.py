from django.utils import timezone

from django.db import models


class NewReleases(models.Model):
    """Store the date of new releases and artists in relation to it."""
    created_at = models.DateTimeField(default=timezone.now)
    artists = models.ManyToManyField('Artist', related_name='new_release')


class Artist(models.Model):
    """Store information about an artist."""
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    uri = models.CharField(max_length=100)
    api_href = models.URLField()
    spotify_link = models.URLField()
