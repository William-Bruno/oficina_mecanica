from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.veiculo import (
    VeiculoCreate,
    VeiculoUpdate,
    VeiculoPage,
    VeiculoPublic,
    VeiculoClientePublic
)

from app.repository.cliente_repository import ClienteRepository
from app.repository.veiculo_repository import VeiculoRepository
from app.services.veiculo_service import VeiculoService

router = APIRouter(prefix="/veiculos", tags=["Veículos"])

def get_veiculo_service(session: Annotated[Session, Depends(get_session)]) -> VeiculoService:
    repo_veiculo = VeiculoRepository(session)
    repo_cliente = ClienteRepository(session)
    return VeiculoService(repository=repo_veiculo, cliente_repository=repo_cliente)

#Type alias
ServiceDepends = Annotated[VeiculoService, Depends(get_veiculo_service)]

@router.post("", response_model=VeiculoPublic, status_code=status.HTTP_201_CREATED)
def criar_veiculo(dados: VeiculoCreate, service: ServiceDepends):
    return service.criar(dados)

@router.get("/", response_model=VeiculoPage, status_code=status.HTTP_200_OK)
def listar_veiculos(
    service: ServiceDepends,
    p:int = Query(default=1, ge=1, description="Número da página"),
    tp:int = Query(default=10, ge=1, le=100, description="Tamanho da página"),
    placa:str | None = Query(default=None, description="Filtro por placa"),
    cliente_id:int | None =Query(default=None, description="Filtro por ID do cliente")
):
    return service.listar_paginado(p=p,tp=tp, placa=placa, cliente_id=cliente_id)

@router.get("/{veiculo_id}", response_model=VeiculoClientePublic, status_code=status.HTTP_200_OK)
def buscar_veiculo_por_id(veiculo_id: int, service:ServiceDepends):
    return service.buscar_por_id(veiculo_id)

@router.patch("/{veiculo_id}", response_model=VeiculoPublic, status_code=status.HTTP_201_CREATED)
def atualizar_veiculo(veiculo_id: int, dados: VeiculoUpdate, service: ServiceDepends):
    return service.atualizar(veiculo_id, dados)

@router.delete("/{veiculo_id}", status_code=status.HTTP_200_OK)
def remover_veiculo(veiculo_id:int, service: ServiceDepends):
    return service.remover(veiculo_id)

