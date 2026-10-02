from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.peca import Peca
    from app.models.ordem_servico import OrdemServico

class ItemPecaBase(SQLModel):
    quantidade: int = Field(default=1, gt=0)
    preco_unitario: float = Field(default=0.0, ge=0)
    aprovado: bool = Field(default=True, nullable=False)
    peca_id: int = Field(foreign_key="peca.id", nullable=False)
    ordem_servico_id: int = Field(foreign_key="ordemservico.id", nullable=False)

class ItemPeca(ItemPecaBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    peca: "Peca" = Relationship(back_populates="itens_pecas")
    ordem_servico: "OrdemServico" = Relationship(back_populates="itens_pecas")


class ItemPecaCreate(ItemPecaBase):
    pass

class ItemPecaUpdate(SQLModel):
    quantidade: int | None = None
    preco_unitario: float | None = None
    aprovado: bool | None = None
    peca_id: int | None = None
    ordem_servico_id: int | None = None

class ItemPecaPublic(ItemPecaBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None