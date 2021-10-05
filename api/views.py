from requests import get

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .exceptions import GetNewReleaseError
from auth_management.spotify_oauth import SpotifyAuth
from auth_management.utils import is_user_authenticated, get_user_token


SPOTIFY_AUTH = SpotifyAuth()
SPOTIFY_API_URL = 'https://api.spotify.com'


class NewreleasesArtists(APIView):
    """Manage new releases on Spotify."""

    def get(self, request, format=None):
        # Check if user is authenticated
        is_authenticated = is_user_authenticated(request.session.session_key)

        # retrieve to spotify authrorization token
        if is_authenticated:
            token = get_user_token(request.session.session_key)
        else:
            # If not authenticated, redirect to the Spotify authentication url
            return redirect(SPOTIFY_AUTH.get_user())

        # request the spotify endpoint '/v1/browse/new-releases'
        limit = 50
        offset = 0
        url = SPOTIFY_API_URL + '/v1/browse/new-releases'
        response = get(
            url,
            params={'limit': limit, 'offset': offset},
            headers={
                'Authorization': f'{token.token_type} {token.access_token}'
            }
        )

        # Check status code
        print(response.status_code)
        if response.status_code not in [200, 201]:
            raise GetNewReleaseError(
                "Could not retrieve artists from the endpoint "
                f"'/v1/browse/new-releases': {response.text}"
            )

        # store data in a dictionary
        result = response.json()

        # Loop over the pagination to retrieve all albums
        while response.json()['albums']['next'] is not None:
            offset += limit
            response = get(
                url,
                params={'limit': limit, 'offset': offset},
                headers={
                    'Authorization': f'{token.token_type} {token.access_token}'
                }
            )

            if response.status_code not in [200, 201]:
                raise GetNewReleaseError(
                    "Could not retrieve artists from the endpoint "
                    f"'/v1/browse/new-releases': {response.text}"
                )

            result['albums'].update(response.json()['albums'])

        # Display response
        return Response(result)
