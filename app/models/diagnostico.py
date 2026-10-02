from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship

from app.models.enums import NivelCombustivel

if TYPE_CHECKING:
    from app.models.ordem_servico import OrdemServico

class DiagnosticoBase(SQLModel):
    analise_mecanico: str = Field(min_length=3, max_length=150, nullable=False)
    quilometragem: int = Field(ge=0, default=0, nullable=False)
    avarias_latarias: str = Field(min_length=3, max_length=150, nullable=False)
    nivel_combustivel: NivelCombustivel = Field(default=NivelCombustivel.MEDIO, nullable=False)
    ordem_servico_id: int = Field(foreign_key="ordemservico.id", unique=True, nullable=False)

class Diagnostico(DiagnosticoBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    ordem_servico: "OrdemServico" = Relationship(back_populates="diagnostico")

class DiagnosticoCreate(DiagnosticoBase):
    pass

class DiagnosticoUpdate(SQLModel):
    analise_mecanico: str |None = None
    quilometragem: int |None = None
    avarias_latarias: str |None = None
    nivel_combustivel: NivelCombustivel |None = None
    ordem_servico_id: int |None = None

class DiagnosticoPublic(DiagnosticoBase):
    id:int
    created_at: datetime 
    updated_at: datetime | None = None
