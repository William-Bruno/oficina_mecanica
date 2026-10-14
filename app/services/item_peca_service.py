from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    RecursoNaoEncontradoException,
    RegraDeNegocioException,
    ViolacaoChaveEstrangeiraException
)
from app.models.enums import StatusOrdemServico
from app.models.item_peca import (
    ItemPeca,
    ItemPecaCreate,
    ItemPecaUpdate
)

from app.models.ordem_servico import OrdemServico

from app.repository.item_peca_repository import ItemPecaRepository
from app.repository.ordem_servico_repository import OrdemServicoRepository
from app.repository.peca_repository import PecaRepository

from app.services.ordem_servico_service import OrdemServicoService

class ItemPecaService:
    def __init__(
            self, 
            repository: ItemPecaRepository,
            ordem_servico_repository: OrdemServicoRepository,
            peca_repository: PecaRepository,
            ordem_servico_service: OrdemServicoService
    ):
        self.repository = repository
        self.ordem_servico_repository = ordem_servico_repository
        self.peca_repository = peca_repository
        self.ordem_servico_service = ordem_servico_service

    def _validar_ordem_servico(self, ordem_servico_id:int) -> OrdemServico:
        ordem_servico_db = self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not ordem_servico_db:
            raise RecursoNaoEncontradoException(f"Ordem de Serviço com ID {ordem_servico_id} não encontrada.")
        if ordem_servico_db.status in (StatusOrdemServico.CONCLUIDA, StatusOrdemServico.CANCELADA):
            raise RegraDeNegocioException(f"Nãoé possível alterar itens de uma Ordem de Serviço com status {ordem_servico_db.status}")
        return ordem_servico_db

    def _validar_peca(self, peca_id:int) -> None:
        peca_db = self.peca_repository.get_by_id(peca_id)
        if not peca_db:
            raise RecursoNaoEncontradoException(f"Peça com ID {peca_id} não encontada")

    def _buscar_item_peca_por_id(self, item_peca_id:int) -> ItemPeca:
        item_peca_db = self.repository.get_by_id(item_peca_id)
        if not item_peca_id:
            raise RecursoNaoEncontradoException(f"Item de peça com ID {item_peca_id} não encontrado.")
        return item_peca_db

    def listar_por_ordem_servico_id(self, ordem_servico_id:int) -> list[ItemPeca]:
        ordem_servico_db = self.ordem_servico_repository.get_by_id(ordem_servico_id)
        if not ordem_servico_db:
            raise RecursoNaoEncontradoException(f"Ordem de Serviço com ID {ordem_servico_id} não encontrada.")
        return self.repository.get_by_ordem_servico_id(ordem_servico_id)

    def buscar_por_id(self, item_peca_id:int) -> ItemPeca:
        return self._buscar_item_peca_por_id(item_peca_id)

    def criar(self, ordem_servico_id:int, dados:ItemPecaCreate) -> ItemPeca:
        self._validar_ordem_servico(ordem_servico_id)
        self._validar_peca(dados.peca_id)

        # Veriica se a peça já foi adicionada
        peca_existente = self.repository.get_by_ordem_servico_e_peca(ordem_servico_id, dados.peca_id)
        if peca_existente:
            raise RegraDeNegocioException(
                f"Esta peça já está cadastrada nesta Ordem de Serviço com {peca_existente.quantidade} unidade(s). "
                "Para alterar, atualize a quantidade do item existente."
            )
        # Cria normalmente
        try:
            nova_peca = self.repository.create(ordem_servico_id, dados)
            self.ordem_servico_service.atualizar_valor_total(ordem_servico_id)
            return nova_peca
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao adicionar a peça à Ordem de Serviço.")

    def atualizar(self, item_peca_id:int, dados:ItemPecaUpdate) -> ItemPeca:
        item_peca_db = self._buscar_item_peca_por_id(item_peca_id)
        self._validar_ordem_servico(item_peca_db.ordem_servico_id)

        if dados.peca_id and dados.peca_id != item_peca_db.peca_id:
            self._validar_ordem_servico(dados.peca_id)

        try:
            item_peca_atualizada = self.repository.update(item_peca_db, dados)
            self.ordem_servico_service.atualizar_valor_total(item_peca_db.ordem_servico_id)
            return item_peca_atualizada
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao atalizar peça de serviço")

    def remover(self, item_peca_id:int) -> dict[str,str]:
        item_peca_db = self._buscar_item_peca_por_id(item_peca_id)
        self._validar_ordem_servico(item_peca_db.ordem_servico_id)

        try:
            self.repository.delete(item_peca_db)
            self.ordem_servico_service.atualizar_valor_total(item_peca_db.ordem_servico_id)
            return {"message":"Item de peça removida com sucesso!"}
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException(
                "Não foi possível remover o item de peça devido a restrições"
            )
        

    