import os

# ROOT URL for the GitHub API.
ROOT = "https://api.github.com/"

# API token for GitHub.
API_TOKEN = os.getenv("API_TOKEN")

# HTTP Methods supported by `httpx`.
METHODS = ("GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE")
