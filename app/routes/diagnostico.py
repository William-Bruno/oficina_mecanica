from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.diagnostico import DiagnosticoCreate, DiagnosticoPublic, DiagnosticoUpdate
from app.repository.diagnostico_repository import DiagnosticoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.services.diagnostico_service import DiagnosticoService


router = APIRouter(tags=["Diagnósticos"])

def get_diagnostico_service(session: Session = Depends(get_session)) -> DiagnosticoService:
    repository = DiagnosticoRepository(session)
    ordem_servico_repository = OrdemServicoRepository(session)
    return DiagnosticoService(repository, ordem_servico_repository)

# Chamada de dependencias de sessão
DiagnosticoServiceDepends = Annotated[DiagnosticoService, Depends(get_diagnostico_service)]

@router.post("/ordens-servico/{ordem_servico_id}/diagnostico", response_model=DiagnosticoPublic, status_code=status.HTTP_201_CREATED)
def criar_diagnostico(ordem_servico_id: int, dados: DiagnosticoCreate, service: DiagnosticoServiceDepends):
    return service.criar(ordem_servico_id, dados)

@router.get("/ordens-servico/{ordem_servico_id}/diagnostico",response_model=DiagnosticoPublic)
def buscar_diagnostico_ordem_servico(ordem_servico_id:int, service: DiagnosticoServiceDepends):
    return service.buscar_por_ordem_servico_id(ordem_servico_id)

@router.patch("/diagnosticos/{diagnostico_id}", response_model=DiagnosticoPublic)
def atualizar_diagnostico(diagnostico_id: int, dados:DiagnosticoUpdate, service:DiagnosticoServiceDepends):
    return service.atualizar(diagnostico_id, dados)

@router.delete("/diagnosticos/{diagnostico_id}", status_code=status.HTTP_200_OK)
def remover_diagnostico(diagnostio_id: int, service: DiagnosticoServiceDepends):
    return service.remover(diagnostio_id)





