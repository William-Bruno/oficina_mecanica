from sqlalchemy import func
from sqlmodel import Session, select

from app.models.servico import Servico, ServicoCreate,ServicoUpdate

class ServicoRepository:
    
    def __init__(self, session:Session):
        self.session = session

    def _salvar(self, objeto):
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)
        return objeto

    def get_by_id(self, servico_id:int) -> Servico | None:
        return self.session.get(Servico, servico_id)

    def get_by_descricao(self, descricao:str) -> Servico | None:
        statement = select(Servico).where(Servico.descricao == descricao)
        return self.session.exec(statement).first()

    def get_paginado(self, pagina:int=1, tamanho_pagina:int=10,descricao:str | None=None, ativo:bool|None=None) -> tuple[list[Servico], int]:
        consulta = select(Servico)
        consulta_total = select(func.count()).select_from(Servico)

        #Filtros
        if descricao:
            filtro_descricao = Servico.descricao.ilike(f"%{descricao}%")
            consulta= consulta.where(filtro_descricao)
            consulta_total = consulta_total.where(filtro_descricao)

        #Filtro de Ativa/Inativa
        if ativo is not None:
            consulta = consulta.where(Servico.ativo == ativo)
            consulta_total = consulta_total.where(Servico.ativo == ativo)

        total_registros = self.session.exec(consulta_total).one()

        deslocamento = (pagina-1)*tamanho_pagina
        consulta = (consulta.order_by(Servico.id).offset(deslocamento).limit(tamanho_pagina))

        servicos = self.session.exec(consulta).all()
        return servicos, total_registros

    def create(self,dados:ServicoCreate)->Servico:
        servico = Servico.model_validate(dados)
        return self._salvar(servico)

    def update(self, dados_db: Servico, dados:ServicoUpdate) -> Servico:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        dados_db.sqlmodel_update(dados_atualizados)
        return self._salvar(dados_db)

    def active(self, dados_db:Servico) -> None:
        dados_db.ativo = True
        return self._salvar(dados_db)

    def deactive(self, dados_db:Servico) -> None:
        dados_db.ativo = False
        return self._salvar(dados_db)   

    def rollback(self) -> None:
        self.session.rollback()