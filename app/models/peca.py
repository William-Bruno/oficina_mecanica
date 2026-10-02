from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

class PecaBase(SQLModel):
    nome: str = Field(min_length=3, max_length=120, index=True)
    preco: float = Field(gt=0, nullable=False)

class Peca(PecaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None

class PecaCreate(PecaBase):
    pass

class PecaUpdate(SQLModel):
    nome: str | None = None
    preco: float | None = Field(default=None, gt=0)

class PecaPublic(PecaBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None
