"""Server script."""

import os
import warnings

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from httpx import RequestError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from github import Endpoint


DEFAULT_RATE = "60/hour"

# Heroku sets the config vars as environment variables.
endpoint = Endpoint(
    "GET", "/repos/{}/{}/releases/latest", api_token=os.getenv("API_TOKEN")
)

if endpoint.api_token_is_set:
    DEFAULT_RATE = "80/minute"

app = FastAPI()

# Adds rate limiting support.
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# `request` needs to be an argument for `slowapi` to work.
@app.get("/")
@limiter.limit(DEFAULT_RATE)
async def root(request: Request, owner: str, repo: str):
    try:
        response = await endpoint.request(owner, repo)
    except RequestError as exc:
        warnings.warn(exc.__doc__ or "Request failed") # Fallback message.
    else:
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )

# Properly close on shutdown.
@app.on_event("shutdown")
async def shutdown_handler():
    await endpoint.close()