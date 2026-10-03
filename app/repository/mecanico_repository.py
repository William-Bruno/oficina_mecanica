from sqlalchemy import func
from sqlmodel import Session, select

from app.models.mecanico import Mecanico, MecanicoCreate, MecanicoUpdate

class MecanicoRepository:
    
    def __init__(self, session:Session):
        self.session = session

    def get_by_id(self, mecanico_id:int) -> Mecanico | None:
        return self.session.get(Mecanico, mecanico_id)

    def get_by_nome(self, nome:str) -> Mecanico | None:
        statement = select(Mecanico).where(Mecanico.nome == nome)
        return self.session.exec(statement).first()

    def get_by_especialidade(self, especialidade:str) -> Mecanico | None:
        statement = select(Mecanico).where(Mecanico.especialidade == especialidade)
        return self.session.exec(statement).first()

    def get_paginado(self, pagina:int=1, tamanho_pagina:int=10,
                     nome:str | None=None, especialidade:str|None=None,
                     ) -> tuple[list[Mecanico], int]:
        consulta = select(Mecanico)
        consulta_total = select(func.count()).select_from(Mecanico)

        #Filtros
        if nome:
            filtro_nome = Mecanico.nome.ilike(f"%{nome}%")
            consulta= consulta.where(filtro_nome)
            consulta_total = consulta_total.where(filtro_nome)

        if especialidade:
            filtro_especialidade = Mecanico.especialidade.ilike(f"%{especialidade}")
            consulta =consulta.where(filtro_especialidade)
            consulta_total = consulta_total.where(filtro_especialidade)

        total_registros = self.session.exec(consulta_total).one()

        deslocamento = (pagina-1)*tamanho_pagina
        consulta = (consulta.order_by(Mecanico.nome).offset(deslocamento).limit(tamanho_pagina))

        mecanicos = self.session.exec(consulta).all()
        return mecanicos, total_registros

    def create(self,dados:MecanicoCreate)->Mecanico:
        mecanico = Mecanico.model_validate(dados)
        self.session.add(mecanico)
        self.session.commit()
        self.session.refresh(mecanico)
        return mecanico

    def update(self, dados_db: Mecanico, dados:MecanicoUpdate) -> Mecanico:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        dados_db.sqlmodel_update(dados_atualizados)
        self.session.add(dados_db)
        self.session.commit()
        self.session.refresh(dados_db)
        return dados_db

    def delete(self, dados_db:Mecanico) -> None:
        self.session.delete(dados_db)
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()