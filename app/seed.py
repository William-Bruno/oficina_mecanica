from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select

from app.core.database import engine
from app.models.cliente import Cliente
from app.models.diagnostico import Diagnostico
from app.models.enums import (
    CombustivelVeiculo,
    EspecialidadeMecanico,
    FormaPagamento,
    NivelCombustivel,
    StatusOrdemServico,
)
from app.models.item_peca import ItemPeca
from app.models.item_servico import ItemServico
from app.models.mecanico import Mecanico
from app.models.ordem_servico import OrdemServico
from app.models.pagamento import Pagamento
from app.models.peca import Peca
from app.models.servico import Servico
from app.models.veiculo import Veiculo


def seed_database() -> None:
    with Session(engine) as session:
        # 0. Verifica se o banco já possui dados
        existing_cliente = session.exec(select(Cliente)).first()
        if existing_cliente:
            print("Bando de dados já alimentado.")
            return

        print("Semente iniciada")

        now = datetime.now(timezone.utc)

        # ----------------------------------------------------------------------
        # 1. CLIENTES (10 registros)
        # ----------------------------------------------------------------------
        clientes_data = [
            ("Carlos Eduardo Silva", "85999911101", "carlos.silva@email.com"),
            ("Mariana Albuquerque", "85988822202", "mariana.albuquerque@email.com"),
            ("Fernando Henrique Rocha", "85997733303", "fernando.rocha@email.com"),
            ("Patricia Mendes Lima", "85996644404", "patricia.mendes@email.com"),
            ("Lucas Gabriel Santos", "85995555505", "lucas.santos@email.com"),
            ("Beatriz Vasconcelos", "85994466606", "beatriz.v@email.com"),
            ("Rodrigo Antonio Castro", "85993377707", "rodrigo.castro@email.com"),
            ("Camila de Oliveira", "85992288808", "camila.oliveira@email.com"),
            ("Gustavo Ribeiro Martins", "85991199909", "gustavo.martins@email.com"),
            ("Juliana Barbosa Souza", "85990000010", "juliana.souza@email.com"),
        ]

        clientes = [
            Cliente(nome=nome, telefone=tel, email=email)
            for nome, tel, email in clientes_data
        ]
        session.add_all(clientes)
        session.commit()
        for c in clientes:
            session.refresh(c)

        # ----------------------------------------------------------------------
        # 2. VEÍCULOS (20 registros distribuídos entre os clientes)
        # ----------------------------------------------------------------------
        veiculos_data = [
            ("ABC1D23", "Chevrolet", "Onix 1.0 Turbo", 2022, CombustivelVeiculo.FLEX, clientes[0].id),
            ("XYZ9K87", "Toyota", "Corolla 2.0 Flex", 2021, CombustivelVeiculo.FLEX, clientes[1].id),
            ("KGB4E55", "Volkswagen", "Polo 1.0 TSI", 2023, CombustivelVeiculo.FLEX, clientes[2].id),
            ("JHG7F88", "Fiat", "Argo 1.3 Drive", 2020, CombustivelVeiculo.FLEX, clientes[3].id),
            ("MNB3H22", "Hyundai", "HB20 1.0 Evolution", 2021, CombustivelVeiculo.FLEX, clientes[4].id),
            ("POU8Y11", "Honda", "Civic 2.0 EXL", 2019, CombustivelVeiculo.GASOLINA, clientes[5].id),
            ("QWE5R44", "Ford", "Ka 1.5 SE", 2018, CombustivelVeiculo.FLEX, clientes[6].id),
            ("RTY6U77", "Renault", "Kwid 1.0 Zen", 2022, CombustivelVeiculo.FLEX, clientes[7].id),
            ("UIO9P00", "Jeep", "Renegade 1.8 Longitude", 2020, CombustivelVeiculo.FLEX, clientes[8].id),
            ("ASD2F33", "Nissan", "Kicks 1.6 SV", 2021, CombustivelVeiculo.FLEX, clientes[9].id),
            ("ZXC4V55", "Chevrolet", "Tracker 1.2 Turbo", 2023, CombustivelVeiculo.FLEX, clientes[0].id),
            ("QAZ1W22", "Toyota", "Yaris Hatch 1.5", 2022, CombustivelVeiculo.FLEX, clientes[1].id),
            ("WSX3E44", "Volkswagen", "Virtus 1.6 MSI", 2020, CombustivelVeiculo.FLEX, clientes[2].id),
            ("EDC5R66", "Fiat", "Strada 1.3 Endurance", 2022, CombustivelVeiculo.FLEX, clientes[3].id),
            ("RFV7T88", "Hyundai", "Creta 2.0 Ultimate", 2021, CombustivelVeiculo.FLEX, clientes[4].id),
            ("TGB9Y00", "Honda", "HR-V 1.8 EXL", 2020, CombustivelVeiculo.FLEX, clientes[5].id),
            ("YHN1U22", "Ford", "EcoSport 1.5 Titanium", 2019, CombustivelVeiculo.FLEX, clientes[6].id),
            ("UJM3I44", "Renault", "Duster 1.6 Iconic", 2021, CombustivelVeiculo.FLEX, clientes[7].id),
            ("IKOL5P6", "Jeep", "Compass 1.3 Turbo", 2022, CombustivelVeiculo.FLEX, clientes[8].id),
            ("OLP7K88", "Peugeot", "208 1.6 Griffe", 2022, CombustivelVeiculo.FLEX, clientes[9].id),
        ]

        veiculos = [
            Veiculo(placa=p, marca=m, modelo=mod, ano=a, combustivel=c, cliente_id=cid)
            for p, m, mod, a, c, cid in veiculos_data
        ]
        session.add_all(veiculos)
        session.commit()
        for v in veiculos:
            session.refresh(v)

        # ----------------------------------------------------------------------
        # 3. MECÂNICOS (10 registros)
        # ----------------------------------------------------------------------
        mecanicos_data = [
            ("Roberto 'Beto' Santos", EspecialidadeMecanico.MECANICA_GERAL),
            ("Juliana Costa", EspecialidadeMecanico.INJECAO_ELETRONICA),
            ("Marcos Antonio Vieira", EspecialidadeMecanico.AR_CONDICIONADO),
            ("Fernando Souza", EspecialidadeMecanico.MECANICA_GERAL),
            ("Lucas Dantas", EspecialidadeMecanico.MOTOR_RETIFICA),
            ("Gabriel Nunes", EspecialidadeMecanico.MECANICA_GERAL),
            ("Andre Luis Pinheiro", EspecialidadeMecanico.SUSPENSAO_FREIOS),
            ("Rafael Cavalcante", EspecialidadeMecanico.MECANICA_GERAL),
            ("Thiago Farias", EspecialidadeMecanico.INJECAO_ELETRONICA),
            ("Bruno Eduardo Lima", EspecialidadeMecanico.CAMBIO_AUTOMATICO),
        ]

        mecanicos = [
            Mecanico(nome=nome, especialidade=esp)
            for nome, esp in mecanicos_data
        ]
        session.add_all(mecanicos)
        session.commit()
        for m in mecanicos:
            session.refresh(m)

        # ----------------------------------------------------------------------
        # 4. PEÇAS (30 registros)
        # ----------------------------------------------------------------------
        pecas_data = [
            ("Óleo Motor 5W30 Sintético (1L)", 48.00),
            ("Filtro de Óleo Lubrificante", 38.00),
            ("Filtro de Ar do Motor", 42.00),
            ("Filtro de Combustível", 35.00),
            ("Filtro do Ar-Condicionado", 45.00),
            ("Jogo de Velas de Ignição (4 un)", 140.00),
            ("Jogo de Cabos de Ignição", 120.00),
            ("Pastilha de Freio Dianteira", 190.00),
            ("Pastilha de Freio Traseira", 160.00),
            ("Disco de Freio Dianteiro (Par)", 320.00),
            ("Disco de Freio Traseiro (Par)", 280.00),
            ("Fluido de Freio DOT 4 (500ml)", 35.00),
            ("Amortecedor Dianteiro", 450.00),
            ("Amortecedor Traseiro", 380.00),
            ("Kit Coifa do Amortecedor", 85.00),
            ("Bucha da Bandeja de Suspensão", 65.00),
            ("Pivô de Suspensão", 110.00),
            ("Terminal de Direção", 95.00),
            ("Bateria 60Ah 12V", 480.00),
            ("Correia Dentada", 130.00),
            ("Tensor da Correia Dentada", 170.00),
            ("Kit Correia + Tensor", 280.00),
            ("Bomba d'Água", 240.00),
            ("Aditivo para Radiador (1L)", 32.00),
            ("Palheta do Limpador de Pára-brisa", 65.00),
            ("Lâmpada Farol H7", 28.00),
            ("Bobina de Ignição", 260.00),
            ("Sensor MAP", 185.00),
            ("Sensor de Oxigênio (Sonda Lambda)", 290.00),
            ("Radiador de Água", 520.00),
        ]

        pecas = [
            Peca(nome=nome, preco=p)
            for nome, p in pecas_data
        ]
        session.add_all(pecas)
        session.commit()
        for p in pecas:
            session.refresh(p)

        # ----------------------------------------------------------------------
        # 5. SERVIÇOS (30 registros)
        # ----------------------------------------------------------------------
        servicos_data = [
            ("Troca de Óleo e Filtro de Óleo", 85.00),
            ("Substituição de Filtro de Ar e Combustível", 50.00),
            ("Higienização do Ar-Condicionado", 120.00),
            ("Alinhamento e Balanceamento 3D", 140.00),
            ("Troca de Pastilhas de Freio Dianteiras", 110.00),
            ("Troca de Pastilhas e Discos de Freio", 220.00),
            ("Sangria e Troca do Fluido de Freio", 95.00),
            ("Troca de Velas e Cabos de Ignição", 130.00),
            ("Limpeza de Bicos Injetores via Ultrassom", 210.00),
            ("Diagnóstico Eletrônico via Scanner", 150.00),
            ("Troca do Kit de Correia Dentada", 380.00),
            ("Troca do Amortecedor Dianteiro (Par)", 260.00),
            ("Troca do Amortecedor Traseiro (Par)", 220.00),
            ("Substituição da Bateria", 40.00),
            ("Troca da Lâmpada do Farol", 25.00),
            ("Troca da Palheta do Pára-brisa", 20.00),
            ("Substituição da Bomba d'Água", 290.00),
            ("Limpeza e Enxágue do Sistema de Arrefecimento", 180.00),
            ("Troca de Buchas da Suspensão (Par)", 190.00),
            ("Troca de Pivô de Suspensão", 100.00),
            ("Troca de Terminal de Direção", 90.00),
            ("Revisão Geral do Sistema de Ignição", 170.00),
            ("Substituição da Sonda Lambda", 120.00),
            ("Substituição da Bobina de Ignição", 80.00),
            ("Troca da Correia de Acessórios (Poli-V)", 95.00),
            ("Revisão Preventiva de 10.000 km", 320.00),
            ("Revisão Preventiva de 30.000 km", 480.00),
            ("Revisão Preventiva de 50.000 km", 650.00),
            ("Troca do Radiador de Água", 310.00),
            ("Regulagem e Limpeza do TBI (Tico de Borboleta)", 160.00),
        ]

        servicos = [
            Servico(descricao=desc, preco=p)
            for desc, p in servicos_data
        ]
        session.add_all(servicos)
        session.commit()
        for s in servicos:
            session.refresh(s)

        # ----------------------------------------------------------------------
        # 6. ORDENS DE SERVIÇO (15 registros com status variados)
        # ----------------------------------------------------------------------
        ordens_data = [
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=45), now - timedelta(days=44), "Troca de óleo de rotina.", 313.00, veiculos[0].id, mecanicos[0].id),
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=40), now - timedelta(days=39), "Barulho na suspensão ao passar em quebra-molas.", 815.00, veiculos[1].id, mecanicos[1].id),
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=35), now - timedelta(days=34), "Luz da injecção acesa e engasgos.", 585.00, veiculos[2].id, mecanicos[2].id),
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=30), now - timedelta(days=29), "Pedal do freio duro e chiado ao frear.", 620.00, veiculos[3].id, mecanicos[3].id),
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=25), now - timedelta(days=24), "Carro não liga pela manhã.", 520.00, veiculos[4].id, mecanicos[4].id),
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=20), now - timedelta(days=19), "Motor esquentando no trânsito.", 752.00, veiculos[5].id, mecanicos[5].id),
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=15), now - timedelta(days=14), "Vibração no volante acima de 80 km/h.", 140.00, veiculos[6].id, mecanicos[6].id),
            (StatusOrdemServico.CONCLUIDA, now - timedelta(days=10), now - timedelta(days=9), "Falta de potência nas retomadas.", 820.00, veiculos[7].id, mecanicos[7].id),
            (StatusOrdemServico.EM_ANDAMENTO, now - timedelta(days=3), None, "Revisão geral dos 50.000km em andamento.", 1110.00, veiculos[8].id, mecanicos[8].id),
            (StatusOrdemServico.EM_ANDAMENTO, now - timedelta(days=2), None, "Troca de amortecedores dianteiros.", 1160.00, veiculos[9].id, mecanicos[9].id),
            (StatusOrdemServico.EM_ANDAMENTO, now - timedelta(days=1), None, "Vazamento de líquido rosa abaixo do radiador.", 862.00, veiculos[10].id, mecanicos[0].id),
            (StatusOrdemServico.AGENDADA, now - timedelta(hours=5), None, "Orçamento para substituição das velas e cabos.", 390.00, veiculos[11].id, mecanicos[1].id),
            (StatusOrdemServico.AGENDADA, now - timedelta(hours=3), None, "Cheiro ruim ao ligar o ar-condicionado.", 165.00, veiculos[12].id, mecanicos[2].id),
            (StatusOrdemServico.AGENDADA, now - timedelta(hours=2), None, "Aguardando aprovação do cliente para freios.", 490.00, veiculos[13].id, mecanicos[3].id),
            (StatusOrdemServico.CANCELADA, now - timedelta(days=12), now - timedelta(days=12), "Cliente desistiu do orçamento de suspensão.", 0.00, veiculos[14].id, mecanicos[4].id),
        ]

        ordens = []
        for status, dt_ini, dt_fim, obs, valor, vid, mid in ordens_data:
            os_obj = OrdemServico(
                status=status,
                data_inicio=dt_ini,
                data_fim=dt_fim,
                observacao=obs,
                valor_total=valor,
                veiculo_id=vid,
                mecanico_id=mid,
            )
            session.add(os_obj)
            ordens.append(os_obj)

        session.commit()
        for o in ordens:
            session.refresh(o)

        # ----------------------------------------------------------------------
        # 7. ITENS DE SERVIÇO (20 itens vinculados às OS)
        # ----------------------------------------------------------------------
        itens_servico_data = [
            (1, servicos[0].preco, False, servicos[0].id, ordens[0].id),   # OS 1: Troca óleo
            (1, servicos[11].preco,False, servicos[11].id, ordens[1].id), # OS 2: Troca amortecedor
            (1, servicos[18].preco,False, servicos[18].id, ordens[1].id), # OS 2: Troca buchas
            (1, servicos[8].preco,True, servicos[8].id, ordens[2].id),   # OS 3: Limpeza bicos
            (1, servicos[9].preco,True, servicos[9].id, ordens[2].id),   # OS 3: Scanner
            (1, servicos[5].preco,True, servicos[5].id, ordens[3].id),   # OS 4: Pastilhas + discos
            (1, servicos[6].preco,True, servicos[6].id, ordens[3].id),   # OS 4: Sangria fluido
            (1, servicos[13].preco,False, servicos[13].id, ordens[4].id), # OS 5: Troca bateria
            (1, servicos[16].preco,False, servicos[16].id, ordens[5].id), # OS 5: Bomba d'água
            (1, servicos[17].preco,True, servicos[17].id, ordens[5].id), # OS 6: Arrefecimento
            (1, servicos[3].preco,True, servicos[3].id, ordens[6].id),   # OS 7: Alinhamento
            (1, servicos[10].preco,True, servicos[10].id, ordens[7].id), # OS 8: Correia dentada
            (1, servicos[27].preco,False, servicos[27].id, ordens[8].id), # OS 9: Revisão 50k
            (1, servicos[11].preco,True, servicos[11].id, ordens[9].id), # OS 10: Amortecedores
            (1, servicos[28].preco,True, servicos[28].id, ordens[10].id),# OS 11: Troca radiador
            (1, servicos[7].preco,False, servicos[7].id, ordens[11].id), # OS 12: Velas e cabos
            (1, servicos[2].preco,True, servicos[2].id, ordens[12].id), # OS 13: Ar-condicionado
            (1, servicos[4].preco,True, servicos[4].id, ordens[13].id), # OS 14: Pastilhas
            (1, servicos[1].preco,True, servicos[1].id, ordens[0].id),   # OS 1: Filtro ar/combustivel
            (1, servicos[21].preco,True, servicos[21].id, ordens[2].id), # OS 3: Ignição
        ]

        itens_servico = [
            ItemServico(tempo_hora=th, valor_hora=vh, aprovado=ap, servico_id=sid, ordem_servico_id=oid)
            for th, vh, ap, sid, oid in itens_servico_data
        ]
        session.add_all(itens_servico)

        # ----------------------------------------------------------------------
        # 8. ITENS DE PEÇA (20 itens vinculados às OS)
        # ----------------------------------------------------------------------
        itens_peca_data = [
            (4, pecas[0].preco, True, pecas[0].id, ordens[0].id),   # OS 1: 4L Óleo
            (1, pecas[1].preco,True, pecas[1].id, ordens[0].id),   # OS 1: Filtro Óleo
            (2, pecas[12].preco,True, pecas[12].id, ordens[1].id), # OS 2: 2x Amortecedores
            (2, pecas[15].preco,True, pecas[15].id, ordens[1].id), # OS 2: 2x Buchas
            (1, pecas[28].preco,True, pecas[28].id, ordens[2].id), # OS 3: Sonda Lambda
            (1, pecas[7].preco,True, pecas[7].id, ordens[3].id),   # OS 4: Pastilha dianteira
            (1, pecas[9].preco,False, pecas[9].id, ordens[3].id),   # OS 4: Discos
            (1, pecas[18].preco,False, pecas[18].id, ordens[4].id), # OS 5: Bateria
            (1, pecas[22].preco,False, pecas[22].id, ordens[5].id), # OS 6: Bomba d'água
            (2, pecas[23].preco,False, pecas[23].id, ordens[5].id), # OS 6: 2x Aditivo
            (1, pecas[21].preco,False, pecas[21].id, ordens[7].id), # OS 8: Kit Correia
            (1, pecas[27].preco,True, pecas[27].id, ordens[8].id), # OS 9: Sensor MAP
            (2, pecas[12].preco,True, pecas[12].id, ordens[9].id), # OS 10: Amortecedores
            (1, pecas[29].preco,True, pecas[29].id, ordens[10].id),# OS 11: Radiador
            (1, pecas[5].preco,True, pecas[5].id, ordens[11].id),  # OS 12: Velas
            (1, pecas[6].preco,False, pecas[6].id, ordens[11].id),  # OS 12: Cabos
            (1, pecas[4].preco,False, pecas[4].id, ordens[12].id),  # OS 13: Filtro AC
            (1, pecas[7].preco,False, pecas[7].id, ordens[13].id),  # OS 14: Pastilhas
            (1, pecas[2].preco,True, pecas[2].id, ordens[0].id),   # OS 1: Filtro Ar
            (1, pecas[11].preco,False, pecas[11].id, ordens[3].id),  # OS 4: Fluido Freio
        ]

        itens_peca = [
            ItemPeca(quantidade=q, preco_unitario=pu, aprovado=ap, peca_id=pid, ordem_servico_id=oid)
            for q, pu, ap, pid, oid in itens_peca_data
        ]
        session.add_all(itens_peca)

        # ----------------------------------------------------------------------
        # 9. DIAGNÓSTICOS (10 diagnósticos para as OS mais avançadas)
        # ----------------------------------------------------------------------
        diagnosticos_data = [
            ("Troca de óleo dentro do prazo preventivo.", 35200, "Sem avarias visíveis.", NivelCombustivel.ALTO, True, ordens[0].id),
            ("Desgaste acentuado nas buchas da bandeja e amortecedores vazando.", 68100, "Arranhão leve na porta do motorista.", NivelCombustivel.MEDIO,False, ordens[1].id),
            ("Bico injetor 2 travado aberto e sonda lambda com leitura lenta.", 52400, "Para-choque dianteiro levemente ralado.", NivelCombustivel.BAIXO,True, ordens[2].id),
            ("Pastilhas no limite de desgaste e discos com ondulação.", 41000, "Sem avarias.", NivelCombustivel.MEDIO,False, ordens[3].id),
            ("Bateria com placa em curto, não retém carga.", 31500, "Sem avarias.", NivelCombustivel.ALTO,True, ordens[4].id),
            ("Rotor da bomba d'água corroído.", 79000, "Pequeno amassado no para-lama esquerdo.", NivelCombustivel.BAIXO,False, ordens[5].id),
            ("Rodas dianteiras desbalanceadas.", 18900, "Sem avarias.", NivelCombustivel.ALTO,True, ordens[6].id),
            ("Correia dentada ressecada com risco de rompimento.", 62000, "Sem avarias.", NivelCombustivel.MEDIO,False, ordens[7].id),
            ("Revisão completa dos 50.000km.", 50100, "Risco na tampa do porta-malas.", NivelCombustivel.MEDIO,True, ordens[8].id),
            ("Amortecedor dianteiro direito travado.", 84000, "Sem avarias.", NivelCombustivel.ALTO,False, ordens[9].id),
        ]

        diagnosticos = [
            Diagnostico(
                analise_mecanico=analise,
                quilometragem=km,
                avarias_latarias=avarias,
                nivel_combustivel=nivel,
                aprovado_cliente=ap,
                ordem_servico_id=oid,
            )
            for analise, km, avarias, nivel, ap, oid in diagnosticos_data
        ]
        session.add_all(diagnosticos)

        # ----------------------------------------------------------------------
        # 10. PAGAMENTOS (10 lançamentos para as OS concluídas/em andamento)
        # ----------------------------------------------------------------------
        pagamentos_data = [
            (313.00, FormaPagamento.PIX, ordens[0].data_fim or now, ordens[0].id),
            (815.00, FormaPagamento.CREDITO, ordens[1].data_fim or now, ordens[1].id),
            (585.00, FormaPagamento.DEBITO, ordens[2].data_fim or now, ordens[2].id),
            (620.00, FormaPagamento.DINHEIRO, ordens[3].data_fim or now, ordens[3].id),
            (520.00, FormaPagamento.PIX, ordens[4].data_fim or now, ordens[4].id),
            (752.00, FormaPagamento.CREDITO, ordens[5].data_fim or now, ordens[5].id),
            (140.00, FormaPagamento.PIX, ordens[6].data_fim or now, ordens[6].id),
            (820.00, FormaPagamento.CREDITO, ordens[7].data_fim or now, ordens[7].id),
            (500.00, FormaPagamento.PIX, now - timedelta(days=1), ordens[8].id), # Sinal/Adiantamento OS 9
            (600.00, FormaPagamento.CREDITO, now, ordens[9].id),           # Sinal/Adiantamento OS 10
        ]

        pagamentos = [
            Pagamento(valor=val, forma_pagamento=forma, data=dt, ordem_servico_id=oid)
            for val, forma, dt, oid in pagamentos_data
        ]
        session.add_all(pagamentos)

        # Commita todas as tabelas e relacionamentos associados
        session.commit()

        print("Semente virou arvore com sucesso!")


if __name__ == "__main__":
    seed_database()