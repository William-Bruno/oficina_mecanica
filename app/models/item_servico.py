from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.servico import Servico
    from app.models.ordem_servico import OrdemServico

class ItemServicoBase(SQLModel):
    tempo_hora: int = Field(default=1, gt=0)
    valor_hora: float = Field(default=0.0, ge=0)
    servico_id: int = Field(foreign_key="servico.id", nullable=False)
    ordem_servico_id: int = Field(foreign_key="ordemservico.id", nullable=False)

class ItemServico(ItemServicoBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    servico: "Servico" = Relationship(back_populates="itens_servicos")
    ordem_servico: "OrdemServico" = Relationship(back_populates="itens_servicos")


class ItemServicoCreate(ItemServicoBase):
    pass

class ItemServicoUpdate(SQLModel):
    tempo_hora: int | None = None
    valor_hora: float | None = None
    servico_id: int | None = None
    ordem_servico_id: int | None = None

class ItemServicoPublic(ItemServicoBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None