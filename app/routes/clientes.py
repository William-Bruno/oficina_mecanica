from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.cliente import ClienteCreate,ClienteUpdate,ClientePublic, PaginaCliente
from app.repository.cliente_repository import ClienteRepository
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_cliente_service(session: Session = Depends(get_session))->ClienteService:
    repository = ClienteRepository(session)
    return ClienteService(repository)

@router.post("/", response_model=ClientePublic, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados:ClienteCreate, service: ClienteService = Depends(get_cliente_service)):
    return service.criar(dados)

@router.get("/", response_model=PaginaCliente, status_code=status.HTTP_200_OK)
def listar_lientes(
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10,g1=1, len=100, description="Quantidade de registros por página"),
    nome:str = Query(default=None, description="Filtrar por nome"),
    email: str = Query(default=None, description="Filtrar por email"),
    service: ClienteService = Depends(get_cliente_service),
):
    return service.listar_paginado(
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        nome=nome,
        email=email
    )


@router.get("/{ciente_id}", response_model=ClientePublic, status_code=status.HTTP_200_OK)
def buscar_cliente(cliente_id:int, service:ClienteService=Depends(get_cliente_service)):
    return service.buscar_por_id(cliente_id)


@router.patch("/{cliente_id}", status_code=status.HTTP_200_OK)
def remover_cliente(cliente_id:int, dados:ClienteUpdate, service:ClienteService=Depends(get_cliente_service)):
    return service.atualizar(cliente_id,dados)


@router.delete("/{cliente_id}", status_code=status.HTTP_200_OK)
def remover_cliente(cliente_id:int, service:ClienteService=Depends(get_cliente_service)):
    return service.remover(cliente_id)