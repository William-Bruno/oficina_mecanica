from app.models.relatorio import RelatorioInadimplencia
from app.repository.relatorios_repository import RelatorioRepository

class RelatorioService:
    def __init__(self, repository: RelatorioRepository):
        self.repository = repository

    def relatorio_inadimplencia(self) -> list[RelatorioInadimplencia]:
        resultados = self.repository.get_inadimplencia()

        relatorio = []
        for resultado in resultados:
            nome, telefone, placa, ordem_serico_id, valor_total, total_pago = resultado
            saldo_devedor = valor_total-total_pago
            
            item = RelatorioInadimplencia(
                cliente_nome=nome,
                telefone=telefone,
                veiculo_placa=placa,
                ordem_servico_id=ordem_serico_id,
                valor_total_ordem_servico=valor_total,
                total_pago=total_pago,
                saldo_devedor=saldo_devedor
            )

            relatorio.append(item)

        return relatorio