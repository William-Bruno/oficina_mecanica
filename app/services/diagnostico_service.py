from app.core.exceptions import RecursoNaoEncontradoException, RegraDeNegocioException
from app.models.diagnostico import Diagnostico, DiagnosticoCreate, DiagnosticoUpdate
from app.repository.diagnostico_repository import DiagnosticoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository

class DiagnosticoService:
    def __init__(
        self,
        repository: DiagnosticoRepository,
        ordem_servico_repository: OrdemServicoRepository,
    ):
        self.repository = repository
        self.ordem_servico_repository = ordem_servico_repository

    def _validar_ordem_servico(self, ordem_servico_id: int):
        ordem_db = self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not ordem_db:
            raise RecursoNaoEncontradoException(
                f"Ordem de Serviço com ID {ordem_servico_id} não encontrada."
            )

    def criar(self, ordem_servico_id: int, dados: DiagnosticoCreate) -> Diagnostico:
        self._validar_ordem_servico(ordem_servico_id)

        diagnostico_existente = self.repository.get_by_ordem_servico_id(ordem_servico_id)
        if diagnostico_existente:
            raise RegraDeNegocioException(
                "Esta Ordem de Serviço já possui um diagnóstico cadastrado. "
            )

        return self.repository.create(ordem_servico_id, dados)

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
            
        return self.repository.update(diagnostico_db, dados)

    def remover(self, diagnostico_id: int) -> dict[str, str]:
        diagnostico_db = self.repository.get_by_id(diagnostico_id)
        if not diagnostico_db:
            raise RecursoNaoEncontradoException(
                f"Diagnóstico com ID {diagnostico_id} não encontrado."
            )
            
        self.repository.delete(diagnostico_db)
        return {"mensagem": "Diagnóstico removido com sucesso."}