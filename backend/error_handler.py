import logging
from functools import wraps
from typing import Callable

from fastapi import HTTPException

logger = logging.getLogger(__name__)


def handle_errors(func: Callable):
    """Decorator to add error handling to endpoints."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise  # Re-raise HTTP exceptions
        except ValueError as e:
            logger.warning(f"Validation error in {func.__name__}: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
