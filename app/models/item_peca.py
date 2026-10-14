from typing import TYPE_CHECKING
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import field_serializer

from sqlmodel import SQLModel, Field, Relationship

from app.models.paginacao import Paginacao

if TYPE_CHECKING:
    from app.models.peca import Peca
    from app.models.ordem_servico import OrdemServico

class ItemPecaBase(SQLModel):
    quantidade: int = Field(default=1, gt=0)
    preco_unitario: Decimal = Field(default=Decimal("0.00"), ge=0)
    aprovado: bool = Field(default=True, nullable=False)
    peca_id: int = Field(foreign_key="peca.id", nullable=False)
    ordem_servico_id: int = Field(foreign_key="ordemservico.id", nullable=False)

class ItemPeca(ItemPecaBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},)
    peca: "Peca" = Relationship(back_populates="itens_pecas")
    ordem_servico: "OrdemServico" = Relationship(back_populates="itens_pecas")


class ItemPecaCreate(SQLModel):
    peca_id: int
    quantidade: int = Field(default=1, gt=0)
    preco_unitario: Decimal = Field(default=Decimal("0.00"), ge=0)
    aprovado: bool = Field(default=True)

class ItemPecaUpdate(SQLModel):
    quantidade: int | None = None
    preco_unitario: Decimal | None = None
    aprovado: bool | None = None
    peca_id: int | None = None

class ItemPecaPublic(ItemPecaBase):
    id: int
    created_at: datetime 
    updated_at: datetime
    
    @field_serializer("preco_unitario")
    def formatar_valor_hora(self, valor:Decimal)->Decimal:
        return valor.quantize(Decimal("0.01"))

class ItemPecaPage(SQLModel):
    dados: list[ItemPecaPublic]
    paginacao: Paginacao