from typing import TYPE_CHECKING
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import field_serializer

from sqlmodel import Field, SQLModel, Relationship

from app.models.enums import FormaPagamento

if TYPE_CHECKING:
    from app.models.ordem_servico import OrdemServico

class PagamentoBase(SQLModel):
    valor: Decimal = Field(default=Decimal("0.00"), gt=0, nullable=False)
    forma_pagamento: FormaPagamento = Field(default=FormaPagamento.DINHEIRO, nullable=False)
    ordem_servico_id: int = Field(foreign_key="ordemservico.id", nullable=False)

class Pagamento(PagamentoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},)
    ordem_servico: "OrdemServico" = Relationship(back_populates="pagamentos")

class PagamentoCreate(SQLModel):
    valor: Decimal = Field(gt=0)
    forma_pagamento: FormaPagamento = Field(default=FormaPagamento.DINHEIRO)

class PagamentoUpdate(SQLModel):
    valor: Decimal |None =None
    forma_pagamento: FormaPagamento | None = None

class PagamentoPublic(PagamentoBase):
    id: int
    data: datetime
    created_at: datetime 
    updated_at: datetime

    @field_serializer("valor")
    def formatar_valor(self, valor:Decimal)->Decimal:
        return valor.quantize(Decimal("0.01"))
