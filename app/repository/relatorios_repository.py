from sqlmodel import Session, select, func
from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.ordem_servico import OrdemServico
from app.models.pagamento import Pagamento
from app.models.enums import StatusOrdemServico

class RelatorioRepository:
    def __init__(self, session:Session):
        self.session = session

    def get_inadimplencia(self):
        statement_pagamentos = (
        select(
            Pagamento.ordem_servico_id,
            func.coalesce(func.sum(Pagamento.valor), 0).label("total_pago")
        ).group_by(
            Pagamento.ordem_servico_id
        ).subquery())

        statement = (
        select(
            Cliente.nome,
            Cliente.telefone,
            Veiculo.placa,
            OrdemServico.id,
            OrdemServico.valor_total,
            func.coalesce(statement_pagamentos.c.total_pago, 0).label("total_pago")
        ).join(
            Veiculo, Veiculo.cliente_id == Cliente.id
        ).join(
            OrdemServico, OrdemServico.veiculo_id == Veiculo.id
        ).outerjoin(
            statement_pagamentos, statement_pagamentos.c.ordem_servico_id == OrdemServico.id
        ).where(
            OrdemServico.status == StatusOrdemServico.CONCLUIDA
        ).where(
            OrdemServico.valor_total > func.coalesce(statement_pagamentos.c.total_pago, 0)
        ))

        return self.session.exec(statement).all()


    