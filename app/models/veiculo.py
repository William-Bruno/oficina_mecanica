from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, Relationship

from app.models.enums import CombustivelVeiculo

if TYPE_CHECKING:
    from app.models.cliente import Cliente

class VeiculoBase(SQLModel):
    placa: str = Field(max_length=7, unique=True, index=True)
    marca: str = Field(min_length=3, max_length=120, nullable=False)
    modelo: str = Field(min_length=3, max_length=120, nullable=False)
    ano: int = Field(gt=0)
    combustivel: CombustivelVeiculo = Field(default=CombustivelVeiculo.FLEX, nullable=False)
    cliente_id: int = Field(foreign_key="cliente.id", nullable=False)

class Veiculo(VeiculoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    cliente: "Cliente" = Relationship(back_populates="veiculos")

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoUpdate(SQLModel):
    placa: str | None = None
    marca: str | None = None
    modelo: str | None = None
    ano: int | None = None
    combustivel: CombustivelVeiculo | None = None
    cliente_id: int | None = None

class VeiculoPublic(VeiculoBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None
