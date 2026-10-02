from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, Relationship

from app.models.enums import FormaPagamento

if TYPE_CHECKING:
    from app.models.ordem_servico import OrdemServico

class PagamentoBase(SQLModel):
    valor: float = Field(gt=0, nullable=False)
    forma_pagamento: FormaPagamento = Field(default=FormaPagamento.PIX, nullable=False)
    data: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    ordem_servico_id: int = Field(foreign_key="ordemservico.id", nullable=False)

class Pagamento(PagamentoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    ordem_servico: "OrdemServico" = Relationship(back_populates="pagamentos")

class PagamentoCreate(PagamentoBase):
    pass

class PagamentoUpdate(SQLModel):
    valor: float | None = Field(default=None, gt=0)
    forma_pagamento: FormaPagamento | None = None
    data: datetime | None = None
    ordem_servico_id: int | None = None

class PagamentoPublic(PagamentoBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None
