from sqlmodel import Session, select

from app.models.item_peca import ItemPeca, ItemPecaCreate, ItemPecaUpdate

class ItemPecaRepository:
    def __init__(self, session:Session):
        self.session = session

    def _salvar(self, item_peca_db:ItemPeca) -> ItemPeca:
        self.session.add(item_peca_db)
        self.session.commit()
        self.session.refresh(item_peca_db)
        return item_peca_db

    def rollback(self) -> None:
        self.session.rollback()

    def get_by_id(self, item_peca_id:int) -> ItemPeca | None:
        return self.session.get(ItemPeca, item_peca_id)

    def get_by_ordem_servico_id(self, ordem_servico_id:int) -> list[ItemPeca]:
        statement = select(ItemPeca).where(ItemPeca.ordem_servico_id == ordem_servico_id)
        resultados = self.session.exec(statement).all()
        return list(resultados)

    def get_by_ordem_servico_e_peca(self, orderm_servico_id:int, peca_id:int) -> ItemPeca | None:
        statement = select(ItemPeca).where(ItemPeca.ordem_servico_id == orderm_servico_id, ItemPeca.peca_id == peca_id)
        return self.session.exec(statement).first()

    def create(self, ordem_servico_id:int, dados: ItemPecaCreate) -> ItemPeca:
        item_peca_db = ItemPeca.model_validate(
            dados,
            update={"ordem_servico_id": ordem_servico_id})
        return self._salvar(item_peca_db)

    def update(self, item_peca_db: ItemPeca, dados: ItemPecaUpdate) -> ItemPeca:
        dados_atualizados = dados.model_dump(exclude_unset=True)
        item_peca_db.sqlmodel_update(dados_atualizados)
        return self._salvar(item_peca_db)

    def delete(self, item_peca_db: ItemPeca) -> None:
        self.session.delete(item_peca_db)
        self.session.commit()
