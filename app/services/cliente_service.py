from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.cliente import Cliente, ClienteCreate,ClienteUpdate, PaginaCliente
from app.models.paginacao import MetadadosPaginacao
from app.repository.cliente_repository import ClienteRepository

class ClienteService:

    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def buscar_por_id(self, cliente_id: int) -> Cliente:
        """busca por id, retorna excecao"""
        cliente = self.repository.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com ID{cliente_id} não econtrado"
            )
        return cliente
    
    def listar_paginado(
        self,
        pagina:int=1,
        tamanho_pagina:int=10,
        nome:str|None = None,
        email:str|None=None
    ) -> PaginaCliente:
        """Lista paginado, calcula os metadados e retorna PaginaCliente"""
        clientes, total_registros = self.repository.get_paginado(
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
            nome=nome,
            email=email,
        )

        if total_registros > 0:
            total_paginas = (total_registros + tamanho_pagina - 1 )//tamanho_pagina
        else:
            total_paginas = 0

        return PaginaCliente(
            dados=clientes,
            paginacao=MetadadosPaginacao(
                total_registros=total_registros,
                total_paginas=total_paginas,
                pagina_atual=pagina,
                tamanho_pagina=tamanho_pagina
            ),
        )

    def criar(self, dados:ClienteCreate) -> Cliente:
        """valida email e cria um noco cliente"""
        if dados.email:
            existe = self.repository.get_by_email(dados.email)
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Já existe um cliente cadastrado com este e-mail"
                )
        try:
            return self.repository.create(dados)
        except IntegrityError:
            self.repository.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade ao cadastrar cliente"
            )

    def atualizar(self, cliente_id:int, dados:ClienteUpdate) -> Cliente:
        """busca o cliente, valida se existe e a duplicidade do email"""
        dados_db = self.buscar_por_id(cliente_id)

        if dados.email and dados.email != dados_db.email:
            existe = self.repository.get_by_email(dados.email)
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Já existe outro cliente cadastrado com este e-mail"
                )
        try:
            return self.repository.update(dados_db,dados)
        except IntegrityError:
            self.repository.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade ao cadastrar cliente"
            )
    
    def remover(self, cliente_id: int) -> dict[str, str]:
        """buscar o cliente e tenta remover"""
        dados_db = self.buscar_por_id(cliente_id)

        try:
            self.repository.delete(dados_db)
            return {"message": "Cliente removido com sucesso"}
        except IntegrityError:
            self.repository.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cliente possui veicuos ou ordens de servico e não pode ser removido"
            )