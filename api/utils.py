from requests import get

from .models import NewReleases, Artist


def merge_get_artists_requests(url, token_type, access_token, limit, offset):
    """
    Return the list of items in the endpoint to retrieve new releases.

    Loop over the pagination to merge all items.
    """
    data = []
    next = ""
    while next is not None:
        response = get(
            url,
            params={'limit': limit, 'offset': offset},
            headers={'Authorization': f'{token_type} {access_token}'}
        )

        # Check status code
        if response.status_code not in [200, 201, 202, 203, 204]:
            raise GetNewReleasesError(
                "Could not retrieve albums: "
                f"[{response.status_code}] {response.text}"
            )

        data += response.json()['albums']['items']
        next = response.json()['albums']['next']
        offset += limit

    return data


def assign_artists_to_new_releases(items):
    """
    Instanciate a Newrelease object and assign artists to it.

    If the Artist object does not exist, create it before assigning it.
    """
    new_releases = NewReleases.objects.create()

    for item in items:
        for artist in item['artists']:
            id = artist['id']
            try:
                new_releases.artists.add(Artist.objects.get(pk=id))
            except Artist.DoesNotExist:
                artist = Artist.objects.create(
                    id=id,
                    name=artist['name'],
                    type=artist['type'],
                    uri=artist['uri'],
                    api_href=artist['href'],
                    spotify_link=artist['external_urls']['spotify'],
                )
                new_releases.artists.add(artist)

    return new_releases
