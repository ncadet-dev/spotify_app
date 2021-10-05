from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .exceptions import SpotifyCallbackError
from .spotify_oauth import SpotifyAuth
from .utils import update_or_create_user_token, is_user_authenticated

# Instanciate SpotifyAuth for use
SPOTIFY_AUTH = SpotifyAuth()


class getAuthUrl(APIView):
    """Obtain the url to authenticate the user to Spotify."""

    def get(self, request, format=None):
        return Response(
            {'url': SPOTIFY_AUTH.get_user()},
            status=status.HTTP_200_OK
        )


def spotify_callback(request, format=None):
    """Handle the response from Spotify after user authentication."""
    code = request.GET.get('code')
    if error := request.GET.get('error'):
        raise SpotifyCallbackError(
            "The following error was raised when tyring to authenticate to "
            f"Spotify: {error}"
        )

    # Request the token with the newly obtained code
    response = SPOTIFY_AUTH.get_user_token(code)

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    # Create a session if this one does not exits
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_token(
        request.session.session_key,
        access_token,
        refresh_token,
        expires_in,
        token_type
    )

    return redirect('api:new_releases')


class IsAuthenticated(APIView):
    """Inform whether the user is connected to Spotify."""

    def get(self, request, format=None):
        return Response(
            {
                'is_authenticated': is_user_authenticated(
                    request.session.session_key
                )
            }
        )
