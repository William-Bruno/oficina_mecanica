from typing import TYPE_CHECKING
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import field_serializer

from sqlmodel import Field, SQLModel, Relationship
from app.models.paginacao import Paginacao

if TYPE_CHECKING:
    from app.models.item_servico import ItemServico

class ServicoBase(SQLModel):
    descricao: str = Field(min_length=3, max_length=250, index=True)
    preco: Decimal = Field(default=Decimal("0.00"), gt=0, max_digits=10, decimal_places=2, nullable=False)
    ativo: bool = Field(default=True)

class Servico(ServicoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},)
    itens_servicos: list["ItemServico"] = Relationship(back_populates="servico")

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(SQLModel):
    descricao: str | None = None
    preco: Decimal = Field(default=Decimal("0.00"), gt=0, max_digits=10, decimal_places=2)
    ativo: bool | None = None

class ServicoPublic(ServicoBase):
    id: int
    created_at: datetime 
    updated_at: datetime

    @field_serializer("preco")
    def formatar_valor(self, valor:Decimal)->Decimal:
        return valor.quantize(Decimal("0.01"))

class ServicoPage(SQLModel):
    dados: list[ServicoPublic]
    paginacao: Paginacao

