from sqlmodel import SQLModel

class MetadadosPaginacao(SQLModel):
    total_registros: int
    total_paginas: int
    pagina_atual: int
    tamanho_pagina: int

