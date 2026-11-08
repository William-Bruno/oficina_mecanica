from enum import StrEnum

class EspecialidadeMecanico(StrEnum):
    MECANICA_GERAL = "mecanica_geral"
    INJECAO_ELETRONICA = "injecao_eletronica"
    SUSPENSAO_FREIOS = "suspensao_freios"
    CAMBIO_AUTOMATICO = "cambio_automatico"
    AR_CONDICIONADO = "ar_condicionado"
    MOTOR_RETIFICA = "motor_retifica"

class CombustivelVeiculo(StrEnum):
    GASOLINA ="gasolina"
    ALCOOL = "alcool"
    FLEX = "flex"
    HIBRIDO = "hibribo"
    DIESEL = "diesel"
    ELETRICO = "eletrico"

class StatusOrdemServico(StrEnum):
    AGENDADA = "agendada"
    EM_ORCAMENTO = "em_orcamento"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"

class FormaPagamento(StrEnum):
    DINHEIRO = "dinheiro"
    PIX = "pix"
    CREDITO = "credito"
    DEBITO = "debito"

class NivelCombustivel(StrEnum):
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"

class StatusExecucaoItem(StrEnum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"