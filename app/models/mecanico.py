from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, Relationship

from app.models.diagnostico import Diagnostico
from app.models.enums import EspecialidadeMecanico
from app.models.paginacao import Paginacao

if TYPE_CHECKING:
    from app.models.ordem_servico import OrdemServico
    from app.models.item_servico import ItemServico

class MecanicoBase(SQLModel):
    nome: str = Field(min_length=3, max_length=150, index=True)
    especialidade: EspecialidadeMecanico = Field(
        default=EspecialidadeMecanico.MECANICA_GERAL, 
        nullable=False
    )
    ativo: bool = Field(default=True)

class Mecanico(MecanicoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    itens_servicos: list["ItemServico"] = Relationship(back_populates="mecanico")
    diagnosticos: list["Diagnostico"] = Relationship(back_populates="mecanico")

class MecanicoCreate(MecanicoBase):
    pass

class MecanicoUpdate(SQLModel):
    nome: str | None = None
    especialidade: EspecialidadeMecanico | None = None
    ativo: bool | None = None

class MecanicoPublic(MecanicoBase):
    id: int
    created_at: datetime 
    updated_at: datetime

class MecanicoPage(SQLModel):
    dados: list[MecanicoPublic]
    paginacao: Paginacao
