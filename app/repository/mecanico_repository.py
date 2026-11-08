from sqlalchemy import func
from sqlmodel import Session, select

from app.models.mecanico import Mecanico, MecanicoCreate, MecanicoUpdate

class MecanicoRepository:
    
    def __init__(self, session:Session):
        self.session = session

    def _salvar(self, objeto):
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)
        return objeto

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
                     ativo:bool|None=None,
                     ) -> tuple[list[Mecanico], int]:
        consulta = select(Mecanico)
        consulta_total = select(func.count()).select_from(Mecanico)

        #Filtros
        if nome:
            filtro_nome = Mecanico.nome.ilike(f"%{nome}%")
            consulta= consulta.where(filtro_nome)
            consulta_total = consulta_total.where(filtro_nome)

        # Filtro especialidade
        if especialidade:
            filtro_especialidade = Mecanico.especialidade.ilike(f"%{especialidade}")
            consulta =consulta.where(filtro_especialidade)
            consulta_total = consulta_total.where(filtro_especialidade)

        #Filtro de Ativa/Inativa
        if ativo is not None:
            consulta = consulta.where(Mecanico.ativo == ativo)
            consulta_total = consulta_total.where(Mecanico.ativo == ativo)

        total_registros = self.session.exec(consulta_total).one()

        deslocamento = (pagina-1)*tamanho_pagina
        consulta = (consulta.order_by(Mecanico.nome).offset(deslocamento).limit(tamanho_pagina))

        mecanicos = self.session.exec(consulta).all()
        return mecanicos, total_registros

    def create(self,dados:MecanicoCreate)->Mecanico:
        mecanico = Mecanico.model_validate(dados)
        return self._salvar(mecanico)

    def update(self, dados_db: Mecanico, dados:MecanicoUpdate) -> Mecanico:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        dados_db.sqlmodel_update(dados_atualizados)
        return self._salvar(dados_db)

    def active(self, dados_db:Mecanico) -> None:
        dados_db.ativo = True
        return self._salvar(dados_db)
    
    def deactive(self, dados_db:Mecanico) -> None:
        dados_db.ativo = False
        return self._salvar(dados_db) 

    def rollback(self) -> None:
        self.session.rollback()