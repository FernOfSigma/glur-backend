"""A tiny module for calling the GitHub REST API."""

import warnings

from httpx_cache import AsyncClient


__all__ = ["Endpoint"]

ROOT = "https://api.github.com/"

# HTTP Methods supported by `httpx`.
METHODS = (
    "GET",
    "OPTIONS", 
    "HEAD",
    "POST",
    "PUT",
    "PATCH",
    "DELETE"
)


class InvalidMethod(Exception):

    def __init__(self, method, *args):
        super().__init__(*args)
        self.method = method

    def __str__(self):
        # Wrap every method name in single quotes.
        method_list = [f"'{method}'" for method in METHODS]
        return (
            f"Invalid HTTP method: '{self.method}': "
            f"Must be one of {', '.join(method_list)}"
        )


class Endpoint:
    """Represents a GitHub API endpoint for ease of use."""

    def __init__(self, method, endpoint, api_token=None):
        headers = {
            # Set default cache expiration time to 1h.
            "Cache-Control": "max-age=3600",
            "User-Agent": "gru/0.0.1"
        }
        # Add the API token to `headers`.
        if api_token is not None:
            headers["Authorization"] = f"Bearer {api_token}"
        else:
            warnings.warn("Setting a GitHub API token is recommended")
        # Create `AsyncClient` instance to reuse the connection.
        self._client = AsyncClient(headers=headers)
        
        if method not in METHODS:
            raise InvalidMethod(method)
        else:
            self._method = method

        # Remove leading "/" to ensure correct URL building.
        self._endpoint = endpoint.lstrip("/")

    @property
    def api_token_is_set(self):
        """Indicates if the a GitHub API token has been set."""
        return self._client.headers.get("Authorization") is None

    async def request(self, *args, **kwargs):
        """Sends a request to the GitHub API endpoint."""
        url = ROOT + self._endpoint.format(*args)
        return await self._client.request(self._method, url, **kwargs)

    async def close(self):
        """Close the underlying `AsyncClient` instance."""
        await self._client.aclose()
