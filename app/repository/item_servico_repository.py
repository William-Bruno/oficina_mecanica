from sqlmodel import Session, select

from app.models.item_servico import ItemServico, ItemServicoCreate, ItemServicoUpdate

class ItemServicoRepository:
    def __init__(self, session:Session):
        self.session = session

    def _salvar(self, item_servico_db:ItemServico) -> ItemServico:
        self.session.add(item_servico_db)
        self.session.commit()
        self.session.refresh(item_servico_db)
        return item_servico_db

    def rollback(self) -> None:
        self.session.rollback()

    def get_by_id(self, item_servico_id:int) -> ItemServico | None:
        return self.session.get(ItemServico, item_servico_id)

    def get_by_ordem_servico_id(self, ordem_servico_id:int) -> list[ItemServico]:
        statement = select(ItemServico).where(ItemServico.ordem_servico_id == ordem_servico_id)
        resultados = self.session.exec(statement).all()
        return list(resultados)

    def get_by_ordem_servico_e_servico(self, orderm_servico_id:int, servico_id:int) -> ItemServico | None:
        statement = select(ItemServico).where(ItemServico.ordem_servico_id == orderm_servico_id, ItemServico.servico_id == servico_id)
        return self.session.exec(statement).first()

    def create(self, ordem_servico_id:int, dados: ItemServicoCreate) -> ItemServico:
        item_servico_db = ItemServico.model_validate(
            dados,
            update={"ordem_servico_id": ordem_servico_id})
        return self._salvar(item_servico_db)

    def update(self, item_servico_db: ItemServico, dados: ItemServicoUpdate) -> ItemServico:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        item_servico_db.sqlmodel_update(dados_atualizados)
        return self._salvar(item_servico_db)

    def delete(self, item_servico_db: ItemServico) -> None:
        self.session.delete(item_servico_db)
        self.session.commit()
