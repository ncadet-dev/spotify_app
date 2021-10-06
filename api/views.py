from datetime import date

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import NewReleases
from .serializers import NewReleasesSerializer
from .utils import assign_artists_to_new_releases, merge_get_artists_requests
from auth_management.spotify_oauth import SpotifyAuth
from auth_management.utils import is_user_authenticated, get_user_token


SPOTIFY_AUTH = SpotifyAuth()
SPOTIFY_API_URL = 'https://api.spotify.com'


class NewReleasesView(APIView):
    """Manage new releases on Spotify."""

    def get(self, request, format=None):
        """List artists from today's new releases."""
        # If new releases have been stored in DB, retrieve it and return it
        new_releases = NewReleases.objects.filter(
            created_at__date=date.today()
        )

        if new_releases.exists():
            return Response(NewReleasesSerializer(new_releases[0]).data)

        # Check if user is authenticated
        is_authenticated = is_user_authenticated(request.session.session_key)

        # if user is not authenticated redirect to Spotify login page
        if not is_authenticated:
            return redirect(SPOTIFY_AUTH.get_user())

        # Retrieve to spotify authrorization token
        token = get_user_token(request.session.session_key)

        # Request the spotify endpoint '/v1/browse/new-releases'
        url = SPOTIFY_API_URL + '/v1/browse/new-releases'
        data = merge_get_artists_requests(
            url, token.token_type, token.access_token, 50, 0
        )

        # Instanciate NewRelease and assign artists to it
        new_releases = assign_artists_to_new_releases(data)

        return Response(NewReleasesSerializer(new_releases).data)
