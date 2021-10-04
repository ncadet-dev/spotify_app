from django.db import models


class SpotifyToken(models.Model):
    """A model to store and refresh Spotify tokens."""
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=250)
    refresh_token = models.CharField(max_length=250)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
