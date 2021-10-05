import base64
import json
import requests
import os

from .exceptions import RefreshTokenError, PostRefreshError, GetTokenError


class SpotifyAuth(object):
    SPOTIFY_URL_AUTH = "https://accounts.spotify.com/authorize/"
    SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token/"
    RESPONSE_TYPE = "code"
    HEADER = "application/x-www-form-urlencoded"
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CALLBACK_URL = "http://localhost:5000/auth"
    SCOPE = "user-read-email user-read-private"

    def get_auth_url(self, client_id, redirect_uri, scope):
        return (
            f"{self.SPOTIFY_URL_AUTH}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
            "&response_type=code"
        )

    def get_token(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        encoded = base64.b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode()
        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        }

        post = requests.post(
            self.SPOTIFY_URL_TOKEN,
            params=body,
            headers=headers
        )

        if post.status_code not in (200, 201):
            raise GetTokenError(
                "Could not retrieve token from endpoint "
                f"{self.SPOTIFY_URL_TOKEN} with code: {code}"
            )
        return self.handle_token(json.loads(post.text))

    def handle_token(self, response):
        if "error" in response:
            raise RefreshTokenError(
                "An error occured in the refreshment of the access token"
                f": {response['error']}"
            )
        return response

    def refresh_auth(self, refresh_token):
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        post_refresh = requests.post(
            self.SPOTIFY_URL_TOKEN, data=body, headers=self.HEADER
        )

        if post_refresh.status_code not in (200, 201):
            raise PostRefreshError(
                f"Post for token refreshment went wrong: {post_refresh.text}"
            )
        p_back = json.dumps(post_refresh.text)

        return self.handleToken(p_back)

    def get_user(self):
        return self.get_auth_url(
            self.CLIENT_ID,
            f"{self.CALLBACK_URL}/callback",
            self.SCOPE
        )

    def get_user_token(self, code):
        return self.get_token(
            code, self.CLIENT_ID,
            self.CLIENT_SECRET,
            f"{self.CALLBACK_URL}/callback"
        )
