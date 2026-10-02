from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.veiculo import Veiculo

class ClienteBase(SQLModel):
    nome: str = Field(min_length=3, max_length=150, index=True)
    telefone: str = Field(max_length=11, nullable=False)
    email: str = Field(min_length=3, max_length=120, unique=True)


class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    veiculos: list["Veiculo"] = Relationship(back_populates="cliente")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(SQLModel):
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None

class ClientePublic(ClienteBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None
