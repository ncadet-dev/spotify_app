from datetime import date
from requests import get

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ArtistsFromNewReleases
from .exceptions import GetNewReleaseError
from .utils import albums_dict_to_artists_list
from auth_management.spotify_oauth import SpotifyAuth
from auth_management.utils import is_user_authenticated, get_user_token


SPOTIFY_AUTH = SpotifyAuth()
SPOTIFY_API_URL = 'https://api.spotify.com'


class NewreleasesArtists(APIView):
    """Manage new releases on Spotify."""

    def get(self, request, format=None):
        # If new releases have been stored in DB, retrieve it and return it
        new_releases = ArtistsFromNewReleases.objects.filter(
            created_at__date=date.today()
        )

        if new_releases.exists():
            return Response(new_releases[0].artists)

        # Check if user is authenticated
        is_authenticated = is_user_authenticated(request.session.session_key)

        # Retrieve to spotify authrorization token
        if is_authenticated:
            token = get_user_token(request.session.session_key)
        else:
            # If not authenticated, redirect to the Spotify authentication url
            return redirect(SPOTIFY_AUTH.get_user())

        # Request the spotify endpoint '/v1/browse/new-releases'
        limit = 50
        offset = 0
        url = SPOTIFY_API_URL + '/v1/browse/new-releases'
        headers = {'Authorization': f'{token.token_type} {token.access_token}'}
        response = get(
            url,
            params={'limit': limit, 'offset': offset},
            headers=headers
        )

        # Check status code
        if response.status_code not in (200, 201):
            raise GetNewReleaseError(
                "Could not retrieve artists from the endpoint "
                f"'/v1/browse/new-releases': {response.text}"
            )

        # Store data in a dictionary
        data = response.json()

        # Loop over the pagination to retrieve all albums
        while response.json()['albums']['next'] is not None:
            offset += limit
            response = get(
                url,
                params={'limit': limit, 'offset': offset},
                headers=headers
            )

            if response.status_code not in [200, 201]:
                raise GetNewReleaseError(
                    "Could not retrieve artists from the endpoint "
                    f"'/v1/browse/new-releases': {response.text}"
                )

            data['albums'].update(response.json()['albums'])

        # Format the the dictionary and store it in DB
        # formatted_data = albums_dict_to_artists_list(data)
        #
        # # Store data in DB
        # new_releases = ArtistsFromNewReleases(artists=formatted_data)
        # new_releases.save()

        return Response(data)
