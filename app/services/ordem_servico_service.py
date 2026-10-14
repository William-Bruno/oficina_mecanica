from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    RecursoNaoEncontradoException,
    RegraDeNegocioException,
    ViolacaoChaveEstrangeiraException,
)
from app.models.enums import StatusOrdemServico
from app.models.ordem_servico import (
    OrdemServico,
    OrdemServicoCreate,
    OrdemServicoPage,
    OrdemServicoUpdate,
)
from app.models.paginacao import Paginacao
from app.repository.mecanico_repository import MecanicoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.repository.veiculo_repository import VeiculoRepository

class OrdemServicoService:

    def __init__(
        self,
        repository: OrdemServicoRepository,
        veiculo_repository: VeiculoRepository,
        mecanico_repository: MecanicoRepository,
    ):
        self.repository = repository
        self.veiculo_repository = veiculo_repository
        self.mecanico_repository = mecanico_repository

    def _validar_veiculo_e_cliente(self, veiculo_id: int) -> None:
        """Garante que o veículo informado existe no banco de dados."""
        veiculo = self.veiculo_repository.get_by_id(veiculo_id)
        if not veiculo:
            raise RecursoNaoEncontradoException(
                f"Veículo com ID {veiculo_id} não encontrado."
            )

    def _validar_mecanico(self, mecanico_id: int) -> None:
        """Garante que o mecânico informado existe no banco de dados."""
        mecanico = self.mecanico_repository.get_by_id(mecanico_id)
        if not mecanico:
            raise RecursoNaoEncontradoException(
                f"Mecânico com ID {mecanico_id} não encontrado."
            )

    def _validar_ordem_servico_concluida_cancelada(self, ordem_db: OrdemServico) -> None:
        """Impede alterações em Ordens de Serviço já finalizadas ou canceladas."""
        if ordem_db.status in (StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA,):
            raise RegraDeNegocioException(
                f"A Ordem de Serviço com status {ordem_db.status.value} não pode mais ser alterada."
            )

    def _validar_ordem_servico_status(self, ordem_db: OrdemServico, novo_status: StatusOrdemServico) -> None:
        if ordem_db.status == novo_status:
            return

        # 1. Bloqueia se a OS já estiver em estado terminal (CONCLUIDA / CANCELADA)
        self._validar_ordem_servico_concluida_cancelada(ordem_db)

        # 2. Validação para CONCLUIDA: exige ao menos 1 item (serviço ou peça)
        if novo_status == StatusOrdemServico.CONCLUIDA:
            if not ordem_db.itens_servicos and not ordem_db.itens_pecas:
                raise RegraDeNegocioException(
                    "Não é possível concluir uma Ordem de Serviço sem nenhum serviço ou peça cadastrada."
                )

        # 3. Regra para CANCELAMENTO: só cancela se estiver AGENDADA ou EM_ORCAMENTO
        if novo_status == StatusOrdemServico.CANCELADA:
            if ordem_db.status not in (
                StatusOrdemServico.AGENDADA,
                StatusOrdemServico.EM_ORCAMENTO,
            ):
                raise RegraDeNegocioException(
                    f"Não é possível cancelar uma Ordem de Serviço com status '{ordem_db.status.value}'."
                )
            return

        # 4. Transições a partir de AGENDADA (só pode avançar para EM_ANDAMENTO)
        if ordem_db.status == StatusOrdemServico.AGENDADA:
            if novo_status != StatusOrdemServico.EM_ANDAMENTO:
                raise RegraDeNegocioException(
                    "Uma Ordem de Serviço 'AGENDADA' só pode ser alterada para 'EM_ANDAMENTO' ou 'CANCELADA'."
                )

        # 5. Transições a partir de EM_ANDAMENTO (pode ir para EM_ORCAMENTO ou CONCLUIDA)
        elif ordem_db.status == StatusOrdemServico.EM_ANDAMENTO:
            if novo_status not in (
                StatusOrdemServico.EM_ORCAMENTO,
                StatusOrdemServico.CONCLUIDA,
            ):
                raise RegraDeNegocioException(
                    "Uma Ordem de Serviço 'EM_ANDAMENTO' só pode avançar para 'EM_ORCAMENTO' ou 'CONCLUIDA'."
                )

        # 6. Transições a partir de EM_ORCAMENTO (retorna para EM_ANDAMENTO ao aprovar)
        elif ordem_db.status == StatusOrdemServico.EM_ORCAMENTO:
            if novo_status != StatusOrdemServico.EM_ANDAMENTO:
                raise RegraDeNegocioException(
                    "Uma Ordem de Serviço 'EM_ORCAMENTO' precisa retornar para 'EM_ANDAMENTO' ao ser aprovada."
                )

    def _recalcular_valor_total(self, ordem_db: OrdemServico) -> Decimal:
        """Calcula o valor total somando itens de serviços e peças aprovados com precisão Decimal."""
        total_servicos = sum(
            (
                Decimal(str(item.tempo_hora)) * Decimal(str(item.valor_hora))
                for item in ordem_db.itens_servicos
                if item.aprovado
            ),
            Decimal("0.00"),
        )

        total_pecas = sum(
            (
                Decimal(str(item.quantidade))
                * Decimal(str(item.preco_unitario))
                for item in ordem_db.itens_pecas
                if item.aprovado
            ),
            Decimal("0.00"),
        )

        return total_servicos + total_pecas


    def buscar_por_id(self, ordem_servico_id: int) -> OrdemServico:
        """Busca Ordem de Serviço por ID. Lança 404 se não existir."""
        ordem_servico = self.repository.get_by_id(ordem_servico_id)
        if not ordem_servico:
            raise RecursoNaoEncontradoException(f"Ordem de Serviço com ID {ordem_servico_id} não encontrada.")
        return ordem_servico

    def listar_paginado(
        self,
        p: int = 1,
        tp: int = 10,
        status: StatusOrdemServico | None = None,
        veiculo_id: int | None = None,
        mecanico_id: int | None = None,
        data_inicio: datetime | None = None,
        data_fim: datetime | None = None,
    ) -> OrdemServicoPage:
        """Lista Ordens de Serviço paginadas com suporte a múltiplos filtros."""
        ordens, total_registros = self.repository.get_paginado(
            p=p,
            tp=tp,
            status=status,
            veiculo_id=veiculo_id,
            mecanico_id=mecanico_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )

        total_paginas = ((total_registros + tp - 1) // tp if total_registros > 0 else 0)

        return OrdemServicoPage(
            dados=ordens,
            paginacao=Paginacao(
                total_registros=total_registros,
                total_paginas=total_paginas,
                pagina_atual=p,
                tamanho_pagina=tp,
            ),
        )


    def criar(self, dados: OrdemServicoCreate) -> OrdemServico:
        """Cria uma nova Ordem de Serviço validando todas as chaves estrangeiras."""
        self._validar_veiculo_e_cliente(dados.veiculo_id)
        self._validar_mecanico(dados.mecanico_id)

        try:
            return self.repository.create(dados)
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException(
                "Erro de integridade ao cadastrar a Ordem de Serviço."
            )

    def atualizar(self, ordem_servico_id: int, dados: OrdemServicoUpdate) -> OrdemServico:
        """Atualiza parcialmente uma Ordem de Serviço respeitando a máquina de estados e validações de FK."""
        ordem_db = self.buscar_por_id(ordem_servico_id)

        if dados.status:
            self._validar_ordem_servico_status(ordem_db=ordem_db, novo_status=dados.status)
            if dados.status in (StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA,):
                ordem_db.data_fim = datetime.now(timezone.utc)
        else:
            self._validar_ordem_servico_concluida_cancelada(ordem_db)

        # Validação de troca de veículo
        if dados.veiculo_id and dados.veiculo_id != ordem_db.veiculo_id:
            self._validar_veiculo_e_cliente(dados.veiculo_id)

        # Validação de troca de mecânico
        if dados.mecanico_id and dados.mecanico_id != ordem_db.mecanico_id:
            self._validar_mecanico(dados.mecanico_id)

        try:
            return self.repository.update(ordem_db, dados)
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException(
                "Erro de integridade ao atualizar a Ordem de Serviço."
            )

    def atualizar_valor_total(self, ordem_servico_id: int) -> OrdemServico:
        """Recalcula e persiste o valor total com base nos itens atualizados."""
        ordem_db = self.buscar_por_id(ordem_servico_id)
        ordem_db.valor_total = self._recalcular_valor_total(ordem_db)
        return self.repository._salvar(ordem_db)

    def remover(self, ordem_servico_id: int) -> dict[str, str]:
        """Remove uma Ordem de Serviço caso não possua pagamentos ou itens vinculados."""
        ordem_db = self.buscar_por_id(ordem_servico_id)
        self._validar_ordem_servico_concluida_cancelada(ordem_db)

        try:
            self.repository.delete(ordem_db)
            return {"message": "Ordem de Serviço removida com sucesso!"}
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException(
                "A Ordem de Serviço possui registros associados (itens ou pagamentos) e não pode ser removida."
            )