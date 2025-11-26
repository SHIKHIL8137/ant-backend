from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.logger import logger


def register_exception_handlers(app):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP Error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": False, "message": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation Error: {exc}")
        return JSONResponse(
            status_code=422,
            content={"status": False, "message": "Invalid input", "errors": exc.errors()}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error"}
        )
