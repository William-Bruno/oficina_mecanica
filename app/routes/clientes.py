from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.cliente import ClienteCreate,ClienteUpdate,ClientePublic, ClientePage
from app.repository.cliente_repository import ClienteRepository
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_cliente_service(session: Session = Depends(get_session))->ClienteService:
    repository = ClienteRepository(session)
    return ClienteService(repository)

ServiceDepends = Annotated[ClienteService, Depends(get_cliente_service)]

@router.post("/", response_model=ClientePublic, status_code=status.HTTP_201_CREATED, summary="Cadastrar um cliente")
def criar_cliente(dados:ClienteCreate, service: ServiceDepends):
    return service.criar(dados)

@router.get("/", response_model=ClientePage, status_code=status.HTTP_200_OK, summary="Listrar todos os clientes")
def listar_clientes(
    service: ServiceDepends,
    pagina: int = Query(default=1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(default=10,g1=1, len=100, description="Quantidade de registros por página"),
    nome:str = Query(default=None, description="Filtrar por nome"),
    email: str = Query(default=None, description="Filtrar por email"),
):
    return service.listar_paginado(
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        nome=nome,
        email=email
    )


@router.get("/{cliente_id}", response_model=ClientePublic, status_code=status.HTTP_200_OK, summary="Buscar cliente pelo ID")
def buscar_cliente(cliente_id:int, service:ServiceDepends):
    return service.buscar_por_id(cliente_id)


@router.patch("/{cliente_id}", status_code=status.HTTP_201_CREATED, summary="Atualizar dados do cliente")
def atualizar_cliente(cliente_id:int, dados:ClienteUpdate, service:ServiceDepends):
    return service.atualizar(cliente_id,dados)


@router.delete("/{cliente_id}", status_code=status.HTTP_200_OK, summary="Remover um cliente")
def remover_cliente(cliente_id:int, service:ServiceDepends):
    return service.remover(cliente_id)