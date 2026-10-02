class AppError(Exception):
    status_code = 500
    msg = "Erro interno no servidor"

    def __init__(self, msg: str | None = None):
        if msg:
            self.msg = msg
        super().__init__(self.msg)


class RegraDeNegocioException(AppError):
    """Regra de negócio violada"""
    status_code = 422
    msg = "Regra de negócio violada"


class RecursoNaoEncontradoException(AppError):
    """ID não existe"""
    status_code = 404
    msg = "Recurso não encontrado"


class EntidadeDuplicadaException(AppError):
    """Chave única duplicada"""
    status_code = 409
    msg = "Dado já existe no sistema"


class AssociacaoInvalidaException(AppError):
    """Violação de FK"""
    status_code = 409
    msg = "Problemas com associações entre chaves das entidades"


class ConfigError(AppError):
    """Problemas com arquivo de configuração"""
    status_code = 500
    msg = "Falha nas configurações"