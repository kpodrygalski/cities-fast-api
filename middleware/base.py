from typing import Callable
from fastapi import FastAPI, APIRouter, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match


def router_middleware(app: FastAPI, router: APIRouter):
    """Decorator to add a router-specific middleware."""

    def deco(func: Callable) -> Callable:
        async def _middleware(request: Request, call_next: Callable):
            # Check if scopes match
            matches = any(
                [
                    route.matches(request.scope)[0] == Match.FULL
                    for route in router.routes
                ]
            )
            if matches:  # Run the middleware if they do
                return await func(request, call_next)
            else:  # Otherwise skip the middleware
                return await call_next(request)

        app.add_middleware(BaseHTTPMiddleware, dispatch=_middleware)
        return func

    return deco
