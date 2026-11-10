
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.relatorio import RelatorioInadimplencia
from app.repository.relatorios_repository import RelatorioRepository
from app.services.relatorio_service import RelatorioService


router = APIRouter(prefix="/relatorios", tags=["Relatórios e Consultas Complexas"])

def get_relatorio_repository(session: Session = Depends(get_session)) -> RelatorioRepository:
    return RelatorioRepository(session)

def get_relatorio_sevice(repository: RelatorioRepository = Depends(get_relatorio_repository)) ->RelatorioService:
    return RelatorioService(repository)

RelatorioServiceDepends = Annotated[RelatorioService, Depends(get_relatorio_sevice)]

@router.get("/inadimplencia", response_model=list[RelatorioInadimplencia], status_code=status.HTTP_200_OK)
def relatorio_inadimplencia(service: RelatorioServiceDepends):
    """Retorna as ordens de serviço concluídas que possuem saldo devedor """
    return service.relatorio_inadimplencia()