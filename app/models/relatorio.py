from decimal import Decimal
from pydantic import BaseModel, Field, field_serializer

class RelatorioInadimplencia(BaseModel):
    cliente_nome: str
    telefone:str
    veiculo_placa: str
    ordem_servico_id:int
    #problemas com a exibicão do Decimal no Swagger
    valor_total_ordem_servico: Decimal = Field(json_schema_extra={"example": 200.00})
    total_pago: Decimal = Field(json_schema_extra={"example": 50.00})
    saldo_devedor: Decimal = Field(json_schema_extra={"example": 150.00})

    @field_serializer("valor_total_ordem_servico", "total_pago", "saldo_devedor")
    def formatar_valor(self, valor: Decimal | float | None) -> Decimal:
        if valor is None:
            return Decimal("0.00")
        return Decimal(str(valor)).quantize(Decimal("0.01"))