import traceback

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from infrastructure.config.logs import log

logger = log.getChild(__name__)


async def main_exception_handler(req: Request, exc: Exception) -> JSONResponse:
    tb_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logger.error("Unhandled Exception:\n%s", tb_str)
    return JSONResponse(
        status_code=get_status_code(exc),
        content={"error": get_message(exc)}
    )


def get_message(exc) -> str:
    if isinstance(exc, RequestValidationError):
        return "\n".join([_.get("msg") for _ in exc.errors()])
    return str(exc)


def get_status_code(exc: Exception) -> int:
    if isinstance(exc, RequestValidationError):
        return 422
    return exc.status_code if hasattr(exc, "status_code") else 500
