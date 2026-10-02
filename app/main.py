from fastapi import FastAPI
from app.core.logging_config import logger
from app.core.logging_middleware import logging_middleware
from app.core.error_middleware import error_middleware

app = FastAPI(
    title="API de Oficina Mecanica",
    description="API de gestão de Oficina Mecanica",
    version="1.0.0"
)

app.middleware("http")(error_middleware)    
app.middleware("http")(logging_middleware)  


logger.info("API iniciada!")