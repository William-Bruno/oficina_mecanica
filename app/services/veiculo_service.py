from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ViolacaoChaveEstrangeiraException, CampoDuplicadoException, RecursoNaoEncontradoException

from app.models.paginacao import Paginacao
from app.models.veiculo import Veiculo, VeiculoCreate, VeiculoUpdate, VeiculoPage
from app.repository.cliente_repository import ClienteRepository
from app.repository.veiculo_repository import VeiculoRepository

class VeiculoService:
    def __init__(self, repository:VeiculoRepository, cliente_repository:ClienteRepository):
        self.repository = repository
        self.cliente_repository = cliente_repository

    def _validar_cliente_existente(self, cliente_id:int) -> None:
        cliente_existente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente_existente:
            raise RecursoNaoEncontradoException(
                f"Cliente com ID {cliente_id} não encontrado"
            )

    def _validar_placa_existente(self, placa:str) -> None:
         if self.repository.get_by_placa(placa):
            raise CampoDuplicadoException(
                f"Já existe um veículo cadastrado com a placa {placa}"
            )

    def buscar_por_id(self, veiculo_id:int)->Veiculo:
        veiculo = self.repository.get_by_id(veiculo_id)
        if not veiculo:
            raise RecursoNaoEncontradoException(
                f"Veículo com ID {veiculo_id} não encontrado"
            )
        return veiculo

    def listar_paginado(self,p:int=1,tp:int=10,placa:str|None=None,cliente_id:int|None=None)-> VeiculoPage:
        veiculos, total_registros = self.repository.get_paginado(
            p=p,
            tp=tp,
            placa=placa,
            cliente_id=cliente_id
        )
        total_paginas = (
            (total_registros+tp-1) // tp if total_registros > 0 else 0)

        return VeiculoPage(
            dados=veiculos,
            paginacao=Paginacao(
                total_registros=total_registros,
                total_paginas=total_paginas,
                pagina_atual=p,
                tamanho_pagina=tp
            ),
        )

    def criar(self, dados:VeiculoCreate) -> Veiculo:
        self._validar_cliente_existente(dados.cliente_id)
        self._validar_placa_existente(dados.placa)
        try:
            return self.repository.create(dados)
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao cadastrar o veículo"
            )

    def atualizar(self, veiculo_id:int, dados:VeiculoUpdate) -> Veiculo:
        veiculo_db = self.buscar_por_id(veiculo_id)

        if (dados.cliente_id is not None and dados.cliente_id != veiculo_db.cliente_id):
            self._validar_cliente_existente(dados.cliente_id)
        if dados.placa and dados.placa != veiculo_db.placa:
            self._validar_placa_existente(dados.placa)
        try:
            return self.repository.update(veiculo_db, dados)
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao atualizar veiculo"
            )

    def remover(self, veiculo_id:int) -> dict[str, str]:
        veiculo_db = self.buscar_por_id(veiculo_id)
        try:
            self.repository.delete(veiculo_db)
            return {"message":"Veículo removido com sucesso!"}
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Veículo possui ordens de serviço assoiadas e não pode ser removido."
            )