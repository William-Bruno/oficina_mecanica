from app.core.exceptions import RecursoNaoEncontradoException, RegraDeNegocioException
from app.models.diagnostico import Diagnostico, DiagnosticoCreate, DiagnosticoUpdate
from app.models.enums import StatusOrdemServico
from app.models.veiculo import VeiculoUpdate
from app.repository.diagnostico_repository import DiagnosticoRepository
from app.repository.mecanico_repository import MecanicoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.repository.veiculo_repository import VeiculoRepository

class DiagnosticoService:
    def __init__(
        self,
        repository: DiagnosticoRepository,
        ordem_servico_repository: OrdemServicoRepository,
        veiculo_repository: VeiculoRepository,
        mecanico_repository: MecanicoRepository
    ):
        self.repository = repository
        self.ordem_servico_repository = ordem_servico_repository
        self.veiculo_repository = veiculo_repository
        self.mecanico_repository=mecanico_repository

    def _validar_ordem_servico(self, ordem_servico_id: int):
        ordem_servico_db = self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not ordem_servico_db:
            raise RecursoNaoEncontradoException(
                f"Ordem de Serviço com ID {ordem_servico_id} não encontrada."
            )
        if ordem_servico_db.status in (StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA):
            raise RegraDeNegocioException(
                f"Não é possível diagnosticar uma Ordem de Serviço com status {ordem_servico_db.status}"
            )
        return ordem_servico_db

    def _validar_mecanico(self, mecanico_id: int) -> None:
        """Garante que o mecânico informado existe no banco de dados."""
        mecanico = self.mecanico_repository.get_by_id(mecanico_id)
        if not mecanico:
            raise RecursoNaoEncontradoException(
                f"Mecânico com ID {mecanico_id} não encontrado."
            )
        if not mecanico.ativo:
            raise RegraDeNegocioException(
                f"O mecânico {mecanico.nome} está inativo e não pode ser vinculado"
            )

    def criar(self, ordem_servico_id: int, dados: DiagnosticoCreate) -> Diagnostico:
        ordem_servico_db = self._validar_ordem_servico(ordem_servico_id)
        self._validar_mecanico(dados.mecanico_id)

        diagnostico_existente = self.repository.get_by_ordem_servico_id(ordem_servico_id)
        if diagnostico_existente:
            raise RegraDeNegocioException(
                "Esta Ordem de Serviço já possui um diagnóstico cadastrado. "
            )

        novo_diagnostico = self.repository.create(ordem_servico_id, dados)

        veiculo_db = self.veiculo_repository.get_by_id(ordem_servico_db.veiculo_id)
        if veiculo_db and dados.quilometragem > veiculo_db.quilometragem:
            self.veiculo_repository.update(
                veiculo_db, VeiculoUpdate(quilometragem=dados.quilometragem)
            )

        return novo_diagnostico
    

    def buscar_por_ordem_servico_id(self, ordem_servico_id: int) -> Diagnostico:
        self._validar_ordem_servico(ordem_servico_id)
        
        diagnostico_db = self.repository.get_by_ordem_servico_id(ordem_servico_id)
        if not diagnostico_db:
            raise RecursoNaoEncontradoException(
                f"Nenhum diagnóstico encontrado para a Ordem de Serviço ID {ordem_servico_id}."
            )
        return diagnostico_db

    def atualizar(self, diagnostico_id: int, dados: DiagnosticoUpdate) -> Diagnostico:
        diagnostico_db = self.repository.get_by_id(diagnostico_id)
        if not diagnostico_db:
            raise RecursoNaoEncontradoException(
                f"Diagnóstico com ID {diagnostico_id} não encontrado."
            )
        #verificação de status da ordem do serviço
        self._validar_ordem_servico(diagnostico_db.ordem_servico_id)
        #verificação do mecanico
        if dados.mecanico_id and dados.mecanico_id != diagnostico_db.mecanico_id:
            self._validar_mecanico(dados.mecanico_id)
        
        return self.repository.update(diagnostico_db, dados)
