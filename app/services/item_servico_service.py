from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    RecursoNaoEncontradoException,
    RegraDeNegocioException,
    ViolacaoChaveEstrangeiraException
)
from app.models.enums import StatusOrdemServico
from app.models.item_servico import (
    ItemServico,
    ItemServicoCreate,
    ItemServicoUpdate
)

from app.models.ordem_servico import OrdemServico 

from app.repository.item_servico_repository import ItemServicoRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.repository.servico_repository import ServicoRepository

from app.services.ordem_servico_service import OrdemServicoService

class ItemServicoService:
    def __init__(
            self,
            repository: ItemServicoRepository,
            ordem_servico_repository: OrdemServicoRepository,
            servico_repository: ServicoRepository,
            ordem_servico_service: OrdemServicoService
    ):
        self.repository = repository
        self.ordem_servico_repository = ordem_servico_repository
        self.servico_repository = servico_repository
        self.ordem_servico_service = ordem_servico_service

    def _validar_ordem_servico(self, ordem_servico_id:int) -> OrdemServico:
        ordem_servico_db = self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not ordem_servico_db:
            raise RecursoNaoEncontradoException(f"Ordem de Serviço com ID {ordem_servico_id} não encontrada.")
        if ordem_servico_db.status in (StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA):
            raise RegraDeNegocioException(f"Nãoé possível alterar itens de uma Ordem de Serviço com status {ordem_servico_db.status}")
        return ordem_servico_db

    def _validar_servico(self, servico_id:int) -> None:
        servico_db = self.servico_repository.get_by_id(servico_id)
        if not servico_db:
            raise RecursoNaoEncontradoException(f"Serviço com ID {servico_id} nao encontrado")

    def _buscar_item_servico_por_id(self, item_servico_id:int) -> ItemServico:
        item_servico_db = self.repository.get_by_id(item_servico_id)
        if not item_servico_db:
            raise RecursoNaoEncontradoException(f"Item de serviço com ID {item_servico_id} não encontrado.")
        return item_servico_db

    def listar_por_ordem_servico_id(self, ordem_servico_id:int) -> list[ItemServico]:
        ordem_servico_db = self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not ordem_servico_db:
            raise RecursoNaoEncontradoException(f"Ordem de Serviço com ID {ordem_servico_id} não encontrada.")
        return self.repository.get_by_ordem_servico_id(ordem_servico_id)

    def buscar_por_id(self, item_servico_id:int) -> ItemServico:
        return self._buscar_item_servico_por_id(item_servico_id)

    def criar(self, ordem_servico_id:int, dados:ItemServicoCreate) -> ItemServico:
        self._validar_ordem_servico(ordem_servico_id)
        self._validar_servico(dados.servico_id)

        #Verifica se já existe
        servico_existente = self.repository.get_by_ordem_servico_e_servico(ordem_servico_id, dados.servico_id)
        if servico_existente:
            raise RegraDeNegocioException(
                f"Este serviço já foi adicionado a esta Ordem de Serviço. "
                "Caso necessário, atualize o tempo ou valor do serviço já existente."
            )
        #Cria o serviço
        try:
            novo_servico = self.repository.create(ordem_servico_id, dados)
            #Calcular o valor total
            self.ordem_servico_service.atualizar_valor_total(ordem_servico_id)
            return novo_servico
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao adicionar o serviço à Ordem de Serviço")

    def atualizar(self, item_servico_id:int, dados:ItemServicoUpdate)-> ItemServico:
        item_servico_db = self._buscar_item_servico_por_id(item_servico_id)
        self._validar_ordem_servico(item_servico_db.ordem_servico_id)

        #valida se houver troca de servico
        if dados.servico_id and dados.servico_id != item_servico_db.servico_id:
            self._validar_ordem_servico(dados.servico_id)

        try:
            item_servico_atualizado = self.repository.update(item_servico_db, dados)
            # atualiza o novo valor da ordem de serviço
            self.ordem_servico_service.atualizar_valor_total(item_servico_db.ordem_servico_id)
            return item_servico_atualizado
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de integridadeao atualizar o item de serviço")

    def remover(self, item_servico_id:int) -> dict[str, str]:
        item_servico_db = self._buscar_item_servico_por_id(item_servico_id)
        self._validar_ordem_servico(item_servico_db.ordem_servico_id)
        
        try:
            self.repository.delete(item_servico_db)
            self.ordem_servico_service.atualizar_valor_total(item_servico_db.ordem_servico_id)
            return {"message":"Item de serviço removido com sucesso!"}
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException(
                "Não foi possível remover o item de serviço devido a restrições"
            )
