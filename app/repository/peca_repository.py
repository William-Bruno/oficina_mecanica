from sqlalchemy import func
from sqlmodel import Session, select

from app.models.peca import Peca, PecaCreate,PecaUpdate

class PecaRepository:
    
    def __init__(self, session:Session):
        self.session = session

    def get_by_id(self, peca_id:int) -> Peca | None:
        return self.session.get(Peca, peca_id)

    def get_by_nome(self, descricao:str) -> Peca | None:
        statement = select(Peca).where(Peca.nome == descricao)
        return self.session.exec(statement).first()

    def get_paginado(self, pagina:int=1, tamanho_pagina:int=10,nome:str | None=None,) -> tuple[list[Peca], int]:
        consulta = select(Peca)
        consulta_total = select(func.count()).select_from(Peca)

        #Filtros
        if nome:
            filtro_nome = Peca.nome.ilike(f"%{nome}%")
            consulta= consulta.where(filtro_nome)
            consulta_total = consulta_total.where(filtro_nome)

        total_registros = self.session.exec(consulta_total).one()

        deslocamento = (pagina-1)*tamanho_pagina
        consulta = (consulta.order_by(Peca.id).offset(deslocamento).limit(tamanho_pagina))

        pecas = self.session.exec(consulta).all()
        return pecas, total_registros

    def create(self,dados:PecaCreate)->Peca:
        peca = Peca.model_validate(dados)
        self.session.add(peca)
        self.session.commit()
        self.session.refresh(peca)
        return peca

    def update(self, dados_db: Peca, dados:PecaUpdate) -> Peca:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        dados_db.sqlmodel_update(dados_atualizados)
        self.session.add(dados_db)
        self.session.commit()
        self.session.refresh(dados_db)
        return dados_db

    def delete(self, dados_db:Peca) -> None:
        self.session.delete(dados_db)
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()