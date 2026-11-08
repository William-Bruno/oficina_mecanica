from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    ViolacaoChaveEstrangeiraException, 
    CampoDuplicadoException, 
    RecursoNaoEncontradoException,
    ConflitoEstadoException,
    )

from app.models.peca import Peca, PecaCreate, PecaUpdate, PecaPage
from app.models.paginacao import Paginacao
from app.repository.peca_repository import PecaRepository

class PecaService:
    
    def __init__(self, repository: PecaRepository):
        self.repository = repository

    def _validar_peca_nome(self, nome:str)->None:
        existe = self.repository.get_by_nome(nome)
        if existe:
            raise CampoDuplicadoException("Já existe uma peça cadastrado com este nome")

    def buscar_por_id(self, peca_id:int) -> Peca:
        peca = self.repository.get_by_id(peca_id)
        if not peca:
            raise RecursoNaoEncontradoException(f"Peca com ID {peca_id} não encontrado")
        return peca

    def listar_paginado(self, pagina:int=1,tamanho_pagina:int=10,nome:str|None=None,ativo:bool|None=None) -> PecaPage:
        pecas, total_registros = self.repository.get_paginado(
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
            nome=nome,
            ativo=ativo
        )

        if total_registros > 0:
            total_paginas = (total_registros + tamanho_pagina - 1) // tamanho_pagina
        else:
            total_paginas = 0

        return PecaPage(
            dados=pecas,
            paginacao=Paginacao(
                total_registros=total_registros,
                total_paginas=total_paginas,
                pagina_atual=pagina,
                tamanho_pagina=tamanho_pagina
            )
        )

    def criar(self, dados:PecaCreate) -> Peca:
        if dados.nome:
            self._validar_peca_nome(dados.nome)
        try:
            return self.repository.create(dados)
        except IntegrityError:
            raise ViolacaoChaveEstrangeiraException("Erro de integridade ao cadastrar a peça")

    def atualizar(self, peca_id:int, dados:PecaUpdate) -> Peca:
        dados_id = self.buscar_por_id(peca_id)
        
        if dados.nome and dados.nome != dados_id.nome:
            self._validar_peca_nome(dados.nome)
        try:
            return self.repository.update(dados_id, dados)
        except IntegrityError:
            self.repository.rollback()
            raise ViolacaoChaveEstrangeiraException("Erro de intgridade ao atualizar peca")

    def ativar(self, peca_id:int) -> Peca:
        peca_db = self.buscar_por_id(peca_id)

        if peca_db.ativo:
            raise ConflitoEstadoException(
                f"A peça {peca_db.nome} já está ativa"
            )
        return self.repository.active(peca_db)

    def desativar(self, peca_id:int) -> Peca:
        peca_db = self.buscar_por_id(peca_id)

        if not peca_db.ativo:
            raise ConflitoEstadoException(
                f"A peça {peca_db.nome} já está desativada"
            )
        return self.repository.deactive(peca_db)