from typing import TYPE_CHECKING, Optional
from datetime import datetime, timezone
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship

from app.models.enums import StatusOrdemServico

from app.models.diagnostico import DiagnosticoPublic
from app.models.item_servico import ItemServicoPublic
from app.models.item_peca import ItemPecaPublic
from app.models.pagamento import PagamentoPublic
from app.models.veiculo import VeiculoClientePublic
from app.models.paginacao import Paginacao

if TYPE_CHECKING:
    from app.models.veiculo import Veiculo
    from app.models.item_servico import ItemServico
    from app.models.item_peca import ItemPeca
    from app.models.pagamento import Pagamento
    from app.models.diagnostico import Diagnostico

class OrdemServicoBase(SQLModel):
    data_inicio: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data_fim: datetime | None = None
    status: StatusOrdemServico = Field(default=StatusOrdemServico.AGENDADA, nullable=False)
    observacao: str = Field(default=None, max_length=150, nullable=False)
    valor_total: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2, nullable=False)
    veiculo_id: int = Field(foreign_key="veiculo.id", nullable=False)

class OrdemServico(OrdemServicoBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},)
    veiculo: "Veiculo" = Relationship(back_populates="ordens_servico")
    itens_servicos: list["ItemServico"] = Relationship(back_populates="ordem_servico")
    itens_pecas: list["ItemPeca"] = Relationship(back_populates="ordem_servico")
    pagamentos: list["Pagamento"] = Relationship(back_populates="ordem_servico")
    diagnostico: Optional["Diagnostico"] = Relationship(back_populates="ordem_servico")

class OrdemServicoCreate(OrdemServicoBase):
    pass

class OrdemServicoUpdate(SQLModel):
    data_inicio: datetime | None = None
    data_fim: datetime | None = None
    status: StatusOrdemServico | None = None
    observacao: str | None = None
    valor_total: Decimal | None = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    veiculo_id: int | None = None  

class OrdemServicoPublic(OrdemServicoBase):
    id: int
    created_at: datetime 
    updated_at: datetime

class OrdemServicoPublicDetalhada(OrdemServicoPublic):
    veiculo: Optional[VeiculoClientePublic] = None
    diagnostico: Optional[DiagnosticoPublic] = None
    itens_servicos: list[ItemServicoPublic] = []
    itens_pecas: list[ItemPecaPublic] = []
    pagamentos: list[PagamentoPublic] = []

    

class OrdemServicoStatusUpdate(SQLModel):
    status: StatusOrdemServico

class OrdemServicoPage(SQLModel):
    dados:list[OrdemServicoPublic]
    paginacao: Paginacao


