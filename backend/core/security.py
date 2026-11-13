from fastapi import Depends, Header, HTTPException, status

from .config import settings


def api_key_guard(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    if not settings.API_KEY or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
