from decimal import Decimal

from app.core.exceptions import RecursoNaoEncontradoException, RegraDeNegocioException, RequisicaoInvalidaException

from app.models.pagamento import Pagamento, PagamentoCreate
from app.models.enums import StatusOrdemServico

from app.repository.pagamento_repository import PagamentoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository

class PagamentoService:
    def __init__(self, repository: PagamentoRepository, ordem_servico_repository: OrdemServicoRepository):
        self.repository = repository
        self.ordem_servico_repository = ordem_servico_repository

    def registrar_pagamento(self, ordem_servico_id:int, dados:PagamentoCreate) -> Pagamento:
        ordem_servico_db = self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not ordem_servico_db:
            raise RecursoNaoEncontradoException(
                f"Ordem de Serviço com ID {ordem_servico_id} não encontrada. "
            )

        if ordem_servico_db.status == StatusOrdemServico.CANCELADA:
            raise RequisicaoInvalidaException(
                f"Não é possivel receber pagamento para uma Ordem de Serviço com status CANCELADA."
            )

        total_pecas = sum(
            (item.quantidade * item.preco_unitario) for item in ordem_servico_db.itens_pecas if item.aprovado
        )
        total_servicos = sum(
            (item.tempo_hora * item.valor_hora) for item in ordem_servico_db.itens_servicos if item.aprovado
        )

        total_ordem_servico = total_pecas + total_servicos
        if total_ordem_servico == Decimal("0.00"):
            raise RequisicaoInvalidaException(
                f"Ordem de Serviço não possi peças ou serviços aprovados para gerar cobrança"
            )

        pagamentos_realizados = self.repository.get_by_ordem_servico_id(ordem_servico_db.id)
        total_pago = sum(p.valor for p in pagamentos_realizados)
        saldo_devedor = total_ordem_servico - total_pago

        if saldo_devedor <=Decimal("0.00"):
            raise RequisicaoInvalidaException(
                f"Ordem de serviço já está totalmente paga."
            )
        if dados.valor > saldo_devedor:
            raise RequisicaoInvalidaException(
                f"O valor de pagamento  (R$ {dados.valor:.2f}) excede o saldo devedor atual (R$ {saldo_devedor:.2f})"
            )

        novo_pagamento = Pagamento(
            valor = dados.valor,
            forma_pagamento=dados.forma_pagamento,
            ordem_servico_id=ordem_servico_id
        )
        if ordem_servico_db.valor_total != total_ordem_servico:
            ordem_servico_db.valor_total = total_ordem_servico
            self.ordem_servico_repository.update(ordem_servico_db)

        return self.repository.create(novo_pagamento)