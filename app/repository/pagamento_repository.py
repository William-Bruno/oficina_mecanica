from sqlmodel import Session, select

from app.models.pagamento import Pagamento

class PagamentoRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, pagamento: Pagamento) ->Pagamento:
        self.session.add(pagamento)
        self.session.commit()
        self.session.refresh(pagamento)
        return pagamento

    def get_by_ordem_servico_id(self, ordem_servico_id:int) -> list[Pagamento]:
        statement = select(Pagamento).where(Pagamento.ordem_servico_id == ordem_servico_id)
        return list(self.session.exec(statement).all())


