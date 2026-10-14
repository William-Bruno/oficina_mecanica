from datetime import datetime

from sqlmodel import Session, select, func
from app.models.ordem_servico import OrdemServico, OrdemServicoCreate, OrdemServicoUpdate
from app.models.enums import StatusOrdemServico

class OrdemServicoRepository:
    def __init__(self, session:Session):
        self.session = session

    def _salvar(self, ordem_db: OrdemServico) -> OrdemServico:
        self.session.add(ordem_db)
        self.session.commit()
        self.session.refresh(ordem_db)
        return ordem_db

    def rollback(self) -> None:
        self.session.rollback()

    def get_by_id(self, ordem_servico_id:int) -> OrdemServico | None:
        return self.session.get(OrdemServico, ordem_servico_id)

    def get_paginado(
            self,
            p:int=1,
            tp:int=10,
            status:StatusOrdemServico|None=None,
            veiculo_id:int | None = None,
            mecanico_id:int | None = None,
            data_inicio:datetime | None = None,
            data_fim:datetime|None = None,
    ) -> tuple[list[OrdemServico], int]:
        statement = select(OrdemServico)

        if status:
            statement = statement.where(OrdemServico.status == status)
        if veiculo_id:
            statement = statement.where(OrdemServico.veiculo_id == veiculo_id)
        if mecanico_id:
            statement = statement.where(OrdemServico.mecanico_id == mecanico_id)
        if data_inicio:
            statement = statement.where(OrdemServico.created_at >= data_inicio)
        if data_fim:
            statement = statement.where(OrdemServico.created_at <= data_fim)

        count_statment = select(func.count()).select_from(statement.subquery())
        total_registros = self.session.exec(count_statment).one()

        offset = (p-1)*tp
        statement = statement.offset(offset).limit(tp).order_by(OrdemServico.created_at.desc())

        ordens_servicos = list(self.session.exec(statement).all())
        return ordens_servicos, total_registros

    def create(self, dados: OrdemServicoCreate) -> OrdemServico:
        ordem_db = OrdemServico.model_validate(dados)
        return self._salvar(ordem_db)

    def update(self, ordem_db: OrdemServico, dados: OrdemServicoUpdate) -> OrdemServico:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        ordem_db.sqlmodel_update(dados_atualizados)
        return self._salvar(ordem_db)

    def delete(self, ordem_db: OrdemServico) -> None:
        self.session.delete(ordem_db)
        self.session.commit()