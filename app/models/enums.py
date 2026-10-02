from enum import Enum

class EspecialidadeMecanico(str, Enum):
    MECANICA_GERAL = "mecanica_geral"
    INJECAO_ELETRONICA = "injecao_eletronica"
    SUSPENSAO_FREIOS = "suspensao_freios"
    CAMBIO_AUTOMATICO = "cambio_automatico"
    AR_CONDICIONADO = "ar_condicionado"
    MOTOR_RETIFICA = "motor_retifica"

class CombustivelVeiculo(str, Enum):
    GASOLINA ="gasolina"
    ALCOOL = "alcool"
    FLEX = "flex"
    HIBRIDO = "hibribo"
    DIESEL = "diesel"
    ELETRICO = "eletrico"

class StatusOrdemServico(str, Enum):
    AGENDADA = "agendada"
    EM_ORCAMENTO = "em_orcamento"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"

class FormaPagamento(str, Enum):
    DINHEIRO = "dinheiro"
    PIX = "pix"
    CREDITO = "credito"
    DEBITO = "debito"

class NivelCombustivel(str, Enum):
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"