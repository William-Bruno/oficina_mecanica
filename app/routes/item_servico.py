from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.item_servico import (
    ItemServicoCreate,
    ItemServicoPublic,
    ItemServicoUpdate,
)
from app.repository.item_servico_repository import ItemServicoRepository
from app.repository.mecanico_repository import MecanicoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.repository.servico_repository import ServicoRepository
from app.repository.veiculo_repository import VeiculoRepository

from app.services.item_servico_service import ItemServicoService
from app.services.ordem_servico_service import OrdemServicoService

router = APIRouter(tags=["Itens de Serviço"])

def get_item_servico_service(session: Annotated[Session, Depends(get_session)]) -> ItemServicoService:
    repo_item_servico = ItemServicoRepository(session)
    repo_ordem_servico = OrdemServicoRepository(session)
    repo_servico = ServicoRepository(session)
    repo_veiculo = VeiculoRepository(session)
    repo_mecanico = MecanicoRepository(session)

    ordem_servico = OrdemServicoService(
        repository=repo_ordem_servico,
        veiculo_repository=repo_veiculo,
        mecanico_repository=repo_mecanico
    )

    return ItemServicoService(
        repository=repo_item_servico,
        ordem_servico_repository=repo_ordem_servico,
        servico_repository=repo_servico,
        ordem_servico_service=ordem_servico
    )

ServiceDepends = Annotated[ItemServicoService, Depends(get_item_servico_service)]

@router.get("/ordens-servico/{ordem_servico_id}/itens-servico", response_model=list[ItemServicoPublic], status_code=status.HTTP_200_OK)
def listar_itens_servico_por_ordem_servico(ordem_servico_id:int, service: ServiceDepends):
    return service.listar_por_ordem_servico_id(ordem_servico_id)

@router.get("/itens-servico/{item_servico_id}", response_model=ItemServicoPublic, status_code=status.HTTP_200_OK)
def buscar_item_servico_por_id(item_servico_id:int, service: ServiceDepends):
    return service.buscar_por_id(item_servico_id)

@router.post("/ordens-servico/{ordem_servico_id}/itens-servico", response_model=ItemServicoPublic, status_code=status.HTTP_201_CREATED)
def adicionar_item_servico(ordem_servico_id:int, dados: ItemServicoCreate, service: ServiceDepends):
    return service.criar(ordem_servico_id, dados)

@router.patch("/itens-servico/{item_servico_id}", response_model=ItemServicoPublic,status_code=status.HTTP_201_CREATED)
def atualizar_item_servico(item_servico_id: int,dados: ItemServicoUpdate,service: ServiceDepends):
    return service.atualizar(item_servico_id, dados)

@router.delete("/itens-servico/{item_servico_id}", status_code=status.HTTP_200_OK)
def remover_item_servico(item_servico_id:int, service:ServiceDepends):
    return service.remover(item_servico_id)