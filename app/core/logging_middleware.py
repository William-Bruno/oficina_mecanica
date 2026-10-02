from fastapi import Request
from app.core.logging_config import logger


async def logging_middleware(request: Request, call_next):
    response = await call_next(request)
    mensagem = f"{request.method} {request.url.path} status={response.status_code}"

    if response.status_code >= 500:
        logger.error(mensagem)
    elif response.status_code >= 400:
        logger.warning(mensagem)
    else:
        logger.info(mensagem)

    return response