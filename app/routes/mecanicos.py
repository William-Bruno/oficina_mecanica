from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.mecanico import MecanicoCreate,MecanicoUpdate, MecanicoPublic, MecanicoPage
from app.repository.mecanico_repository import MecanicoRepository
from app.services.mecanico_service import MecanicoService

router = APIRouter(prefix="/mecanicos", tags=["Mecanicos"])

def get_mecanico_service(session: Session = Depends(get_session)) -> MecanicoService:
    repository = MecanicoRepository(session)
    return MecanicoService(repository)

@router.post("/", response_model=MecanicoPublic, status_code=status.HTTP_201_CREATED, summary="Cadastrar um mecanicos")
def criar_mecanico(dados: MecanicoCreate, service: MecanicoService = Depends(get_mecanico_service)):
    return service.criar(dados)

@router.get("/", response_model=MecanicoPage, status_code=status.HTTP_200_OK, summary="Listar todos os mecanicos")
def listar_mecanicos(
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10,g1=1, len=100, description="Quantidade de registros por página"),
    nome:str = Query(default=None, description="Filtrar por nome"),
    especialidade: str = Query(default=None, description="Filtrar por especialidade"),
    service: MecanicoService = Depends(get_mecanico_service),
):
    return service.listar_paginado(
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        nome=nome,
        especialidade=especialidade
    )


@router.get("/{mecanico_id}", response_model=MecanicoPublic, status_code=status.HTTP_200_OK, summary="Bscar mecanico pelo ID")
def buscar_mecanico(mecanico_id:int, service:MecanicoService=Depends(get_mecanico_service)):
    return service.buscar_por_id(mecanico_id)


@router.patch("/{mecanico_id}", status_code=status.HTTP_201_CREATED, summary="Atualizar dados do Mecanico")
def atualizar_mecanico(mecanico_id:int, dados:MecanicoUpdate, service:MecanicoService=Depends(get_mecanico_service)):
    return service.atualizar(mecanico_id,dados)


@router.delete("/{mecanico_id}", status_code=status.HTTP_200_OK, summary="Remover um Mecanico")
def remover_mecanico(mecanico_id:int, service:MecanicoService=Depends(get_mecanico_service)):
    return service.remover(mecanico_id)