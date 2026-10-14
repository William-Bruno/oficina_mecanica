from sqlmodel import Session, select
from app.models.diagnostico import Diagnostico, DiagnosticoCreate, DiagnosticoUpdate

class DiagnosticoRepository:
    def __init__(self, session: Session):
        self.session = session

    def _salvar(self, objeto:Diagnostico) -> Diagnostico:
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)
        return objeto

    def get_by_id(self, diagnostico_id: int) -> Diagnostico | None:
        return self.session.get(Diagnostico, diagnostico_id)

    def get_by_ordem_servico_id(self, ordem_servico_id: int) -> Diagnostico | None:
        statement = select(Diagnostico).where(Diagnostico.ordem_servico_id == ordem_servico_id)
        return self.session.exec(statement).first()

    def create(self, ordem_servico_id:int, dados: DiagnosticoCreate) -> Diagnostico:
        diagnostico_db = Diagnostico.model_validate(dados, update={"ordem_servico_id": ordem_servico_id})
        return self._salvar(diagnostico_db)

    def update(self, diagnostico_db: Diagnostico, dados:DiagnosticoUpdate) -> Diagnostico:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        diagnostico_db.sqlmodel_update(dados_atualizados)
        return self._salvar(diagnostico_db)

    def delete(self, diagnostico_db: Diagnostico) -> None:
        self.session.delete(diagnostico_db)
        self.session.commit()
    