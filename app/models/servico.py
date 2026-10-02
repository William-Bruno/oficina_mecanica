from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

class ServicoBase(SQLModel):
    descricao: str = Field(min_length=3, max_length=250, index=True)
    preco: float = Field(gt=0, nullable=False)

class Servico(ServicoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(SQLModel):
    descricao: str | None = None
    preco: float | None = Field(default=None, gt=0)

class ServicoPublic(ServicoBase):
    id: int
    created_at: datetime 
    updated_at: datetime | None = None
