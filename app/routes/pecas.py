from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.peca import PecaCreate,PecaUpdate,PecaPublic,PecaPage
from app.repository.peca_repository import PecaRepository
from app.services.peca_service import PecaService

router = APIRouter(prefix="/pecas", tags=["Peças"])

def get_peca_service(session: Session = Depends(get_session)) -> PecaService:
    repository = PecaRepository(session)
    return PecaService(repository)


ServiceDepends = Annotated[PecaService, Depends(get_peca_service)]

@router.post("/", response_model=PecaPublic, status_code=status.HTTP_201_CREATED, summary="Cadastrar uma peça")
def criar_peca(dados: PecaCreate, service: ServiceDepends):
    return service.criar(dados)

@router.get("/", response_model=PecaPage, status_code=status.HTTP_200_OK, summary="Listar todas as peças cadastradas")
def listar_pecas(
    service: ServiceDepends,
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10,g1=1, len=100, description="Quantidade de registros por página"),
    nome:str = Query(default=None, description="Filtrar pelo nome"),
):
    return service.listar_paginado(
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        nome=nome
    )


@router.get("/{peca_id}", response_model=PecaPublic, status_code=status.HTTP_200_OK, summary="Buscar peça pelo ID")
def buscar_peca(peca_id:int, service:ServiceDepends):
    return service.buscar_por_id(peca_id)


@router.patch("/{peca_id}", status_code=status.HTTP_201_CREATED, summary="Atualizar dados de uma peça")
def atualizar_peca(peca_id:int, dados:PecaUpdate, service:ServiceDepends):
    return service.atualizar(peca_id,dados)


@router.delete("/{peca_id}", status_code=status.HTTP_200_OK, summary="Remover uma peça")
def remover_peca(peca_id:int, service:ServiceDepends):
    return service.remover(peca_id)
    