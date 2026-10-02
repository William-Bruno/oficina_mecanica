from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.error import AppError
from app.core.logging_config import logger

MSG_GENERICA = "Erro interno no servidor"


def _resposta(status_code: int, error: str, detail: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": error, "detail": detail})


async def error_middleware(request: Request, call_next):
    local = f"{request.method} {request.url.path}"
    try:
        return await call_next(request)

    except AppError as erro:
        nome = type(erro).__name__
        if erro.status_code >= 500:
            logger.error(f"{local} - {nome}: {erro.msg}")
            return _resposta(erro.status_code, "ServerError", MSG_GENERICA)
        logger.warning(f"{local} - {nome}: {erro.msg}")
        return _resposta(erro.status_code, nome, erro.msg)

    except SQLAlchemyError:
        logger.exception(f"{local} - Erro de banco de dados")
        return _resposta(500, "ServerError", MSG_GENERICA)

    except Exception:
        logger.exception(f"{local} - Erro inesperado")
        return _resposta(500, "ServerError", MSG_GENERICA)