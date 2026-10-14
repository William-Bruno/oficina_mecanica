from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime, timezone
from pydantic import field_serializer

from sqlmodel import SQLModel, Field, Relationship

from app.models.paginacao import Paginacao

if TYPE_CHECKING:
    from app.models.servico import Servico
    from app.models.ordem_servico import OrdemServico

class ItemServicoBase(SQLModel):
    tempo_hora: int = Field(default=1, gt=0)
    valor_hora: Decimal = Field(default=Decimal("0.00"), ge=0)
    aprovado: bool = Field(default=True, nullable=False)
    servico_id: int = Field(foreign_key="servico.id", nullable=False)
    ordem_servico_id: int = Field(foreign_key="ordemservico.id", nullable=False)

class ItemServico(ItemServicoBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},)
    servico: "Servico" = Relationship(back_populates="itens_servicos")
    ordem_servico: "OrdemServico" = Relationship(back_populates="itens_servicos")


class ItemServicoCreate(SQLModel):
    servico_id: int
    tempo_hora: int = Field(default=1, gt=0)
    valor_hora: Decimal = Field(default=Decimal("0.00"), ge=0)
    aprovado: bool = Field(default=True)

class ItemServicoUpdate(SQLModel):
    tempo_hora: int | None = None
    valor_hora: Decimal | None = None
    aprovado: bool | None = None
    servico_id: int | None = None

class ItemServicoPublic(ItemServicoBase):
    id: int
    created_at: datetime 
    updated_at: datetime

    @field_serializer("valor_hora")
    def formatar_valor_hora(self, valor:Decimal)->Decimal:
        return valor.quantize(Decimal("0.01"))

class ItemServicoPage(SQLModel):
    dados:list[ItemServicoPublic]
    paginacao: Paginacao