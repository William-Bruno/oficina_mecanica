from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.servico import ServicoCreate,ServicoUpdate,ServicoPublic,ServicoPage
from app.repository.servico_repository import ServicoRepository
from app.services.servico_service import ServicoService

router = APIRouter(prefix="/servicos", tags=["Serviços"])

def get_servico_service(session: Session = Depends(get_session)) -> ServicoService:
    repository = ServicoRepository(session)
    return ServicoService(repository)

ServiceDepends = Annotated[ServicoService, Depends(get_servico_service)]

@router.post("/", response_model=ServicoPublic, status_code=status.HTTP_201_CREATED, summary="Cadastrar um serviço")
def criar_servico(dados: ServicoCreate, service: ServiceDepends):
    return service.criar(dados)

@router.get("/", response_model=ServicoPage, status_code=status.HTTP_200_OK, summary="Listar todos os serviços cadastrados")
def listar_servicos(
    service: ServiceDepends,
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10,g1=1, len=100, description="Quantidade de registros por página"),
    descricao:str = Query(default=None, description="Filtrar pela descricao"),
):
    return service.listar_paginado(
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        descricao=descricao
    )


@router.get("/{servico_id}", response_model=ServicoPublic, status_code=status.HTTP_200_OK, summary="Bscar serviço pelo ID")
def buscar_servico(servico_id:int, service:ServiceDepends):
    return service.buscar_por_id(servico_id)


@router.patch("/{servico_id}", status_code=status.HTTP_201_CREATED, summary="Atualizar dados de um serviço")
def atualizar_servico(servico_id:int, dados:ServicoUpdate, service:ServiceDepends):
    return service.atualizar(servico_id,dados)


@router.delete("/{servico_id}", status_code=status.HTTP_200_OK, summary="Remover um serviço")
def remover_servico(servico_id:int, service:ServiceDepends):
    return service.remover(servico_id)
    