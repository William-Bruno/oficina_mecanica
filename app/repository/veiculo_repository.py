from sqlmodel import Session, select, func
from app.models.veiculo import Veiculo, VeiculoCreate, VeiculoUpdate

class VeiculoRepository:
    def __init__(self, session:Session):
        self.session = session

    def _salvar(self, objeto):
        self.session.add(objeto)
        self.session.commit()
        self.session.refresh(objeto)
        return objeto

    def get_by_id(self, veiculo_id:int)->Veiculo | None:
        return self.session.get(Veiculo, veiculo_id)

    def get_by_placa(self, placa:str) -> Veiculo | None:
        statement = select(Veiculo).where(Veiculo.placa == placa)
        return self.session.exec(statement).first()

    def get_paginado(self, 
                     p:int=1, 
                     tp:int=10, 
                     placa:str|None=None, 
                     cliente_id:int|None=None)->tuple[list[Veiculo], int]:
        statement = select(Veiculo)

        if placa:
            statement = statement.where(Veiculo.placa.contains(placa))
        if cliente_id:
            statement = statement.where(Veiculo.cliente_id == cliente_id)

        count_statement = select(func.count()).select_from(statement.subquery())
        total_registros = self.session.exec(count_statement).one()

        offset = (p-1)*tp
        statement = statement.offset(offset).limit(tp).order_by(Veiculo.placa)

        veiculos = list(self.session.exec(statement).all())
        return veiculos, total_registros

    def create(self, dados:VeiculoCreate) -> Veiculo:
        veiculo_db = Veiculo.model_validate(dados)
        return self._salvar(veiculo_db)

    def update(self, dados:Veiculo, veiculo_in: VeiculoUpdate)->Veiculo:
        dados_atuaizados = veiculo_in.model_dump(exclude_unset=True)
        dados.sqlmodel_update(dados_atuaizados)
        return self._salvar(dados)
        

    def delete(self, veiculo_db:Veiculo)->None:
        self.session.delete(veiculo_db)
        self.session.commit()

    def rollback(self)->None:
        self.session.rollback()
