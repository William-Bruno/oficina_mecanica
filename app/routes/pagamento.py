from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, status

from app.core.database import get_session
from app.models.pagamento import PagamentoCreate, PagamentoPublic
from app.services.pagamento_service import PagamentoService
from app.repository.pagamento_repository import PagamentoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository


def get_pagamento_service(session: Session = Depends(get_session)) -> PagamentoService:
    repository = PagamentoRepository(session)
    ordem_servico_repository = OrdemServicoRepository(session)
    return PagamentoService(repository, ordem_servico_repository)


router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

PagamentoServiceDepends = Annotated[PagamentoService, Depends(get_pagamento_service)]

@router.post("/{ordem_servico_id}", response_model=PagamentoPublic, status_code=status.HTTP_201_CREATED)
def registrar_pagamento(ordem_servico_id:int, dados: PagamentoCreate, service: PagamentoServiceDepends):
    return service.registrar_pagamento(ordem_servico_id, dados)