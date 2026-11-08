from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflitoEstadoException, ViolacaoChaveEstrangeiraException, RecursoNaoEncontradoException

from app.models.mecanico import Mecanico, MecanicoCreate, MecanicoUpdate, MecanicoPage
from app.models.paginacao import Paginacao
from app.repository.mecanico_repository import MecanicoRepository

class MecanicoService:
    
    def __init__(self, repository: MecanicoRepository):
        self.repository = repository

    def buscar_por_id(self, mecanico_id:int) -> Mecanico:
        mecanico = self.repository.get_by_id(mecanico_id)
        if not mecanico:
            raise RecursoNaoEncontradoException(f"Mecanico com ID {mecanico_id} não encontrado")
        return mecanico

    def listar_paginado(self, pagina:int=1,tamanho_pagina:int=10,
                        nome:str|None=None,especialidade:str|None=None, ativo:bool | None=None
                        ) -> MecanicoPage:
        mecanicos, total_registros = self.repository.get_paginado(
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
            nome=nome,
            especialidade=especialidade,
            ativo=ativo
        )

        if total_registros > 0:
            total_paginas = (total_registros + tamanho_pagina - 1) // tamanho_pagina
        else:
            total_paginas = 0

        return MecanicoPage(
            dados=mecanicos,
            paginacao=Paginacao(
                total_registros=total_registros,
                total_paginas=total_paginas,
                pagina_atual=pagina,
                tamanho_pagina=tamanho_pagina
            )
        )

    def criar(self, dados:MecanicoCreate) -> Mecanico:
        try:
            return self.repository.create(dados)
        except IntegrityError:
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao cadastrar o mecanico")

    def atualizar(self, mecanico_id:int, dados:MecanicoUpdate) -> Mecanico:
        dados_id = self.buscar_por_id(mecanico_id)
        try:
            return self.repository.update(dados_id, dados)
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao atualizar mecanico")

    def ativar(self, mecanico_id:int) -> Mecanico:
        mecanico_db = self.buscar_por_id(mecanico_id)

        if mecanico_db.ativo:
            raise ConflitoEstadoException(
                f"O mecanico {mecanico_db.nome} já está ativo"
            )
        return self.repository.active(mecanico_db)

    def desativar(self, mecanico_id:int) -> Mecanico:
        mecanico_db = self.buscar_por_id(mecanico_id)

        if not mecanico_db.ativo:
            raise ConflitoEstadoException(
                f"O mecanico {mecanico_db.nome} já está desativado"
            )
        return self.repository.deactive(mecanico_db)