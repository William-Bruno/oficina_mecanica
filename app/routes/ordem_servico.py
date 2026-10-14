from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.enums import StatusOrdemServico
from app.models.ordem_servico import (
    OrdemServicoCreate,
    OrdemServicoUpdate,
    OrdemServicoPage,
    OrdemServicoPublic,
    OrdemServicoPublicDetalhada
)

from app.repository.mecanico_repository import MecanicoRepository
from app.repository.veiculo_repository import VeiculoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.services.ordem_servico_service import OrdemServicoService

router = APIRouter(prefix="/ordens-servico", tags=["Ordens de Serviço"])

def get_ordem_servico_service(session: Annotated[Session, Depends(get_session)]) -> OrdemServicoService:
    repo_veiculo = VeiculoRepository(session)
    repo_mecanico = MecanicoRepository(session)
    repo_ordem_servico = OrdemServicoRepository(session)
    return OrdemServicoService(
        repository=repo_ordem_servico, veiculo_repository=repo_veiculo, mecanico_repository=repo_mecanico
    )

#Type alias
ServiceDepends = Annotated[OrdemServicoService, Depends(get_ordem_servico_service)]

@router.get("", response_model=OrdemServicoPage, status_code=status.HTTP_200_OK)
def listar_ordens_servico(
    service: ServiceDepends,
    p: int = Query(default=1, ge=1, description="Número da página"),
    tp: int = Query(default=10, ge=1, le=100, description="Tamanho da página"),
    status: StatusOrdemServico | None = Query(default=None, description="Filtro por status"),
    veiculo_id: int | None = Query(default=None, description="Filtro por ID do veículo"),
    mecanico_id: int | None = Query(default=None, description="Filtro por ID do mecânico"),
    data_inicio: datetime | None = Query(default=None, description="Data inicial de abertura"),
    data_fim: datetime | None = Query(default=None, description="Data final de abertura"),
):
    """Lista Ordens de Serviço paginadas com suporte a múltiplos filtros."""
    return service.listar_paginado(
        p=p,
        tp=tp,
        status=status,
        veiculo_id=veiculo_id,
        mecanico_id=mecanico_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

@router.get("/{ordem_servico_id}",response_model=OrdemServicoPublicDetalhada,status_code=status.HTTP_200_OK,)
def buscar_ordem_servico_por_id(ordem_servico_id: int, service: ServiceDepends):
    """Busca os detalhes completos de uma Ordem de Serviço (Visão 360°)."""
    return service.buscar_por_id(ordem_servico_id)

@router.post("", response_model=OrdemServicoPublic, status_code=status.HTTP_201_CREATED)
def criar_ordem_servico(dados: OrdemServicoCreate, service: ServiceDepends):
    """Abre/Agenda uma nova Ordem de Serviço."""
    return service.criar(dados)


@router.patch("/{ordem_servico_id}",response_model=OrdemServicoPublic,status_code=status.HTTP_200_OK,)
def atualizar_ordem_servico(ordem_servico_id: int, dados: OrdemServicoUpdate, service: ServiceDepends):
    """Atualiza parcialmente os dados ou o status de uma Ordem de Serviço."""
    return service.atualizar(ordem_servico_id, dados)


@router.delete("/{ordem_servico_id}", status_code=status.HTTP_200_OK)
def remover_ordem_servico(ordem_servico_id: int, service: ServiceDepends):
    """Remove uma Ordem de Serviço (caso não possua relacionamentos ativos)."""
    return service.remover(ordem_servico_id)