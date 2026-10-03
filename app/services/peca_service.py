from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.peca import Peca, PecaCreate, PecaUpdate, PecaPage
from app.models.paginacao import Paginacao
from app.repository.peca_repository import PecaRepository

class PecaService:
    
    def __init__(self, repository: PecaRepository):
        self.repository = repository

    def buscar_por_id(self, peca_id:int) -> Peca:
        peca = self.repository.get_by_id(peca_id)
        if not peca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Peca com ID {peca_id} não encontrado"
            )
        return peca

    def listar_paginado(self, pagina:int=1,tamanho_pagina:int=10,nome:str|None=None,) -> PecaPage:
        pecas, total_registros = self.repository.get_paginado(
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
            nome=nome,
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
            existe = self.repository.get_by_nome(dados.nome)
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Já existe uma peça cadastrado com este nome"
                )
        try:
            return self.repository.create(dados)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade ao cadastrar o mecanico"
            )

    def atualizar(self, peca_id:int, dados:PecaUpdate) -> Peca:
        dados_id = self.buscar_por_id(peca_id)
        
        if dados.nome and dados.nome != dados_id.nome:
            existe = self.repository.get_by_nome(dados.nome)
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Já existe outra peça cadastrada com este nome"
                )
        try:
            return self.repository.update(dados_id, dados)
        except IntegrityError:
            self.repository.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de intgridade ao atualizar peca"
            )

    def remover(self, peca_id: int) -> dict[str, str]:
        dados_id = self.buscar_por_id(peca_id)
        try:
            self.repository.delete(dados_id)
            return{"message":"Peca removido com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Peça possui items de peça e não pode ser removido"
            )