from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, Relationship

from app.models.enums import EspecialidadeMecanico

if TYPE_CHECKING:
    from app.models.ordem_servico import OrdemServico

class MecanicoBase(SQLModel):
    nome: str = Field(min_length=3, max_length=150, index=True)
    especialidade: EspecialidadeMecanico = Field(default=EspecialidadeMecanico.MECANICA_GERAL, nullable=False)


class Mecanico(MecanicoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    ordens_servico: list["OrdemServico"] = Relationship(back_populates="mecanico")

class MecanicoCreate(MecanicoBase):
    pass

class MecanicoUpdate(SQLModel):
    nome: str | None = None
    especialidade: EspecialidadeMecanico | None = None

class MecanicoPublic(MecanicoBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None
