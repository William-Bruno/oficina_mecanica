from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.item_peca import (
    ItemPecaCreate,
    ItemPecaPublic,
    ItemPecaUpdate,
)
from app.repository.item_peca_repository import ItemPecaRepository
from app.repository.mecanico_repository import MecanicoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.repository.peca_repository import PecaRepository
from app.repository.veiculo_repository import VeiculoRepository

from app.services.item_peca_service import ItemPecaService
from app.services.ordem_servico_service import OrdemServicoService

router = APIRouter(tags=["Itens de Peças"])

def get_item_peca_service(session: Annotated[Session, Depends(get_session)]) -> ItemPecaService:
    repo_item_peca = ItemPecaRepository(session)
    repo_ordem_servico = OrdemServicoRepository(session)
    repo_peca = PecaRepository(session)
    repo_veiculo = VeiculoRepository(session)
    repo_mecanico = MecanicoRepository(session)

    ordem_servico = OrdemServicoService(
        repository=repo_ordem_servico,
        veiculo_repository=repo_veiculo,
        mecanico_repository=repo_mecanico
    )

    return ItemPecaService(
        repository=repo_item_peca,
        ordem_servico_repository=repo_ordem_servico,
        peca_repository=repo_peca,
        ordem_servico_service=ordem_servico
    )

ServiceDepends = Annotated[ItemPecaService, Depends(get_item_peca_service)]

@router.get("/ordens-servico/{ordem_servico_id}/itens-peca", response_model=list[ItemPecaPublic], status_code=status.HTTP_200_OK)
def listar_itens_peca_por_ordem_servico(ordem_servico_id:int, service: ServiceDepends):
    return service.listar_por_ordem_servico_id(ordem_servico_id)

@router.get("/itens-peca/{item_peca_id}", response_model=ItemPecaPublic, status_code=status.HTTP_200_OK)
def buscar_item_peca_por_id(item_peca_id:int, service: ServiceDepends):
    return service.buscar_por_id(item_peca_id)

@router.post("/ordens-servico/{ordem_servico_id}/itens-peca", response_model=ItemPecaPublic, status_code=status.HTTP_201_CREATED)
def adicionar_item_peca(ordem_peca_id:int, dados: ItemPecaCreate, service: ServiceDepends):
    return service.criar(ordem_peca_id, dados)

@router.patch("/itens-peca/{item_peca_id}", response_model=ItemPecaPublic,status_code=status.HTTP_201_CREATED)
def atualizar_item_peca(item_peca_id: int,dados: ItemPecaUpdate,service: ServiceDepends):
    return service.atualizar(item_peca_id, dados)

@router.delete("/itens-peca/{item_peca_id}", status_code=status.HTTP_200_OK)
def remover_item_peca(item_peca_id:int, service:ServiceDepends):
    return service.remover(item_peca_id)