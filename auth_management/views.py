from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .spotify_oauth import SpotifyAuth

# Instanciate SpotifyAuth for use
SPOTIFY_AUTH = SpotifyAuth()


class getAuthUrl(APIView):
    """Obtain the url to authenticate the user to Spotify."""

    def get(self, request, format=None):
        return Response(
            {'url': SPOTIFY_AUTH.get_user()},
            status=status.HTTP_200_OK
        )
