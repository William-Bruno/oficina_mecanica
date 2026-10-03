from sqlalchemy import func
from sqlmodel import Session, select

from app.models.cliente import Cliente, ClienteCreate, ClienteUpdate

class ClienteRepository:

    def __init__(self, session:Session):
        self.session = session

    def get_by_id(self, cliente_id: int) -> Cliente | None:
        """Busca um clinente pelo ID """
        return self.session.get(Cliente, cliente_id)

    def get_by_email(self, email:str) -> Cliente | None:
        """Busca um cliente peo email"""
        statement = select(Cliente).where(Cliente.email == email)
        return self.session.exec(statement).first()

    def get_paginado(
        self, 
        pagina:int=1, 
        tamanho_pagina:int=10, 
        nome:str|None=None, 
        email:str|None=None,) -> tuple[list[Cliente],int]:
        """Lista de clientes paginada e total de registros"""
        consulta = select(Cliente)
        consulta_total = select(func.count()).select_from(Cliente)

        # Filtro nome
        if nome:
            filtro_nome = Cliente.nome.ilike(f"%{nome}")
            consulta = consulta.where(filtro_nome)
            consulta_total = consulta_total.where(filtro_nome)

        # Filtro email
        if email:
            filtro_email = Cliente.email.ilike(f"%{email}")
            consulta = consulta.where(filtro_email)
            consulta_total = consulta_total.where(filtro_email)

        #contagem total dos filtros
        total_registros = self.session.exec(consulta_total).one()

        # calcula o deslocamento e ordena
        deslocamento = (pagina-1)*tamanho_pagina
        consulta = (consulta.order_by(Cliente.nome).offset(deslocamento).limit(tamanho_pagina))

        clientes = self.session.exec(consulta).all()
        return clientes, total_registros

    def create(self, dados: ClienteCreate)->Cliente:
        """Cria e adiciona um cliente no banco"""
        cliente = Cliente.model_validate(dados)
        self.session.add(cliente)
        self.session.commit()
        self.session.refresh(cliente)
        return cliente

    def update(self, dados_db: Cliente, dados: ClienteUpdate) -> Cliente:
        """Atualiza os campos do cliente no banco"""
        dados_atualizados = dados.model_dump(exclude_unset=True)
        dados_db.sqlmodel_update(dados_atualizados)
        self.session.add(dados_db)
        self.session.commit()
        self.session.refresh(dados_db)
        return dados_db
        
    def delete(self, dados_db:Cliente) -> None:
        """Remover cliente o banco"""
        self.session.delete(dados_db)
        self.session.commit()

    def rollback(self) -> None:
        """Desfaz transação"""
        self.session.rollback()

        