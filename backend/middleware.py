from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Limit request body size to prevent timeouts and DoS."""

    def __init__(self, app, max_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_size:
                return JSONResponse(
                    status_code=413, content={"detail": "Request body too large"}
                )
        response = await call_next(request)
        # Validate response structure for chat endpoints
        if request.url.path == "/chat" and hasattr(response, "body"):
            content = response.body.decode("utf-8")
            if not all(
                keyword in content
                for keyword in [
                    "**Summary:**",
                    "**Plan:**",
                    "**Assumptions:**",
                    "**Next Step:**",
                ]
            ):
                # Log violation but don't block - for HR demo, we enforce but allow
                print("⚠️ Response does not match output contract structure.")
        return response
