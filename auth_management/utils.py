from datetime import timedelta
from django.utils import timezone
from .models import SpotifyToken


SPOTIFY_AUTH = SpotifyToken()


def get_user_token(session_id):
    """Return the user's token if it exists or return None."""
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_token(session_id, access_token, refresh_token,
                                expires_in, token_type):
    """Update or create user's token given a session_id."""
    token = get_user_token(session_id)

    # Define the expires_in date from now
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if token:
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_in = expires_in
        token.token_type = token_type
        token.save()
    else:
        SpotifyToken.objects.create(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type
        )


def is_user_authenticated(session_id):
    """
    Return True if the user is authenticated. Return False otherwise.

    If the access token is expired, also refreshes it.
    """
    token = get_user_token(session_id)
    if token:
        if token.expires_in < timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False


def refresh_spotify_token(session_id):
    """Refresh the access token from the refresh token of the user."""
    token = get_user_token(session_id)
    response = SPOTIFY_AUTH.refresh_auth(token.refresh_token)

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    # The response should not return a refresh token. Use the existing one.
    refresh_token = response.get('refresh_token', token.refresh_token)

    update_or_create_user_token(
        session_id,
        access_token,
        token_type,
        expires_in,
        refresh_token
    )
