from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.servico import Servico, ServicoCreate, ServicoUpdate, ServicoPage
from app.models.paginacao import Paginacao
from app.repository.servico_repository import ServicoRepository

class ServicoService:
    
    def __init__(self, repository: ServicoRepository):
        self.repository = repository

    def buscar_por_id(self, servico_id:int) -> Servico:
        servico = self.repository.get_by_id(servico_id)
        if not servico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Servico com ID {servico_id} não encontrado"
            )
        return servico

    def listar_paginado(self, pagina:int=1,tamanho_pagina:int=10,descricao:str|None=None,) -> ServicoPage:
        servicos, total_registros = self.repository.get_paginado(
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
            descricao=descricao,
        )

        if total_registros > 0:
            total_paginas = (total_registros + tamanho_pagina - 1) // tamanho_pagina
        else:
            total_paginas = 0

        return ServicoPage(
            dados=servicos,
            paginacao=Paginacao(
                total_registros=total_registros,
                total_paginas=total_paginas,
                pagina_atual=pagina,
                tamanho_pagina=tamanho_pagina
            )
        )

    def criar(self, dados:ServicoCreate) -> Servico:
        try:
            return self.repository.create(dados)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade ao cadastrar o mecanico"
            )

    def atualizar(self, servico_id:int, dados:ServicoUpdate) -> Servico:
        dados_id = self.buscar_por_id(servico_id)
        try:
            return self.repository.update(dados_id, dados)
        except IntegrityError:
            self.repository.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de intgridade ao atualizar servico"
            )

    def remover(self, servico_id: int) -> dict[str, str]:
        dados_id = self.buscar_por_id(servico_id)
        try:
            self.repository.delete(dados_id)
            return{"message":"Servico removido com sucesso"}
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Servio possui items de servico e não pode ser removido"
            )